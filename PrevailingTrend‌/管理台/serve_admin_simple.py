#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# 数据库模块
try:
    import database
    from database import init_db, get_stocks, get_industries, get_db_tables, execute_db_query
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("警告: 数据库模块不可用")

# CSV数据读取器
from api.csv_data_reader import build_csv_based_response, build_industry_statistics_response

# 服务器配置
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8090"))

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
        
        # API路由 - 股票数据（新增）
        if parsed.path == "/api/stock-data":
            params = parse_qs(parsed.query or "")
            page = int((params.get("page") or ["0"])[0])
            size = int((params.get("size") or ["50"])[0])
            industry = (params.get("industry") or [None])[0]
            try:
                resp = build_csv_based_response(page, size, industry)
                self._send_json(resp)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)})
            return
        
        # API路由 - 公司名称（新增）
        if parsed.path == "/api/company-names":
            try:
                resp = build_csv_based_response(0, 10000)  # 获取所有公司名称
                # 只返回代码和名称
                if resp.get("success") and resp.get("data", {}).get("content"):
                    companies = [{"code": item["code"], "name": item["name"]} 
                               for item in resp["data"]["content"]]
                    self._send_json({"success": True, "data": companies})
                else:
                    self._send_json({"success": False, "error": "无法获取公司名称"})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)})
            return
        
        # API路由 - 行业数据（新增）
        if parsed.path == "/api/industry-data":
            try:
                resp = build_industry_statistics_response()
                self._send_json(resp)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)})
            return
        
        # API路由 - 数据库查询（如果数据库可用）
        if parsed.path == "/api/db-query" and DATABASE_AVAILABLE:
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
        
        # API路由 - 数据库相关（如果数据库可用）
        if parsed.path == "/api/db/tables" and DATABASE_AVAILABLE:
            self._send_json({"success": True, "data": get_db_tables()})
            return
        
        if parsed.path == "/api/db/query" and DATABASE_AVAILABLE:
            params = parse_qs(parsed.query or "")
            query = (params.get("query") or [""])[0]
            if query:
                result = execute_db_query(query)
                self._send_json(result)
            else:
                self._send_json({"success": False, "message": "查询语句不能为空"})
            return
        
        # 占位API路由 - 返回示例数据
        placeholder_routes = {
            "/api/domestic/hotspots": {"data": [], "message": "热点数据模块未配置"},
            "/api/domestic-hotspot": {"data": [], "message": "热点数据模块未配置"},
            "/api/domestic-hotspot/stats": {"data": {}, "message": "统计模块未配置"},
            "/api/foreign-hotspot": {"data": [], "message": "外资热点模块未配置"},
            "/api/forum-hotspot": {"data": [], "message": "论坛热点模块未配置"},
            "/api/global-capital-flow": {"data": [], "message": "全球资金流向模块未配置"},
            "/api/tencent-jian-index": {"data": [], "message": "腾讯指数模块未配置"},
            "/api/wind-industries": {"data": [], "message": "Wind行业数据模块未配置"},
        }
        
        if parsed.path in placeholder_routes:
            self._send_json({
                "success": True,
                **placeholder_routes[parsed.path]
            })
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


def run():
    """启动服务器"""
    os.chdir(ROOT_DIR)
    httpd = HTTPServer(("", PORT), AdminHandler)
    print("========================================")
    print("管理台服务器启动中...")
    print(f"端口: {PORT}")
    print("静态根目录:", ROOT_DIR)
    print("页面:  http://localhost:%d/index.html" % PORT)
    print("API:   /api/listed-companies, /api/stock-data, /api/company-names, /api/industry-data")
    if DATABASE_AVAILABLE:
        print("数据库: /api/db/query")
    print("========================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")


if __name__ == "__main__":
    run()