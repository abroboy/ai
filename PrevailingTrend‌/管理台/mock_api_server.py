#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

class MockAPIHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/wind-industries':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # 模拟万得行业分类数据
            mock_data = {
                "success": True,
                "data": [
                    # 一级行业
                    {"industryCode": "480100", "industryName": "银行", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "银行业务"},
                    {"industryCode": "430100", "industryName": "房地产开发", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "房地产开发业务"},
                    {"industryCode": "490000", "industryName": "非银金融", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "非银行金融机构"},
                    {"industryCode": "420000", "industryName": "交通运输", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "交通运输服务"},
                    {"industryCode": "360000", "industryName": "电子", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "电子设备制造"},
                    {"industryCode": "280000", "industryName": "电气设备", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "电气设备制造"},
                    {"industryCode": "220000", "industryName": "化工", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "化工产品制造"},
                    {"industryCode": "180000", "industryName": "食品饮料", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "食品饮料制造"},
                    {"industryCode": "120000", "industryName": "医药生物", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "医药生物技术"},
                    {"industryCode": "100000", "industryName": "计算机", "industryLevel": 1, "parentIndustryCode": None, "industryDescription": "计算机软件服务"},
                    
                    # 二级行业
                    {"industryCode": "610300", "industryName": "白酒", "industryLevel": 2, "parentIndustryCode": "180000", "industryDescription": "白酒制造"},
                    {"industryCode": "360100", "industryName": "半导体", "industryLevel": 2, "parentIndustryCode": "360000", "industryDescription": "半导体器件制造"},
                    {"industryCode": "280100", "industryName": "电机", "industryLevel": 2, "parentIndustryCode": "280000", "industryDescription": "电机制造"},
                    {"industryCode": "220100", "industryName": "基础化工", "industryLevel": 2, "parentIndustryCode": "220000", "industryDescription": "基础化工原料"},
                    {"industryCode": "180100", "industryName": "食品加工", "industryLevel": 2, "parentIndustryCode": "180000", "industryDescription": "食品加工制造"},
                    {"industryCode": "120100", "industryName": "化学制药", "industryLevel": 2, "parentIndustryCode": "120000", "industryDescription": "化学药品制造"},
                    {"industryCode": "100100", "industryName": "软件开发", "industryLevel": 2, "parentIndustryCode": "100000", "industryDescription": "软件开发服务"},
                    {"industryCode": "480200", "industryName": "保险", "industryLevel": 2, "parentIndustryCode": "480100", "industryDescription": "保险业务"},
                    {"industryCode": "430200", "industryName": "物业管理", "industryLevel": 2, "parentIndustryCode": "430100", "industryDescription": "物业管理服务"},
                    {"industryCode": "490100", "industryName": "证券", "industryLevel": 2, "parentIndustryCode": "490000", "industryDescription": "证券业务"},
                    {"industryCode": "420100", "industryName": "航空运输", "industryLevel": 2, "parentIndustryCode": "420000", "industryDescription": "航空运输服务"},
                    {"industryCode": "360200", "industryName": "消费电子", "industryLevel": 2, "parentIndustryCode": "360000", "industryDescription": "消费电子产品"},
                    {"industryCode": "280200", "industryName": "新能源设备", "industryLevel": 2, "parentIndustryCode": "280000", "industryDescription": "新能源设备制造"},
                    {"industryCode": "220200", "industryName": "精细化工", "industryLevel": 2, "parentIndustryCode": "220000", "industryDescription": "精细化工产品"},
                    {"industryCode": "180200", "industryName": "软饮料", "industryLevel": 2, "parentIndustryCode": "180000", "industryDescription": "软饮料制造"}
                ],
                "total": 25
            }
            
            response = json.dumps(mock_data, ensure_ascii=False, indent=2)
            self.wfile.write(response.encode('utf-8'))
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = json.dumps({"success": False, "error": "API endpoint not found"})
            self.wfile.write(error_response.encode('utf-8'))
    
    def log_message(self, format, *args):
        print(f"[{self.date_time_string()}] {format % args}")

if __name__ == "__main__":
    PORT = 5001
    
    with socketserver.TCPServer(("", PORT), MockAPIHandler) as httpd:
        print(f"========================================")
        print(f"万得行业分类API模拟服务器启动中...")
        print(f"端口: {PORT}")
        print(f"API地址: http://localhost:{PORT}/api/wind-industries")
        print(f"========================================")
        print(f"按 Ctrl+C 停止服务器")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n服务器已停止")
