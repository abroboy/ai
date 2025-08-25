#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的全球资金流向分析系统启动脚本
"""

import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 创建必要的目录
os.makedirs('static/charts', exist_ok=True)
os.makedirs('static/reports', exist_ok=True)
os.makedirs('logs', exist_ok=True)
os.makedirs('templates/admin', exist_ok=True)

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """仪表盘页面"""
    return render_template('dashboard.html')

@app.route('/admin/login')
def admin_login_page():
    """管理台登录页面"""
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    """管理台仪表盘"""
    return render_template('admin/dashboard.html')

@app.route('/api/status')
def status():
    """系统状态API"""
    return jsonify({
        'success': True,
        'message': '系统运行正常',
        'data': {
            'system_status': 'running',
            'database_connected': False,
            'last_update': datetime.now().isoformat(),
            'api_version': '1.0.0',
            'uptime': '刚刚启动'
        }
    })

@app.route('/api/collect_data', methods=['POST'])
def collect_data():
    """收集数据API（模拟）"""
    return jsonify({
        'success': True,
        'message': '数据收集成功（模拟）',
        'data': {
            'total_records': 150,
            'timestamp': datetime.now().isoformat()
        }
    })

@app.route('/api/analyze_flow', methods=['GET'])
def analyze_flow():
    """分析资金流向API（模拟）"""
    return jsonify({
        'success': True,
        'message': '分析完成（模拟）',
        'data': {
            'global_analysis': {
                'forex': {'total_net_flow': 150.5, 'flow_trend': 'up'},
                'stock': {'total_net_flow': -45.2, 'flow_trend': 'down'},
                'global': {'total_net_flow': 105.3, 'flow_trend': 'up'}
            },
            'analysis_period': '30天',
            'timestamp': datetime.now().isoformat()
        }
    })

@app.route('/admin/api/login', methods=['POST'])
def admin_login():
    """管理台登录API"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # 简单的用户验证
        valid_users = {
            'admin': 'admin123',
            'manager': 'manager123',
            'viewer': 'viewer123'
        }
        
        if username in valid_users and valid_users[username] == password:
            return jsonify({
                'success': True,
                'message': '登录成功',
                'data': {
                    'token': 'mock_token_' + username,
                    'user': {
                        'username': username,
                        'role': 'admin' if username == 'admin' else 'user',
                        'permissions': ['read', 'write'] if username == 'admin' else ['read']
                    }
                }
            })
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'message': '登录失败'}), 500

@app.route('/admin/api/system_status')
def admin_system_status():
    """管理台系统状态API"""
    return jsonify({
        'success': True,
        'data': {
            'database_tables': 0,
            'total_records': 0,
            'database_size': 0,
            'last_update': datetime.now().isoformat(),
            'system_status': 'running'
        }
    })

@app.route('/admin/api/collect_data', methods=['POST'])
def admin_collect_data():
    """管理台数据收集API"""
    return jsonify({
        'success': True,
        'message': '数据收集成功（模拟）',
        'data': {
            'total_records': 150,
            'asset_types': ['forex', 'stock', 'bond'],
            'timestamp': datetime.now().isoformat()
        }
    })

@app.route('/admin/api/analyze_data', methods=['POST'])
def admin_analyze_data():
    """管理台数据分析API"""
    return jsonify({
        'success': True,
        'message': '数据分析完成（模拟）',
        'data': {
            'analysis': {
                'forex': {'total_net_flow': 150.5},
                'stock': {'total_net_flow': -45.2},
                'global': {'total_net_flow': 105.3}
            },
            'analysis_period': '30天',
            'timestamp': datetime.now().isoformat()
        }
    })

@app.route('/admin/api/users')
def get_users():
    """获取用户列表API"""
    users = [
        {'username': 'admin', 'role': 'super_admin', 'permissions': ['read', 'write', 'delete', 'admin']},
        {'username': 'manager', 'role': 'manager', 'permissions': ['read', 'write']},
        {'username': 'viewer', 'role': 'viewer', 'permissions': ['read']}
    ]
    
    return jsonify({
        'success': True,
        'data': users
    })

@app.route('/admin/api/logs')
def get_logs():
    """获取系统日志API"""
    logs = [
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 系统启动成功",
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 管理台初始化完成",
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Web服务运行正常"
    ]
    
    return jsonify({
        'success': True,
        'data': {
            'logs': logs,
            'total_lines': len(logs)
        }
    })

@app.route('/admin/api/backup', methods=['POST'])
def backup_database():
    """数据库备份API"""
    return jsonify({
        'success': True,
        'message': '数据库备份完成（模拟）',
        'data': {
            'backup_tables': {'global_flow_data': 'backup_20240101'},
            'timestamp': datetime.now().isoformat()
        }
    })

if __name__ == '__main__':
    print("=" * 60)
    print("全球资金流向分析系统 - 简化版")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("系统正在启动...")
    print()
    print("访问地址:")
    print("- 首页: http://localhost:5003/")
    print("- 仪表盘: http://localhost:5003/dashboard")
    print("- 管理台登录: http://localhost:5003/admin/login")
    print("- 管理台: http://localhost:5003/admin/dashboard")
    print()
    print("演示账户:")
    print("- 管理员: admin / admin123")
    print("- 经理: manager / manager123")
    print("- 查看者: viewer / viewer123")
    print("=" * 60)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5003,
            debug=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n系统已停止")
    except Exception as e:
        print(f"启动失败: {e}") 