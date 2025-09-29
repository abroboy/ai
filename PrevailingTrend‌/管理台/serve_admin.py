#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import random
import time
from datetime import datetime
import threading
from database import init_db, update_stock_data, get_stocks, get_industries, get_db_tables, execute_db_query

# 从新浪财经获取数据
def fetch_from_sina():
    try:
        import requests
        # 获取上证指数和深证成指
        sina_url = "http://hq.sinajs.cn/list=s_sh000001,s_sz399001"
        response = requests.get(sina_url, timeout=5)
        response.raise_for_status()
        
        # 解析新浪数据格式
        raw_text = response.text
        stock_data = []
        for line in raw_text.split(';'):
            if not line.strip():
                continue
            
            parts = line.split('=')
            if len(parts) != 2:
                continue
            
            code = parts[0].split('_')[-1]
            values = parts[1].strip('"').split(',')
            if len(values) < 6:
                continue
            
            stock_data.append({
                'code': code,
                'name': values[0],
                'price': float(values[1]),
                'change_percent': float(values[3]),
                'volume': int(float(values[4])),
                'market_cap': 0,
                'industry': '指数',
                'heat_score': 100,
                'sentiment': "积极" if float(values[3]) >= 0 else "消极"
            })
        
        # 添加模拟A股数据
        for i in range(50):
            code = f"60{i:04d}"
            stock_data.append({
                'code': code,
                'name': f"模拟股票{i}",
                'price': random.uniform(5, 100),
                'change_percent': random.uniform(-5, 5),
                'volume': random.randint(10000, 1000000),
                'market_cap': random.randint(1000000, 10000000000),
                'industry': random.choice(['银行', '科技', '医药', '能源', '消费', '制造']),
                'heat_score': random.uniform(10, 100),
                'sentiment': random.choice(['积极', '中性', '消极'])
            })
        
        return stock_data
    except Exception as e:
        print(f"获取新浪数据失败: {e}")
        return []

# 异步更新数据
def async_update_data():
    while True:
        try:
            # 获取数据并更新数据库
            data = fetch_from_sina()
            if data:
                update_stock_data(data)
                print(f"数据库更新成功，共{len(data)}条记录")
            else:
                print("获取数据失败，未更新数据库")
        except Exception as e:
            print(f"数据更新失败: {e}")
        time.sleep(3600)  # 每小时更新一次

# 立即执行一次数据更新
try:
    data = fetch_from_sina()
    if data:
        update_stock_data(data)
        print(f"初始数据库更新成功，共{len(data)}条记录")
except Exception as e:
    print(f"初始数据更新失败: {e}")

# 启动时开始异步更新
update_thread = threading.Thread(target=async_update_data)
update_thread.daemon = True
update_thread.start()
import requests
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, quote
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8090"))

# 受限目录映射（避免任意访问）
SAFE_KEYS = {
    "wind": os.path.abspath(os.path.join(ROOT_DIR, "..", "第一层模块", "上市公司或行业分类")),
}

class AdminHandler(SimpleHTTPRequestHandler):
    # 重写send_head方法以优化静态文件的缓存控制
    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # 重定向到尾部带有斜杠的路径
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
            self.send_error(404, "File not found")
            return None
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            # 对于JavaScript文件，设置严格的缓存控制
            if path.endswith('.js'):
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
        # 处理页面路由
        if parsed.path == "/domestic_stocks":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(os.path.join(ROOT_DIR, "templates", "domestic_stocks.html"), "rb") as f:
                self.wfile.write(f.read())
            return
            
        # 处理API路由
        if parsed.path == "/api/domestic/hotspots" or parsed.path == "/api/domestic-hotspot":
            self._send_json(self._generate_hotspots())
            return
        if parsed.path == "/api/domestic-hotspot/stats":
            data = self._generate_hotspots()
            self._send_json(self._calc_stats(data["data"]))
            return
        if parsed.path == "/api/foreign-hotspot":
            self._send_json(self._generate_foreign_hotspots())
            return
        if parsed.path == "/api/forum-hotspot":
            self._send_json(self._generate_forum_hotspots())
            return
        if parsed.path == "/api/global-capital-flow":
            self._send_json(self._generate_global_capital_flow())
            return
        if parsed.path == "/api/tencent-jian-index":
            self._send_json(self._generate_tencent_jian_index())
            return
        if parsed.path == "/api/wind-industries":
            self._send_json(self._generate_wind_industries())
            return
        if parsed.path == "/api/company-attributes":
            self._send_json(self._generate_company_attributes())
            return
        if parsed.path == "/api/company-score-table":
            self._send_json(self._generate_company_score_table())
            return
        if parsed.path == "/api/curve-prediction-analysis":
            self._send_json(self._generate_curve_prediction_analysis())
            return
        if parsed.path == "/api/financial-statements":
            self._send_json(self._generate_financial_statements())
            return
        if parsed.path == "/api/forum-data-analysis":
            self._send_json(self._generate_forum_data_analysis())
            return
        if parsed.path == "/api/industry-company-score-table":
            self._send_json(self._generate_industry_company_score_table())
            return
        if parsed.path == "/api/industry-score-table":
            self._send_json(self._generate_industry_score_table())
            return
        if parsed.path == "/api/qichacha-data":
            self._send_json(self._generate_qichacha_data())
            return
        if parsed.path == "/api/tax-bank-report":
            self._send_json(self._generate_tax_bank_report())
            return
        if parsed.path == "/api/object-factor-weight-table":
            self._send_json(self._generate_object_factor_weight_table())
            return
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
        if parsed.path == "/api/list-dir":
            params = parse_qs(parsed.query or "")
            key = (params.get("key") or [""])[0]
            max_depth = int((params.get("depth") or ["2"])[0])
            resp = self._list_dir_by_key(key, max_depth=max_depth)
            self._send_json({"success": True, "data": resp})
            return
        # 其它路径走静态文件
        return super().do_GET()

    def _send_json(self, payload, status=200):
        # 确保JSON序列化时正确处理中文字符
        body = json.dumps(payload if "success" in payload else {"success": True, "data": payload}, 
                         ensure_ascii=False, separators=(',', ':')).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _generate_hotspots(self):
        try:
            stocks = get_stocks(100)
            if stocks:
                return {
                    "success": True,
                    "data": [{
                        'id': stock['code'],
                        'title': f"{stock['name']} ({stock['code']})",
                        'category': stock['industry'],
                        'content': f"价格: {stock['price']} 涨跌幅: {stock['change_percent']}%",
                        'publishTime': stock['last_update'],
                        'source': "数据库",
                        'heatScore': stock['heat_score'],
                        'sentiment': stock['sentiment'],
                        'keywords': [stock['industry'], "A股"]
                    } for stock in stocks]
                }
        except Exception as e:
            print(f"从数据库获取数据失败: {str(e)}")
            
        # 如果数据库中没有数据或获取失败，尝试从API获取
        try:
            # 尝试从本地缓存文件读取
            cache_file = os.path.join(ROOT_DIR, "domestic_stocks_cache.json")
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    if cached_data.get("expire_time", 0) > time.time():
                        return {"success": True, "data": cached_data["data"]}

            # 尝试新浪财经免费API
            try:
                sina_url = "http://hq.sinajs.cn/list=s_sh000001,s_sz399001"
                response = requests.get(sina_url, timeout=5)
                response.raise_for_status()
                
                # 解析新浪数据格式
                raw_text = response.text
                stock_data = []
                for line in raw_text.split(';'):
                    if not line.strip():
                        continue
                    
                    # 示例数据格式: var hq_str_s_sh000001="上证指数,3094.9209,3094.9209,3078.5500,3094.9209,3078.5500..."
                    parts = line.split('=')
                    if len(parts) != 2:
                        continue
                    
                    code = parts[0].split('_')[-1]
                    values = parts[1].strip('"').split(',')
                    if len(values) < 6:
                        continue
                    
                    stock_data.append({
                        'code': code,
                        'name': values[0],
                        'price': values[1],
                        'change_percent': str((float(values[2]) - float(values[1])) / float(values[1]) * 100),
                        'volume': values[4],
                        'industry': '指数'  # 新浪不提供行业信息，需要从其他接口获取
                    })
                
                # 获取行业数据（从东方财富免费接口）
                if stock_data:
                    eastmoney_url = "http://push2.eastmoney.com/api/qt/ulist.np/get"
                    params = {
                        'fltt': '2',
                        'fields': 'f2,f3,f12,f14,f100,f104,f105,f124',
                        'secids': '1.000001,0.399001'
                    }
                    em_response = requests.get(eastmoney_url, params=params, timeout=5)
                    if em_response.status_code == 200:
                        em_data = em_response.json().get('data', {}).get('diff', [])
                        for item in em_data:
                            for stock in stock_data:
                                if stock['code'] == item.get('f12', ''):
                                    stock['industry'] = item.get('f100', '未知行业')
                                    stock['heatScore'] = item.get('f104', 0)  # 热度评分
                
                # 转换数据格式
                mapped_data = []
                for item in stock_data:
                    mapped_item = {
                        'id': item.get("code"),
                        'title': f"{item.get('name')} ({item.get('code')})",
                        'category': item.get("industry"),
                        'content': f"当前价格: {item.get('price')} 涨跌幅: {item.get('change_percent')}%",
                        'publishTime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'source': "市场数据API",
                        'heatScore': item.get("volume", 0) / 1000000,
                        'sentiment': "积极" if float(item.get("change_percent", 0)) >= 0 else "消极",
                        'keywords': [item.get("industry"), "A股"]
                    }
                    mapped_data.append(mapped_item)
                
                if mapped_data:
                    # 更新缓存
                    with open(cache_file, 'w', encoding='utf-8') as f:
                        json.dump({
                            "data": mapped_data,
                            "expire_time": int(time.time()) + 3600  # 1小时缓存
                        }, f)
                    return {"success": True, "data": mapped_data}
            
            except Exception as api_error:
                print(f"主API调用失败: {str(api_error)}")
                # 主API失败时尝试备用API

            # 备用数据源 - 使用东方财富行业数据
            try:
                industry_url = "http://push2.eastmoney.com/api/qt/clist/get"
                params = {
                    'pn': '1',
                    'pz': '20',
                    'po': '1',
                    'np': '1',
                    'fltt': '2',
                    'invt': '2',
                    'fid': 'f3',
                    'fs': 'm:90+t:2',
                    'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152',
                    '_': str(int(time.time()*1000))
                }
                response = requests.get(industry_url, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json().get('data', {}).get('diff', [])
                    mapped_data = []
                    for item in data:
                        mapped_data.append({
                            'id': item.get('f12'),
                            'title': f"{item.get('f14')} ({item.get('f12')})",
                            'category': item.get('f100', '未知行业'),
                            'content': f"当前涨跌幅: {item.get('f3', 0)}%",
                            'publishTime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'source': "东方财富",
                            'heatScore': item.get('f104', 0),
                            'sentiment': "积极" if float(item.get('f3', 0)) >= 0 else "消极",
                            'keywords': [item.get('f100', '未知行业'), "A股"]
                        })
                    if mapped_data:
                        return {"success": True, "data": mapped_data}
            
            except Exception as e:
                print(f"备用API调用失败: {str(e)}")

            # 最终回退到本地缓存或模拟数据
            backup_file = os.path.join(ROOT_DIR, "domestic_stocks_backup.json")
            if os.path.exists(backup_file):
                with open(backup_file, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                    return {"success": True, "data": backup_data.get("data", [])}

            return {
                "success": True,
                "data": [
                    {
                        'id': "000001",
                        'title': "上证指数 (000001)",
                        'category': "指数",
                        'content': "默认数据，请配置有效数据源",
                        'publishTime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'source': "系统",
                        'heatScore': 50,
                        'sentiment': "中性",
                        'keywords': ["指数", "A股"]
                    }
                ]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"获取国内上市公司数据失败: {str(e)}",
                "data": []
            }

    def _calc_stats(self, data):
        stats = {
            "total_hotspots": len(data),
            "finance_hotspots": 0,
            "policy_hotspots": 0,
            "market_hotspots": 0,
            "industry_hotspots": 0,
            "company_hotspots": 0,
            "macro_hotspots": 0,
            "investment_hotspots": 0,
            "positive_count": 0,
            "neutral_count": 0,
            "negative_count": 0,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        cat_map = {
            "财经热点": "finance_hotspots",
            "政策动态": "policy_hotspots",
            "市场新闻": "market_hotspots",
            "行业资讯": "industry_hotspots",
            "公司热点": "company_hotspots",
            "宏观经济": "macro_hotspots",
            "投资热点": "investment_hotspots",
        }
        for item in data:
            key = cat_map.get(item.get("category"))
            if key:
                stats[key] += 1
            sentiment = item.get("sentiment")
            if sentiment == "积极":
                stats["positive_count"] += 1
            elif sentiment == "中性":
                stats["neutral_count"] += 1
            elif sentiment == "消极":
                stats["negative_count"] += 1
        p, n, z = stats["positive_count"], stats["negative_count"], stats["neutral_count"]
        stats["market_sentiment"] = "积极" if p >= n and p >= z else ("消极" if n >= p and n >= z else "中性")
        return {"success": True, "data": stats}

    def _generate_foreign_hotspots(self):
        # 模拟国外热点数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            foreign_hotspots = [
                {"id": 1, "title": "美联储加息预期升温", "source": "Bloomberg", "date": "2025-09-20", "impact": 92, "region": "北美", "category": "货币政策"},
                {"id": 2, "title": "欧盟碳关税机制正式实施", "source": "Reuters", "date": "2025-09-19", "impact": 85, "region": "欧洲", "category": "环保政策"},
                {"id": 3, "title": "日本央行调整收益率曲线控制政策", "source": "Nikkei", "date": "2025-09-18", "impact": 78, "region": "亚太", "category": "货币政策"},
                {"id": 4, "title": "英国推出新一轮科技创新战略", "source": "Financial Times", "date": "2025-09-17", "impact": 72, "region": "欧洲", "category": "产业政策"},
                {"id": 5, "title": "印度修订外商投资政策", "source": "Economic Times", "date": "2025-09-16", "impact": 76, "region": "亚太", "category": "投资政策"},
                {"id": 6, "title": "巴西启动大规模基础设施建设计划", "source": "Globo", "date": "2025-09-15", "impact": 68, "region": "拉美", "category": "基建政策"},
                {"id": 7, "title": "德国汽车产业转型加速", "source": "Der Spiegel", "date": "2025-09-14", "impact": 83, "region": "欧洲", "category": "产业政策"},
                {"id": 8, "title": "沙特阿拉伯宣布新能源投资计划", "source": "Al Jazeera", "date": "2025-09-13", "impact": 79, "region": "中东", "category": "能源政策"},
                {"id": 9, "title": "澳大利亚矿产资源税改革", "source": "Australian Financial Review", "date": "2025-09-12", "impact": 74, "region": "亚太", "category": "税收政策"},
                {"id": 10, "title": "加拿大推出新的移民政策", "source": "CBC News", "date": "2025-09-11", "impact": 65, "region": "北美", "category": "人口政策"}
            ]
            
            return {"success": True, "data": foreign_hotspots}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取国外热点数据失败: {str(e)}",
                "data": []
            }

    def _generate_forum_hotspots(self):
        # 模拟论坛热点数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            forum_hotspots = [
                {"id": 1, "title": "新能源汽车行业未来发展前景如何？", "platform": "雪球", "author": "价值投资者", "date": "2025-09-22", "views": 12580, "comments": 356, "sentiment": 0.78},
                {"id": 2, "title": "半导体国产化进程加速，哪些公司将受益？", "platform": "雪球", "author": "科技研究员", "date": "2025-09-21", "views": 9876, "comments": 245, "sentiment": 0.85},
                {"id": 3, "title": "美联储加息对A股影响分析", "platform": "东方财富网", "author": "宏观经济学家", "date": "2025-09-20", "views": 15670, "comments": 423, "sentiment": -0.32},
                {"id": 4, "title": "医药板块估值修复，关注这些细分领域", "platform": "雪球", "author": "医药行业分析师", "date": "2025-09-19", "views": 7890, "comments": 198, "sentiment": 0.56},
                {"id": 5, "title": "ChatGPT-6发布，AI概念股再度爆发", "platform": "集思录", "author": "人工智能研究", "date": "2025-09-18", "views": 18920, "comments": 567, "sentiment": 0.92},
                {"id": 6, "title": "地产政策松绑，房地产股会否迎来转机？", "platform": "东方财富网", "author": "地产观察家", "date": "2025-09-17", "views": 11230, "comments": 321, "sentiment": 0.12},
                {"id": 7, "title": "新一轮稀土价格上涨，产业链全景梳理", "platform": "雪球", "author": "资源研究员", "date": "2025-09-16", "views": 6540, "comments": 187, "sentiment": 0.65},
                {"id": 8, "title": "光伏行业产能过剩担忧加剧", "platform": "集思录", "author": "能源分析师", "date": "2025-09-15", "views": 8760, "comments": 234, "sentiment": -0.45},
                {"id": 9, "title": "军工板块持续走强，关注这些细分龙头", "platform": "雪球", "author": "军工研究员", "date": "2025-09-14", "views": 9870, "comments": 276, "sentiment": 0.82},
                {"id": 10, "title": "消费电子行业复苏迹象明显", "platform": "东方财富网", "author": "科技消费分析", "date": "2025-09-13", "views": 7650, "comments": 198, "sentiment": 0.43}
            ]
            
            return {"success": True, "data": forum_hotspots}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取论坛热点数据失败: {str(e)}",
                "data": []
            }

    def _generate_global_capital_flow(self):
        # 模拟全球资金流向数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            capital_flow_data = [
                {"id": 1, "region": "北美", "inflow": 2856.7, "outflow": 2345.8, "netFlow": 510.9, "change": 3.2, "date": "2025-09-22"},
                {"id": 2, "region": "欧洲", "inflow": 1987.3, "outflow": 2156.4, "netFlow": -169.1, "change": -1.8, "date": "2025-09-22"},
                {"id": 3, "region": "亚太", "inflow": 3245.6, "outflow": 2876.9, "netFlow": 368.7, "change": 2.5, "date": "2025-09-22"},
                {"id": 4, "region": "中国", "inflow": 1567.8, "outflow": 1234.5, "netFlow": 333.3, "change": 4.7, "date": "2025-09-22"},
                {"id": 5, "region": "日本", "inflow": 876.5, "outflow": 923.7, "netFlow": -47.2, "change": -0.8, "date": "2025-09-22"},
                {"id": 6, "region": "印度", "inflow": 567.3, "outflow": 432.1, "netFlow": 135.2, "change": 5.6, "date": "2025-09-22"},
                {"id": 7, "region": "拉美", "inflow": 432.8, "outflow": 567.2, "netFlow": -134.4, "change": -3.5, "date": "2025-09-22"},
                {"id": 8, "region": "中东", "inflow": 789.4, "outflow": 654.3, "netFlow": 135.1, "change": 2.8, "date": "2025-09-22"},
                {"id": 9, "region": "非洲", "inflow": 234.5, "outflow": 187.6, "netFlow": 46.9, "change": 4.2, "date": "2025-09-22"},
                {"id": 10, "region": "澳洲", "inflow": 345.7, "outflow": 321.4, "netFlow": 24.3, "change": 1.1, "date": "2025-09-22"}
            ]
            
            return {"success": True, "data": capital_flow_data}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取全球资金流向数据失败: {str(e)}",
                "data": []
            }

    def _generate_tencent_jian_index(self):
        # 模拟腾讯济安指数数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            jian_index_data = {
                "currentIndex": 78.5,
                "previousIndex": 76.2,
                "change": 2.3,
                "updateTime": "2025-09-23 09:30",
                "historicalData": [
                    {"date": "2025-09-16", "value": 75.8},
                    {"date": "2025-09-17", "value": 74.6},
                    {"date": "2025-09-18", "value": 75.2},
                    {"date": "2025-09-19", "value": 76.5},
                    {"date": "2025-09-20", "value": 76.8},
                    {"date": "2025-09-21", "value": 76.2},
                    {"date": "2025-09-22", "value": 77.4},
                    {"date": "2025-09-23", "value": 78.5}
                ]
            }
            
            return {"success": True, "data": jian_index_data}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取腾讯济安指数数据失败: {str(e)}",
                "data": {}
            }

    def _generate_wind_industries(self):
        # 模拟上市公司或行业分类数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            wind_industries_data = [
                {
                    "industryCode": "6101000000",
                    "industryName": "能源",
                    "industryLevel": 1,
                    "parentIndustryCode": None,
                    "companyCount": 234,
                    "marketCap": 15678.90
                },
                {
                    "industryCode": "6101010000",
                    "industryName": "石油天然气",
                    "industryLevel": 2,
                    "parentIndustryCode": "6101000000",
                    "companyCount": 78,
                    "marketCap": 5432.18
                },
                {
                    "industryCode": "6101020000",
                    "industryName": "煤炭",
                    "industryLevel": 2,
                    "parentIndustryCode": "6101000000",
                    "companyCount": 56,
                    "marketCap": 3245.67
                },
                {
                    "industryCode": "6101030000",
                    "industryName": "新能源",
                    "industryLevel": 2,
                    "parentIndustryCode": "6101000000",
                    "companyCount": 100,
                    "marketCap": 6999.05
                },
                {
                    "industryCode": "6102000000",
                    "industryName": "材料",
                    "industryLevel": 1,
                    "parentIndustryCode": None,
                    "companyCount": 189,
                    "marketCap": 8765.43
                },
                {
                    "industryCode": "6102010000",
                    "industryName": "有色金属",
                    "industryLevel": 2,
                    "parentIndustryCode": "6102000000",
                    "companyCount": 67,
                    "marketCap": 3456.78
                },
                {
                    "industryCode": "6102020000",
                    "industryName": "钢铁",
                    "industryLevel": 2,
                    "parentIndustryCode": "6102000000",
                    "companyCount": 45,
                    "marketCap": 1876.54
                },
                {
                    "industryCode": "6102030000",
                    "industryName": "化工",
                    "industryLevel": 2,
                    "parentIndustryCode": "6102000000",
                    "companyCount": 77,
                    "marketCap": 3432.11
                }
            ]
            
            return {"success": True, "data": wind_industries_data}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取上市公司或行业分类数据失败: {str(e)}",
                "data": []
            }

    def _generate_company_attributes(self):
        # 模拟公司属性数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            company_attributes_data = [
                {"id": 1, "name": "腾讯控股", "industry": "互联网", "region": "深圳", "marketCap": 3500, "employees": 108000, "riskLevel": "中低"},
                {"id": 2, "name": "阿里巴巴", "industry": "互联网", "region": "杭州", "marketCap": 2800, "employees": 254000, "riskLevel": "中"},
                {"id": 3, "name": "贵州茅台", "industry": "白酒", "region": "贵州", "marketCap": 2200, "employees": 42000, "riskLevel": "低"},
                {"id": 4, "name": "中国平安", "industry": "金融", "region": "深圳", "marketCap": 1800, "employees": 364000, "riskLevel": "中高"},
                {"id": 5, "name": "宁德时代", "industry": "新能源", "region": "福建", "marketCap": 1200, "employees": 88000, "riskLevel": "中"},
                {"id": 6, "name": "美团", "industry": "互联网", "region": "北京", "marketCap": 950, "employees": 92000, "riskLevel": "中高"},
                {"id": 7, "name": "京东", "industry": "电商", "region": "北京", "marketCap": 850, "employees": 460000, "riskLevel": "中"},
                {"id": 8, "name": "中国移动", "industry": "通信", "region": "北京", "marketCap": 1500, "employees": 456000, "riskLevel": "低"},
                {"id": 9, "name": "比亚迪", "industry": "汽车", "region": "深圳", "marketCap": 1100, "employees": 288000, "riskLevel": "中"},
                {"id": 10, "name": "拼多多", "industry": "电商", "region": "上海", "marketCap": 900, "employees": 12000, "riskLevel": "高"}
            ]
            
            return {"success": True, "data": company_attributes_data}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取公司属性数据失败: {str(e)}",
                "data": []
            }

    def _generate_company_score_table(self):
        # 模拟公司分值表数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            score_data = {
                "updateTime": "2025-09-25 14:30:00",
                "totalCompanies": 3500,
                "averageScore": 68.5,
                "scoreDistribution": {
                    "90-100": 320,
                    "80-89": 680,
                    "70-79": 950,
                    "60-69": 780,
                    "50-59": 420,
                    "0-49": 350
                },
                "topCompanies": [
                    {"rank": 1, "code": "600519", "name": "贵州茅台", "industry": "白酒", "score": 96.8, "change": 0.5},
                    {"rank": 2, "code": "000858", "name": "五粮液", "industry": "白酒", "score": 94.2, "change": 0.3},
                    {"rank": 3, "code": "601318", "name": "中国平安", "industry": "保险", "score": 93.5, "change": -0.2},
                    {"rank": 4, "code": "600036", "name": "招商银行", "industry": "银行", "score": 92.7, "change": 0.8},
                    {"rank": 5, "code": "000333", "name": "美的集团", "industry": "家电", "score": 91.9, "change": 1.2}
                ],
                "bottomCompanies": [
                    {"rank": 3496, "code": "002456", "name": "某某科技", "industry": "电子", "score": 32.5, "change": -2.8},
                    {"rank": 3497, "code": "600123", "name": "某某股份", "industry": "制造", "score": 31.8, "change": -1.5},
                    {"rank": 3498, "code": "300789", "name": "某某生物", "industry": "医药", "score": 30.2, "change": -3.2},
                    {"rank": 3499, "code": "002789", "name": "某某通信", "industry": "通信", "score": 28.5, "change": -4.5},
                    {"rank": 3500, "code": "600321", "name": "某某能源", "industry": "能源", "score": 25.3, "change": -5.2}
                ],
                "biggestGainers": [
                    {"code": "300059", "name": "某某电子", "industry": "电子", "score": 78.5, "change": 8.7},
                    {"code": "002230", "name": "某某科技", "industry": "计算机", "score": 75.2, "change": 7.9},
                    {"code": "600882", "name": "某某汽车", "industry": "汽车", "score": 82.3, "change": 7.5},
                    {"code": "300750", "name": "某某医疗", "industry": "医疗", "score": 79.8, "change": 7.2},
                    {"code": "002415", "name": "某某材料", "industry": "材料", "score": 76.5, "change": 6.8}
                ],
                "biggestLosers": [
                    {"code": "002789", "name": "某某通信", "industry": "通信", "score": 28.5, "change": -4.5},
                    {"code": "600321", "name": "某某能源", "industry": "能源", "score": 25.3, "change": -5.2},
                    {"code": "300125", "name": "某某网络", "industry": "传媒", "score": 35.8, "change": -5.5},
                    {"code": "002156", "name": "某某金融", "industry": "金融", "score": 42.3, "change": -6.2},
                    {"code": "600721", "name": "某某地产", "industry": "房地产", "score": 38.7, "change": -7.5}
                ],
                "scoreFactors": [
                    {"factor": "财务状况", "weight": 30},
                    {"factor": "市场表现", "weight": 25},
                    {"factor": "行业地位", "weight": 20},
                    {"factor": "风险因素", "weight": 15},
                    {"factor": "社会评价", "weight": 10}
                ]
            }
            
            return {"success": True, "data": score_data}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取公司分值表数据失败: {str(e)}",
                "data": {}
            }

    def _generate_curve_prediction_analysis(self):
        # 模拟曲线预测分析数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            prediction_data = {
                "historicalData": [95.2, 95.8, 96.3, 95.9, 96.5],
                "predictedData": [96.5, 97.2, 97.8, 98.3],
                "confidenceInterval": {
                    "lower": [95.8, 96.4, 97.0, 97.5],
                    "upper": [97.2, 98.0, 98.6, 99.1]
                },
                "accuracy": 0.85,
                "modelParameters": {
                    "alpha": 0.05,
                    "beta": 0.1,
                    "gamma": 0.3
                }
            }
            
            return {"success": True, "data": prediction_data}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取曲线预测分析数据失败: {str(e)}",
                "data": {}
            }

    def _generate_financial_statements(self):
        # 模拟财务三表数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            financial_data = {
                "companyName": "贵州茅台",
                "period": "2025年第三季度",
                "balanceSheet": {
                    "assets": 285678900000,
                    "liabilities": 156789000000,
                    "equity": 128889900000
                },
                "incomeStatement": {
                    "revenue": 123456789000,
                    "cost": 34567890000,
                    "profit": 45678901234
                },
                "cashFlow": {
                    "operating": 56789012345,
                    "investing": -23456789012,
                    "financing": -12345678901
                },
                "ratios": {
                    "currentRatio": 2.3,
                    "debtToEquity": 1.22,
                    "grossMargin": 0.72,
                    "roe": 0.35
                },
                "history": [
                    {"period": "2024Q4", "revenue": 112345678900, "profit": 41234567890, "assets": 267890123456},
                    {"period": "2025Q1", "revenue": 115678901234, "profit": 42345678901, "assets": 273456789012},
                    {"period": "2025Q2", "revenue": 118901234567, "profit": 43456789012, "assets": 278901234567}
                ]
            }
            
            return {"success": True, "data": financial_data}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取财务三表数据失败: {str(e)}",
                "data": {}
            }

    def _generate_forum_data_analysis(self):
        # 模拟雪球等论坛数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            forum_data = {
                "period": "2025年9月20日-2025年9月25日",
                "summary": {
                    "totalPosts": 12458,
                    "totalComments": 87654,
                    "totalUsers": 5432,
                    "sentimentScore": 0.65
                },
                "topStocks": [
                    {"code": "600519", "name": "贵州茅台", "mentions": 1245, "sentiment": 0.82},
                    {"code": "000858", "name": "五粮液", "mentions": 987, "sentiment": 0.75},
                    {"code": "601318", "name": "中国平安", "mentions": 876, "sentiment": 0.45},
                    {"code": "600036", "name": "招商银行", "mentions": 765, "sentiment": 0.62},
                    {"code": "000333", "name": "美的集团", "mentions": 654, "sentiment": 0.58}
                ],
                "topTopics": [
                    {"topic": "新能源", "mentions": 2345, "sentiment": 0.78},
                    {"topic": "半导体", "mentions": 1876, "sentiment": 0.72},
                    {"topic": "人工智能", "mentions": 1654, "sentiment": 0.85},
                    {"topic": "医药", "mentions": 1432, "sentiment": 0.65},
                    {"topic": "消费", "mentions": 1321, "sentiment": 0.58}
                ],
                "sentimentTrend": [
                    {"date": "09-20", "score": 0.62},
                    {"date": "09-21", "score": 0.65},
                    {"date": "09-22", "score": 0.68},
                    {"date": "09-23", "score": 0.64},
                    {"date": "09-24", "score": 0.63},
                    {"date": "09-25", "score": 0.65}
                ],
                "hotPosts": [
                    {"title": "新能源汽车行业深度分析", "author": "价值投资者", "views": 12500, "comments": 876, "sentiment": 0.75},
                    {"title": "半导体产业链全景图", "author": "芯片研究", "views": 10200, "comments": 765, "sentiment": 0.82},
                    {"title": "人工智能应用场景展望", "author": "科技前沿", "views": 9800, "comments": 654, "sentiment": 0.88},
                    {"title": "医药行业投资机会", "author": "医药研究员", "views": 8500, "comments": 543, "sentiment": 0.65},
                    {"title": "消费升级趋势分析", "author": "消费洞察", "views": 7800, "comments": 432, "sentiment": 0.72}
                ]
            }
            
            return {"success": True, "data": forum_data}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取论坛数据分析数据失败: {str(e)}",
                "data": {}
            }

    def _generate_industry_company_score_table(self):
        # 模拟行业+公司分值表数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            # 模拟行业数据
            industries = [
                {"code": "BK0438", "name": "半导体", "score": 94.5, "companies": 85},
                {"code": "BK0475", "name": "新能源", "score": 92.8, "companies": 102},
                {"code": "BK0428", "name": "医疗器械", "score": 91.2, "companies": 76},
                {"code": "BK0447", "name": "白酒", "score": 90.5, "companies": 32},
                {"code": "BK0451", "name": "云计算", "score": 89.7, "companies": 68},
                {"code": "BK0433", "name": "人工智能", "score": 88.5, "companies": 55},
                {"code": "BK0465", "name": "生物医药", "score": 87.2, "companies": 92},
                {"code": "BK0422", "name": "煤炭", "score": 58.5, "companies": 45},
                {"code": "BK0478", "name": "钢铁", "score": 56.2, "companies": 38},
                {"code": "BK0424", "name": "航运", "score": 52.8, "companies": 29}
            ]
            
            # 模拟当前选中行业的公司数据
            selected_industry_companies = {
                "industryCode": "BK0438",
                "industryName": "半导体",
                "industryScore": 94.5,
                "updateTime": "2025-09-25 14:30:00",
                "companies": [
                    {"rank": 1, "code": "603501", "name": "韦尔股份", "score": 96.8, "change": 0.5, "marketCap": 1850.5, "pe": 42.3, "pbr": 8.5},
                    {"rank": 2, "code": "688981", "name": "中芯国际", "score": 95.2, "change": 0.8, "marketCap": 2350.8, "pe": 38.7, "pbr": 7.2},
                    {"rank": 3, "code": "002049", "name": "紫光国微", "score": 94.5, "change": 1.2, "marketCap": 1250.3, "pe": 35.2, "pbr": 6.8},
                    {"rank": 4, "code": "002371", "name": "北方华创", "score": 93.7, "change": 0.3, "marketCap": 980.5, "pe": 40.5, "pbr": 7.8},
                    {"rank": 5, "code": "300782", "name": "卓胜微", "score": 92.8, "change": -0.2, "marketCap": 850.2, "pe": 36.8, "pbr": 6.5},
                    {"rank": 6, "code": "603986", "name": "兆易创新", "score": 91.5, "change": 0.7, "marketCap": 780.5, "pe": 32.5, "pbr": 5.8},
                    {"rank": 7, "code": "688012", "name": "中微公司", "score": 90.8, "change": 1.5, "marketCap": 720.3, "pe": 45.2, "pbr": 8.2},
                    {"rank": 8, "code": "300458", "name": "全志科技", "score": 89.5, "change": 0.8, "marketCap": 650.8, "pe": 38.5, "pbr": 6.2},
                    {"rank": 9, "code": "688396", "name": "华润微", "score": 88.7, "change": 0.5, "marketCap": 620.5, "pe": 35.8, "pbr": 5.5},
                    {"rank": 10, "code": "300223", "name": "北京君正", "score": 87.2, "change": -0.3, "marketCap": 580.2, "pe": 42.5, "pbr": 7.2}
                ],
                "scoreDistribution": {
                    "90-100": 8,
                    "80-89": 25,
                    "70-79": 32,
                    "60-69": 15,
                    "50-59": 4,
                    "0-49": 1
                },
                "industryAvgFinancials": {
                    "pe": 38.5,
                    "pbr": 6.8,
                    "roe": 18.2,
                    "netProfitGrowth": 25.3,
                    "revenueGrowth": 22.5
                }
            }
            
            return {"success": True, "data": {
                "industries": industries,
                "selectedIndustryCompanies": selected_industry_companies
            }}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取行业+公司分值表数据失败: {str(e)}",
                "data": {}
            }

    def _generate_industry_score_table(self):
        # 模拟行业分值表数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            industry_data = {
                "updateTime": "2025-09-25 14:30:00",
                "totalIndustries": 28,
                "averageScore": 72.3,
                "scoreDistribution": {
                    "90-100": 3,
                    "80-89": 7,
                    "70-79": 10,
                    "60-69": 5,
                    "50-59": 2,
                    "0-49": 1
                },
                "topIndustries": [
                    {"rank": 1, "code": "BK0438", "name": "半导体", "score": 94.5, "change": 1.2, "companies": 85, "avgCompanyScore": 82.3},
                    {"rank": 2, "code": "BK0475", "name": "新能源", "score": 92.8, "change": 0.5, "companies": 102, "avgCompanyScore": 80.7},
                    {"rank": 3, "code": "BK0428", "name": "医疗器械", "score": 91.2, "change": 0.8, "companies": 76, "avgCompanyScore": 79.5},
                    {"rank": 4, "code": "BK0447", "name": "白酒", "score": 90.5, "change": -0.3, "companies": 32, "avgCompanyScore": 83.2},
                    {"rank": 5, "code": "BK0451", "name": "云计算", "score": 89.7, "change": 1.5, "companies": 68, "avgCompanyScore": 78.9}
                ],
                "bottomIndustries": [
                    {"rank": 24, "code": "BK0422", "name": "煤炭", "score": 58.5, "change": -1.2, "companies": 45, "avgCompanyScore": 55.3},
                    {"rank": 25, "code": "BK0478", "name": "钢铁", "score": 56.2, "change": -0.8, "companies": 38, "avgCompanyScore": 54.1},
                    {"rank": 26, "code": "BK0424", "name": "航运", "score": 52.8, "change": -2.5, "companies": 29, "avgCompanyScore": 51.7},
                    {"rank": 27, "code": "BK0456", "name": "纺织服装", "score": 48.5, "change": -1.7, "companies": 42, "avgCompanyScore": 47.2},
                    {"rank": 28, "code": "BK0476", "name": "传统零售", "score": 45.3, "change": -3.2, "companies": 36, "avgCompanyScore": 44.8}
                ],
                "biggestGainers": [
                    {"code": "BK0451", "name": "云计算", "score": 89.7, "change": 1.5, "companies": 68, "avgCompanyScore": 78.9},
                    {"code": "BK0438", "name": "半导体", "score": 94.5, "change": 1.2, "companies": 85, "avgCompanyScore": 82.3},
                    {"code": "BK0428", "name": "医疗器械", "score": 91.2, "change": 0.8, "companies": 76, "avgCompanyScore": 79.5},
                    {"code": "BK0475", "name": "新能源", "score": 92.8, "change": 0.5, "companies": 102, "avgCompanyScore": 80.7},
                    {"code": "BK0433", "name": "人工智能", "score": 88.5, "change": 0.4, "companies": 55, "avgCompanyScore": 77.2}
                ],
                "biggestLosers": [
                    {"code": "BK0476", "name": "传统零售", "score": 45.3, "change": -3.2, "companies": 36, "avgCompanyScore": 44.8},
                    {"code": "BK0424", "name": "航运", "score": 52.8, "change": -2.5, "companies": 29, "avgCompanyScore": 51.7},
                    {"code": "BK0456", "name": "纺织服装", "score": 48.5, "change": -1.7, "companies": 42, "avgCompanyScore": 47.2},
                    {"code": "BK0422", "name": "煤炭", "score": 58.5, "change": -1.2, "companies": 45, "avgCompanyScore": 55.3},
                    {"code": "BK0478", "name": "钢铁", "score": 56.2, "change": -0.8, "companies": 38, "avgCompanyScore": 54.1}
                ],
                "scoreFactors": [
                    {"factor": "行业景气度", "weight": 25},
                    {"factor": "政策支持", "weight": 20},
                    {"factor": "成长性", "weight": 20},
                    {"factor": "竞争格局", "weight": 15},
                    {"factor": "风险因素", "weight": 10},
                    {"factor": "社会评价", "weight": 10}
                ]
            }
            
            return {"success": True, "data": industry_data}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取行业分值表数据失败: {str(e)}",
                "data": {}
            }

    def _generate_qichacha_data(self):
        # 模拟企查查数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            qichacha_data = {
                "companyName": "示例科技有限公司",
                "regNumber": "91310101MA1FPX1234",
                "legalPerson": "张三",
                "regCapital": "1000万元人民币",
                "establishDate": "2018-05-20",
                "status": "存续",
                "industry": "科技推广和应用服务业",
                "address": "上海市浦东新区张江高科技园区",
                "shareholders": [
                    {"name": "张三", "ratio": "40%", "type": "自然人"},
                    {"name": "李四", "ratio": "30%", "type": "自然人"},
                    {"name": "北京投资有限公司", "ratio": "30%", "type": "企业法人"}
                ],
                "changes": [
                    {"date": "2023-03-15", "type": "注册资本变更", "before": "500万元", "after": "1000万元"},
                    {"date": "2022-08-10", "type": "股东变更", "before": "王五", "after": "李四"},
                    {"date": "2021-12-05", "type": "地址变更", "before": "北京市海淀区", "after": "上海市浦东新区"}
                ],
                "riskInfo": {
                    "lawsuits": 2,
                    "courtAnnouncements": 1,
                    "executions": 0,
                    "abnormalOperations": 0,
                    "penalties": 1
                },
                "relatedCompanies": [
                    {"name": "上海关联公司", "relation": "同一法人", "risk": "低"},
                    {"name": "深圳分公司", "relation": "分支机构", "risk": "中"}
                ]
            }
            
            return {"success": True, "data": qichacha_data}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取企查查数据失败: {str(e)}",
                "data": {}
            }

    def _generate_tax_bank_report(self):
        # 模拟税银报告数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            report_data = {
                "companyName": "示例科技有限公司",
                "period": "2025年第三季度",
                "taxInfo": {
                    "totalTax": 45000000,
                    "taxCompliance": "A级",
                    "overdueTax": 0,
                    "taxCredits": 120
                },
                "bankInfo": {
                    "creditRating": "AA+",
                    "loanAmount": 200000000,
                    "overdueLoan": 0,
                    "creditLines": 500000000
                },
                "riskAssessment": {
                    "taxRisk": "低风险",
                    "financialRisk": "中风险",
                    "overallRisk": "中风险"
                },
                "history": [
                    {"period": "2025Q2", "taxRisk": "低风险", "financialRisk": "低风险", "overallRisk": "低风险"},
                    {"period": "2025Q1", "taxRisk": "低风险", "financialRisk": "中风险", "overallRisk": "中风险"},
                    {"period": "2024Q4", "taxRisk": "中风险", "financialRisk": "中风险", "overallRisk": "中风险"}
                ]
            }
            
            return {"success": True, "data": report_data}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取税银报告数据失败: {str(e)}",
                "data": {}
            }

    def _generate_object_factor_weight_table(self):
        # 模拟对象因子权重表数据
        # 在实际应用中，这里应该连接真实的数据源
        try:
            weight_data = {
                "updateTime": "2025-09-25 14:30:00",
                "objectTypes": ["公司", "行业", "市场"],
                "currentObjectType": "公司",
                "factorCategories": [
                    {
                        "name": "财务因子",
                        "factors": [
                            {"id": "F001", "name": "净利润增长率", "weight": 25, "description": "反映公司盈利能力的增长情况"},
                            {"id": "F002", "name": "资产负债率", "weight": 15, "description": "反映公司的负债水平和偿债能力"},
                            {"id": "F003", "name": "ROE", "weight": 20, "description": "反映公司的净资产收益率"},
                            {"id": "F004", "name": "毛利率", "weight": 10, "description": "反映公司的盈利能力"},
                            {"id": "F005", "name": "经营现金流", "weight": 15, "description": "反映公司的现金流状况"},
                            {"id": "F006", "name": "营收增长率", "weight": 15, "description": "反映公司的业务增长情况"}
                        ],
                        "totalWeight": 100
                    },
                    {
                        "name": "市场因子",
                        "factors": [
                            {"id": "M001", "name": "市盈率", "weight": 20, "description": "反映公司的估值水平"},
                            {"id": "M002", "name": "市净率", "weight": 15, "description": "反映公司的净资产估值水平"},
                            {"id": "M003", "name": "股价波动率", "weight": 25, "description": "反映公司股价的波动情况"},
                            {"id": "M004", "name": "相对大盘表现", "weight": 20, "description": "反映公司相对于大盘的表现"},
                            {"id": "M005", "name": "成交量变化", "weight": 20, "description": "反映公司股票的交易活跃度"}
                        ],
                        "totalWeight": 100
                    },
                    {
                        "name": "行业因子",
                        "factors": [
                            {"id": "I001", "name": "行业景气度", "weight": 30, "description": "反映行业的整体发展状况"},
                            {"id": "I002", "name": "行业竞争格局", "weight": 25, "description": "反映行业的竞争情况"},
                            {"id": "I003", "name": "政策支持度", "weight": 20, "description": "反映行业的政策支持情况"},
                            {"id": "I004", "name": "行业成长性", "weight": 25, "description": "反映行业的未来发展潜力"}
                        ],
                        "totalWeight": 100
                    },
                    {
                        "name": "风险因子",
                        "factors": [
                            {"id": "R001", "name": "流动性风险", "weight": 20, "description": "反映公司的短期偿债能力"},
                            {"id": "R002", "name": "经营风险", "weight": 25, "description": "反映公司的经营稳定性"},
                            {"id": "R003", "name": "财务风险", "weight": 20, "description": "反映公司的财务健康状况"},
                            {"id": "R004", "name": "市场风险", "weight": 15, "description": "反映公司面临的市场环境风险"},
                            {"id": "R005", "name": "政策风险", "weight": 20, "description": "反映公司面临的政策变动风险"}
                        ],
                        "totalWeight": 100
                    },
                    {
                        "name": "社会评价因子",
                        "factors": [
                            {"id": "S001", "name": "媒体评价", "weight": 25, "description": "反映公司在媒体中的评价情况"},
                            {"id": "S002", "name": "社交媒体情绪", "weight": 30, "description": "反映公司在社交媒体中的情绪倾向"},
                            {"id": "S003", "name": "分析师评级", "weight": 25, "description": "反映专业分析师对公司的评级"},
                            {"id": "S004", "name": "ESG评分", "weight": 20, "description": "反映公司的环境、社会和治理表现"}
                        ],
                        "totalWeight": 100
                    }
                ],
                "objectWeights": {
                    "公司": [
                        {"category": "财务因子", "weight": 35},
                        {"category": "市场因子", "weight": 25},
                        {"category": "行业因子", "weight": 15},
                        {"category": "风险因子", "weight": 15},
                        {"category": "社会评价因子", "weight": 10}
                    ],
                    "行业": [
                        {"category": "财务因子", "weight": 20},
                        {"category": "市场因子", "weight": 15},
                        {"category": "行业因子", "weight": 40},
                        {"category": "风险因子", "weight": 15},
                        {"category": "社会评价因子", "weight": 10}
                    ],
                    "市场": [
                        {"category": "财务因子", "weight": 15},
                        {"category": "市场因子", "weight": 40},
                        {"category": "行业因子", "weight": 20},
                        {"category": "风险因子", "weight": 15},
                        {"category": "社会评价因子", "weight": 10}
                    ]
                },
                "presetTemplates": [
                    {"id": "T001", "name": "成长型", "description": "适合评估高成长性公司"},
                    {"id": "T002", "name": "价值型", "description": "适合评估稳定价值型公司"},
                    {"id": "T003", "name": "防御型", "description": "适合评估抗风险能力强的公司"},
                    {"id": "T004", "name": "周期型", "description": "适合评估周期性行业公司"}
                ],
                "simulationResults": {
                    "beforeScore": 85.2,
                    "afterScore": 82.7,
                    "changedFactors": [
                        {"id": "F001", "name": "净利润增长率", "oldWeight": 25, "newWeight": 20, "impact": -1.5},
                        {"id": "M003", "name": "股价波动率", "oldWeight": 25, "newWeight": 30, "impact": -1.0}
                    ]
                }
            }
            
            return {"success": True, "data": weight_data}
        except Exception as e:
            return {
                "success": False,
                "message": f"获取对象因子权重表数据失败: {str(e)}",
                "data": {}
            }

    def _list_dir_by_key(self, key: str, max_depth: int = 2):
        root = SAFE_KEYS.get(key)
        if not root or not os.path.isdir(root):
            return {"root": None, "items": []}
        def walk(d: str, depth: int):
            node = {"name": os.path.basename(d), "path": os.path.relpath(d, root), "type": "dir", "children": []}
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


def run():
    os.chdir(ROOT_DIR)
    httpd = HTTPServer(("", PORT), AdminHandler)
    print("========================================")
    print("管理台与API同端口服务器启动中...")
    print(f"端口: {PORT}")
    print("静态根目录:", ROOT_DIR)
    print("页面:  http://localhost:%d/index.html" % PORT)
    print("API:   /api/domestic-hotspot, /api/domestic-hotspot/stats, /api/list-dir?key=wind")
    print("========================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")

if __name__ == "__main__":
    run()