#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime, timedelta
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import random

# 数据库模块
import database
from database import init_db, get_stocks, get_industries, get_db_tables, execute_db_query

# 模块化API导入
from api.csv_data_reader import build_csv_based_response, build_industry_statistics_response
from api.wind import generate_wind_industries
from api.domestic_hotspots import generate_domestic_hotspots
# 公司数据结构导入
from api.company import StockCompany, create_company_from_akshare_data

# 服务器配置
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8090"))

# 受限目录映射
SAFE_KEYS = {
    "wind": os.path.abspath(os.path.join(ROOT_DIR, "..", "第一层模块", "上市公司或行业分类")),
}

class AdminHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        """优化静态文件缓存控制"""
        # 对于/@vite/client等开发工具路径，直接返回404但不报错
        if self.path == '/@vite/client':
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            return None
        
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            # 自定义404页面，对开发工具相关请求特殊处理
            if self.path.endswith('.js') or self.path.endswith('.css'):
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                return None
            else:
                self.send_error(404, "File not found")
                return None
        
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            
            # 优化缓存策略：JS和CSS文件设置合理的缓存控制
            if path.endswith('.js') or path.endswith('.css'):
                # 设置1小时的缓存时间，同时支持ETag验证
                self.send_header("Cache-Control", "max-age=3600, must-revalidate")
                self.send_header("ETag", f"{fs.st_mtime}-{fs.st_size}")
            elif path.endswith(('.html', '.htm')):
                # HTML文件不缓存，确保获取最新版本
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
            
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def do_GET(self):
        parsed = urlparse(self.path)
        
        # 页面路由
        if parsed.path == "/domestic_stocks":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(os.path.join(ROOT_DIR, "templates", "domestic_stocks.html"), "rb") as f:
                self.wfile.write(f.read())
            return
        
        # API路由 - 上市公司数据（新的CSV数据源）
        if parsed.path == "/api/listed-companies":
            params = parse_qs(parsed.query or "")
            page = int((params.get("page") or ["0"])[0])
            size = int((params.get("size") or ["10"])[0])
            industry = (params.get("industry") or [None])[0]
            try:
                resp = build_csv_based_response(page, size, industry)
                self._send_json(resp)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)})
            return
        
        if parsed.path == "/api/listed-companies/stats":
            try:
                resp = build_industry_statistics_response()
                self._send_json(resp)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)})
            return
        
        # API路由 - 行业统计数据（基于CSV）
        if parsed.path == "/api/industry-statistics":
            try:
                resp = build_industry_statistics_response()
                self._send_json(resp)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)})
            return
        
        # API路由 - 数据库查询
        if parsed.path == "/api/db-query":
            params = parse_qs(parsed.query or "")
            query = (params.get("query") or [""])[0]
            if not query:
                self._send_json({
                    "success": False,
                    "message": "查询参数不能为空",
                    "data": None
                })
                return
            try:
                result = execute_db_query(query)
                self._send_json(result)
            except Exception as e:
                self._send_json({
                    "success": False,
                    "message": f"查询执行失败: {str(e)}",
                    "data": None
                })
            return
        
        # API路由 - 基本功能路由
        api_routes = {
            "/api/domestic-hotspot": self._generate_domestic_hotspots,
            "/api/wind-industries": generate_wind_industries,
            "/api/global-capital-flow": self._generate_global_capital_flow,
            "/api/tencent-jian-index": self._generate_tencent_jian_index,
        }
        
        if parsed.path in api_routes:
            try:
                data = api_routes[parsed.path]()
                if not data.get("data"):
                    data["data"] = []
                self._send_json(data)
            except Exception as e:
                self._send_json({
                    "success": False,
                    "message": f"获取数据失败: {str(e)}",
                    "data": []
                }, status=500)
            return
        
        # API路由 - 数据库相关
        if parsed.path == "/api/db/tables":
            self._send_json({"success": True, "data": get_db_tables()})
            return
        
        if parsed.path == "/api/db/query":
            params = parse_qs(parsed.query or "")
            query = (params.get("query") or [""])[0]
            if query:
                result = execute_db_query(query)
                self._send_json(result)
            else:
                self._send_json({"success": False, "message": "查询语句不能为空"})
            return
        
        # API路由 - 目录列表
        if parsed.path == "/api/list-dir":
            params = parse_qs(parsed.query or "")
            key = (params.get("key") or [""])[0]
            max_depth = int((params.get("depth") or ["2"])[0])
            resp = self._list_dir_by_key(key, max_depth=max_depth)
            self._send_json({"success": True, "data": resp})
            return
        
        # 默认静态文件处理
        return super().do_GET()

    def _send_json(self, payload, status=200):
        """发送JSON响应"""
        body = json.dumps(
            payload if "success" in payload else {"success": True, "data": payload}, 
            ensure_ascii=False, 
            separators=(',', ':')
        ).encode("utf-8")
        
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _list_dir_by_key(self, key: str, max_depth: int = 2):
        """根据key列出目录结构"""
        root = SAFE_KEYS.get(key)
        if not root or not os.path.isdir(root):
            return {"root": None, "items": []}
        
        def walk(d: str, depth: int):
            node = {
                "name": os.path.basename(d), 
                "path": os.path.relpath(d, root), 
                "type": "dir", 
                "children": []
            }
            if depth >= max_depth:
                return node
            
            try:
                for name in sorted(os.listdir(d)):
                    fp = os.path.join(d, name)
                    if os.path.isdir(fp):
                        node["children"].append(walk(fp, depth + 1))
                    else:
                        try:
                            size = os.path.getsize(fp)
                        except OSError:
                            size = 0
                        node["children"].append({
                            "name": name,
                            "path": os.path.relpath(fp, root).replace("\\", "/"),
                            "type": "file",
                            "size": size
                        })
            except OSError:
                pass
            return node
        
        tree = walk(root, 0)
        return {"root": root, "items": tree}

    def _generate_domestic_hotspots(self):
        """生成国内热点数据"""
        try:
            # 导入服务
            from services.domestic_hotspot_fetcher import get_domestic_hotspots
            
            # 获取热点数据
            result = get_domestic_hotspots()
            
            if result.get('success'):
                return result
            else:
                # 如果服务失败，返回模拟数据
                return self._get_mock_domestic_hotspots()
                
        except Exception as e:
            print(f"获取国内热点数据失败: {e}")
            # 返回模拟数据作为备用
            return self._get_mock_domestic_hotspots()
    
    def _get_mock_domestic_hotspots(self):
        """获取模拟国内热点数据"""
        mock_hotspots = [
            {
                "id": "dom_001",
                "title": "A股三季度收官：结构性行情明显",
                "content": "科技股领涨，新能源板块分化，消费股企稳回升",
                "category": "A股",
                "heat_score": 95,
                "sentiment": "积极",
                "source": "证券时报",
                "publish_time": (datetime.now() - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S"),
                "keywords": ["A股", "科技股", "新能源", "消费股"],
                "url": "#"
            },
            {
                "id": "dom_002",
                "title": "央行降准释放流动性1.2万亿",
                "content": "定向降准支持实体经济，房地产板块迎来反弹",
                "category": "货币政策",
                "heat_score": 92,
                "sentiment": "积极",
                "source": "中国证券报",
                "publish_time": (datetime.now() - timedelta(minutes=25)).strftime("%Y-%m-%d %H:%M:%S"),
                "keywords": ["央行", "降准", "流动性", "房地产"],
                "url": "#"
            },
            {
                "id": "dom_003",
                "title": "新能源汽车销量创历史新高",
                "content": "9月销量同比增长35%，产业链公司业绩分化",
                "category": "新能源",
                "heat_score": 89,
                "sentiment": "积极",
                "source": "财经网",
                "publish_time": (datetime.now() - timedelta(minutes=40)).strftime("%Y-%m-%d %H:%M:%S"),
                "keywords": ["新能源汽车", "销量", "产业链"],
                "url": "#"
            },
            {
                "id": "dom_004",
                "title": "人工智能大模型商业化提速",
                "content": "AI应用场景不断拓展，相关概念股受追捧",
                "category": "科技",
                "heat_score": 87,
                "sentiment": "积极",
                "source": "21世纪经济报道",
                "publish_time": (datetime.now() - timedelta(minutes=55)).strftime("%Y-%m-%d %H:%M:%S"),
                "keywords": ["人工智能", "大模型", "AI", "概念股"],
                "url": "#"
            },
            {
                "id": "dom_005",
                "title": "消费板块复苏信号增强",
                "content": "节假日消费数据亮眼，消费信心逐步恢复",
                "category": "消费",
                "heat_score": 82,
                "sentiment": "积极",
                "source": "经济日报",
                "publish_time": (datetime.now() - timedelta(minutes=70)).strftime("%Y-%m-%d %H:%M:%S"),
                "keywords": ["消费", "复苏", "节假日", "消费信心"],
                "url": "#"
            },
            {
                "id": "dom_006",
                "title": "房地产政策持续优化调整",
                "content": "多地出台支持政策，市场预期逐步改善",
                "category": "房地产",
                "heat_score": 78,
                "sentiment": "中性",
                "source": "中国房地产报",
                "publish_time": (datetime.now() - timedelta(minutes=85)).strftime("%Y-%m-%d %H:%M:%S"),
                "keywords": ["房地产", "政策", "支持", "市场预期"],
                "url": "#"
            }
        ]
        
        # 计算统计数据
        category_dist = {}
        sentiment_dist = {"积极": 0, "中性": 0, "消极": 0}
        source_dist = {}
        total_heat = 0
        
        for hotspot in mock_hotspots:
            # 分类统计
            cat = hotspot["category"]
            category_dist[cat] = category_dist.get(cat, 0) + 1
            
            # 情感统计
            sent = hotspot["sentiment"]
            if sent in sentiment_dist:
                sentiment_dist[sent] += 1
            
            # 来源统计
            src = hotspot["source"]
            source_dist[src] = source_dist.get(src, 0) + 1
            
            # 热度统计
            total_heat += hotspot["heat_score"]
        
        # 热度分布
        high_heat = len([h for h in mock_hotspots if h["heat_score"] >= 80])
        medium_heat = len([h for h in mock_hotspots if 60 <= h["heat_score"] < 80])
        low_heat = len([h for h in mock_hotspots if h["heat_score"] < 60])
        
        statistics = {
            "total_count": len(mock_hotspots),
            "avg_heat_score": total_heat / len(mock_hotspots),
            "category_distribution": category_dist,
            "sentiment_distribution": sentiment_dist,
            "source_distribution": source_dist,
            "heat_distribution": {
                "high": high_heat,
                "medium": medium_heat,
                "low": low_heat
            },
            "top_keywords": [
                {"keyword": "A股", "count": 3},
                {"keyword": "政策", "count": 2},
                {"keyword": "新能源", "count": 2},
                {"keyword": "消费", "count": 2}
            ]
        }
        
        return {
            "success": True,
            "data": mock_hotspots,
            "statistics": statistics,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_count": len(mock_hotspots)
        }

    def _generate_global_capital_flow(self):
        """生成全球资金流向数据"""
        try:
            # 基础地区数据
            regions_base = {
                '北美': {'inflow': 5678.9, 'outflow': 5530.4, 'change_range': (-2, 5)},
                '欧洲': {'inflow': 4321.5, 'outflow': 4223.7, 'change_range': (-1, 3)},
                '亚太': {'inflow': 6789.2, 'outflow': 6560.7, 'change_range': (2, 8)},
                '中国': {'inflow': 7890.6, 'outflow': 7557.3, 'change_range': (3, 10)},
                '日本': {'inflow': 1234.5, 'outflow': 1281.7, 'change_range': (-5, 1)},
                '印度': {'inflow': 2345.8, 'outflow': 2210.6, 'change_range': (4, 12)},
                '韩国': {'inflow': 1876.3, 'outflow': 1823.7, 'change_range': (1, 6)},
                '东南亚': {'inflow': 1567.4, 'outflow': 1489.2, 'change_range': (2, 8)},
                '中东': {'inflow': 987.6, 'outflow': 1023.4, 'change_range': (-3, 2)},
                '拉美': {'inflow': 876.5, 'outflow': 912.3, 'change_range': (-2, 4)},
                '非洲': {'inflow': 543.2, 'outflow': 567.8, 'change_range': (-1, 5)},
                '澳洲': {'inflow': 765.4, 'outflow': 743.2, 'change_range': (0, 4)}
            }
            
            # 生成当前数据
            capital_flow_data = []
            for i, (region, base_data) in enumerate(regions_base.items(), 1):
                # 添加随机波动
                inflow_variation = random.uniform(-50, 50)
                outflow_variation = random.uniform(-50, 50)
                
                inflow = base_data['inflow'] + inflow_variation
                outflow = base_data['outflow'] + outflow_variation
                net_flow = inflow - outflow
                
                # 计算变化率
                change_min, change_max = base_data['change_range']
                change = random.uniform(change_min, change_max)
                
                capital_flow_data.append({
                    'id': i,
                    'region': region,
                    'inflow': round(inflow, 1),
                    'outflow': round(outflow, 1),
                    'netFlow': round(net_flow, 1),
                    'change': round(change, 1),
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
            
            # 生成历史数据（用于图表）
            historical_data = {
                'dates': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)],
                'series': []
            }
            
            for region in regions_base.keys():
                # 生成7天的历史净流入数据
                base_net = next(item['netFlow'] for item in capital_flow_data if item['region'] == region)
                historical_series = []
                for i in range(7):
                    variation = random.uniform(-20, 20)
                    historical_series.append(round(base_net + variation, 1))
                
                historical_data['series'].append({
                    'name': region,
                    'data': historical_series
                })
            
            # 添加世界地图坐标数据
            map_data = {
                '北美': {'lat': 45.0, 'lng': -100.0, 'population': 579000000},
                '欧洲': {'lat': 54.0, 'lng': 15.0, 'population': 746400000},
                '亚太': {'lat': 35.0, 'lng': 103.0, 'population': 4641000000},
                '中国': {'lat': 35.0, 'lng': 104.0, 'population': 1439323776},
                '日本': {'lat': 36.2, 'lng': 138.2, 'population': 126476461},
                '印度': {'lat': 20.5, 'lng': 78.9, 'population': 1380004385},
                '韩国': {'lat': 35.9, 'lng': 127.7, 'population': 51269185},
                '东南亚': {'lat': 1.3, 'lng': 103.8, 'population': 673000000},
                '中东': {'lat': 29.5, 'lng': 47.8, 'population': 411000000},
                '拉美': {'lat': -8.7, 'lng': -55.1, 'population': 652000000},
                '非洲': {'lat': -8.7, 'lng': 34.5, 'population': 1340000000},
                '澳洲': {'lat': -25.2, 'lng': 133.7, 'population': 25499884}
            }
            
            # 为每个地区添加地图坐标
            for item in capital_flow_data:
                region = item['region']
                if region in map_data:
                    item.update(map_data[region])
            
            # 计算汇总数据
            total_inflow = sum(item['inflow'] for item in capital_flow_data)
            total_outflow = sum(item['outflow'] for item in capital_flow_data)
            net_global_flow = sum(item['netFlow'] for item in capital_flow_data)
            
            summary = {
                'totalNetInflow': round(net_global_flow, 1),
                'totalChange': round(random.uniform(-2, 5), 1),
                'activeMarkets': len(capital_flow_data),
                'maxInflow': round(max(item['netFlow'] for item in capital_flow_data), 1),
                'maxOutflow': round(min(item['netFlow'] for item in capital_flow_data), 1)
            }
            
            return {
                "success": True,
                "message": "全球资金流向数据获取成功",
                "data": capital_flow_data,
                "historical": historical_data,
                "summary": summary,
                "timestamp": datetime.now().isoformat(),
                "total_regions": len(capital_flow_data),
                "total_inflow": round(total_inflow, 1),
                "total_outflow": round(total_outflow, 1),
                "net_global_flow": round(net_global_flow, 1)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"生成全球资金流向数据失败: {str(e)}",
                "data": [],
                "error": str(e)
            }

    def _generate_tencent_jian_index(self):
        """生成腾讯济安指数数据"""
        try:
            # 模拟腾讯济安指数数据
            index_data = {
                "current_index": 3247.85,
                "change": 38.76,
                "change_percent": 1.23,
                "open": 3210.45,
                "high": 3256.78,
                "low": 3205.12,
                "volume": 1567890000,
                "turnover": 45678900000,
                "pe_ratio": 18.56,
                "pb_ratio": 2.34,
                "dividend_yield": 1.85,
                "market_cap": 2800000000000,
                "constituent_count": 156,
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 成分股数据
            constituents = [
                {
                    "code": "000858",
                    "name": "五粮液",
                    "weight": 8.5,
                    "price": 156.78,
                    "change": 2.1,
                    "change_percent": 1.36,
                    "contribution": 0.18
                },
                {
                    "code": "000568",
                    "name": "泸州老窖",
                    "weight": 7.2,
                    "price": 234.56,
                    "change": 1.8,
                    "change_percent": 0.77,
                    "contribution": 0.13
                },
                {
                    "code": "002415",
                    "name": "海康威视",
                    "weight": 6.8,
                    "price": 34.12,
                    "change": -0.5,
                    "change_percent": -1.44,
                    "contribution": -0.03
                },
                {
                    "code": "600519",
                    "name": "贵州茅台",
                    "weight": 6.5,
                    "price": 1789.23,
                    "change": 12.5,
                    "change_percent": 0.70,
                    "contribution": 0.09
                },
                {
                    "code": "000001",
                    "name": "平安银行",
                    "weight": 5.8,
                    "price": 12.34,
                    "change": 0.12,
                    "change_percent": 0.98,
                    "contribution": 0.07
                }
            ]
            
            # 行业分布
            industry_distribution = [
                {"industry": "食品饮料", "weight": 28.5, "count": 24},
                {"industry": "电子科技", "weight": 23.2, "count": 32},
                {"industry": "医药生物", "weight": 18.7, "count": 28},
                {"industry": "金融服务", "weight": 12.4, "count": 18},
                {"industry": "新能源", "weight": 8.9, "count": 15},
                {"industry": "其他", "weight": 8.3, "count": 39}
            ]
            
            # 历史数据（用于图表）
            historical_data = {
                "dates": [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(29, -1, -1)],
                "values": [3200 + random.uniform(-50, 50) for _ in range(30)]
            }
            
            # 计算统计数据
            total_weight = sum(item["weight"] for item in constituents)
            avg_change = sum(item["change_percent"] for item in constituents) / len(constituents)
            positive_count = len([item for item in constituents if item["change"] > 0])
            negative_count = len([item for item in constituents if item["change"] < 0])
            
            statistics = {
                "total_weight": total_weight,
                "avg_change": round(avg_change, 2),
                "positive_count": positive_count,
                "negative_count": negative_count,
                "neutral_count": len(constituents) - positive_count - negative_count,
                "top_contributor": max(constituents, key=lambda x: x["contribution"])["name"],
                "bottom_contributor": min(constituents, key=lambda x: x["contribution"])["name"]
            }
            
            return {
                "success": True,
                "message": "腾讯济安指数数据获取成功",
                "data": {
                    "index": index_data,
                    "constituents": constituents,
                    "industry_distribution": industry_distribution,
                    "historical": historical_data,
                    "statistics": statistics
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"生成腾讯济安指数数据失败: {str(e)}",
                "data": {},
                "error": str(e)
            }


def main():
    """主启动函数 - 统一的服务器启动入口"""
    # 切换到根目录
    os.chdir(ROOT_DIR)
    
    # 创建HTTP服务器
    httpd = HTTPServer(("", PORT), AdminHandler)
    
    print("========================================")
    print("大势所趋风险框架管理台启动中...")
    print(f"端口: {PORT}")
    print("静态根目录:", ROOT_DIR)
    print("访问地址: http://localhost:%d/index.html" % PORT)
    print("API接口: /api/listed-companies, /api/db/query")
    print("         /api/domestic-hotspot, /api/wind-industries")
    print("         /api/global-capital-flow, /api/tencent-jian-index")
    print("========================================")
    print("按 Ctrl+C 停止服务器")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")

def run():
    """保持向后兼容的启动函数"""
    main()

if __name__ == "__main__":
    main()