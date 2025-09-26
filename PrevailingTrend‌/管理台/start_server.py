#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from http.server import HTTPServer
from serve_admin import AdminHandler

# 设置端口
PORT = int(os.environ.get("PORT", "8090"))
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    # 切换到根目录
    os.chdir(ROOT_DIR)
    
    # 创建HTTP服务器
    httpd = HTTPServer(("", PORT), AdminHandler)
    
    print("========================================")
    print("大势所趋风险框架管理台启动中...")
    print(f"端口: {PORT}")
    print("静态根目录:", ROOT_DIR)
    print("访问地址: http://localhost:%d/index.html" % PORT)
    print("API接口: /api/domestic-hotspot, /api/domestic-hotspot/stats")
    print("========================================")
    print("按 Ctrl+C 停止服务器")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")

if __name__ == "__main__":
    main()