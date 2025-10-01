#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

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
            self.send_error(404, "File not found")
            return None
        
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            # JavaScript文件设置严格缓存控制
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
        
        # 页面路由
        if parsed.path == "/domestic_stocks":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(os.path.join(ROOT_DIR, "templates", "domestic_stocks.html"), "rb") as f:
                self.wfile.write(f.read())
            return
        
        # 国内热点数据模块已删除
        
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
            "/api/domestic-hotspot": generate_domestic_hotspots,
            "/api/wind-industries": generate_wind_industries,
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