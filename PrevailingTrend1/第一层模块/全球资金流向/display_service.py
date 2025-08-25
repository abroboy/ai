#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球资金流向数据展示服务
独立的数据展示模块，无密码管理
"""

import os
import sys
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 创建必要的目录
os.makedirs('static/charts', exist_ok=True)
os.makedirs('static/reports', exist_ok=True)
os.makedirs('logs', exist_ok=True)

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """仪表盘页面"""
    return render_template('dashboard.html')

@app.route('/api/dashboard_data')
def dashboard_data():
    """仪表盘数据API"""
    return jsonify({
        "success": True,
        "data": {
            "global_analysis": {
                "forex": {"total_net_flow": 150.5, "flow_trend": "up"},
                "stock": {"total_net_flow": -45.2, "flow_trend": "down"},
                "global": {"total_net_flow": 105.3, "flow_trend": "up"}
            },
            "last_update": datetime.now().isoformat()
        }
    })

@app.route('/api/flow_analysis')
def flow_analysis():
    """资金流向分析API"""
    period = request.args.get('period', '30d')
    return jsonify({
        "success": True,
        "data": {
            "period": period,
            "analysis": {
                "forex": {"total_net_flow": 150.5},
                "stock": {"total_net_flow": -45.2},
                "global": {"total_net_flow": 105.3}
            },
            "timestamp": datetime.now().isoformat()
        }
    })

@app.route('/api/system_status')
def system_status():
    """系统状态API"""
    return jsonify({
        "success": True,
        "data": {
            "system_status": "running",
            "database_connected": True,
            "last_update": datetime.now().isoformat(),
            "service": "display_service"
        }
    })

@app.route('/api/health')
def health_check():
    """健康检查API"""
    return jsonify({
        "success": True,
        "message": "数据展示服务运行正常",
        "timestamp": datetime.now().isoformat(),
        "service": "display_service"
    })

if __name__ == '__main__':
    print("=" * 60)
    print("全球资金流向数据展示服务")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("服务正在启动...")
    print()
    print("访问地址:")
    print("- 首页: http://localhost:5003/")
    print("- 仪表盘: http://localhost:5003/dashboard")
    print()
    print("API端点:")
    print("- 仪表盘数据: http://localhost:5003/api/dashboard_data")
    print("- 资金流向分析: http://localhost:5003/api/flow_analysis")
    print("- 系统状态: http://localhost:5003/api/system_status")
    print("- 健康检查: http://localhost:5003/api/health")
    print("=" * 60)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5003,
            debug=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n数据展示服务已停止")
    except Exception as e:
        print(f"启动失败: {e}") 