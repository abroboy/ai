# -*- coding: utf-8 -*-
"""
管理台应用
"""

import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from .auth import admin_auth
from utils.logger import setup_logger
from utils.database import DatabaseManager
from core.data_collector import DataCollector
from core.flow_analyzer import FlowAnalyzer

# 创建管理台Flask应用
admin_app = Flask(__name__)
admin_app.secret_key = os.getenv('SECRET_KEY', 'admin-secret-key')
CORS(admin_app)

# 设置日志
logger = setup_logger('admin_console')

# 初始化组件
db_manager = DatabaseManager()
data_collector = DataCollector(db_manager)
flow_analyzer = FlowAnalyzer(db_manager)

@admin_app.route('/admin/login')
def admin_login_page():
    """管理台登录页面"""
    return render_template('admin/login.html')

@admin_app.route('/admin/dashboard')
def admin_dashboard():
    """管理台仪表盘"""
    return render_template('admin/dashboard.html')

@admin_app.route('/admin/api/login', methods=['POST'])
def admin_login():
    """管理台登录API"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
        
        if admin_auth.verify_password(username, password):
            token = admin_auth.generate_token(username)
            user_info = admin_auth.admin_users[username]
            
            return jsonify({
                'success': True,
                'message': '登录成功',
                'data': {
                    'token': token,
                    'user': {
                        'username': username,
                        'role': user_info['role'],
                        'permissions': user_info['permissions']
                    }
                }
            })
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
            
    except Exception as e:
        logger.error(f"登录失败: {e}")
        return jsonify({'success': False, 'message': '登录失败'}), 500

@admin_app.route('/admin/api/logout', methods=['POST'])
@admin_auth.require_auth
def admin_logout():
    """管理台登出API"""
    return jsonify({'success': True, 'message': '登出成功'})

@admin_app.route('/admin/api/system_status')
@admin_auth.require_auth
def system_status():
    """系统状态API"""
    try:
        # 获取数据库状态
        db_stats = db_manager.get_database_stats()
        
        # 获取系统信息
        system_info = {
            'database_tables': len(db_stats),
            'total_records': sum(stats['rows'] for stats in db_stats.values()),
            'database_size': sum(stats['data_size_mb'] for stats in db_stats.values()),
            'last_update': datetime.now().isoformat(),
            'system_status': 'running'
        }
        
        return jsonify({
            'success': True,
            'data': system_info
        })
        
    except Exception as e:
        logger.error(f"获取系统状态失败: {e}")
        return jsonify({'success': False, 'message': '获取系统状态失败'}), 500

@admin_app.route('/admin/api/collect_data', methods=['POST'])
@admin_auth.require_auth
@admin_auth.require_permission('write')
def admin_collect_data():
    """管理台数据收集API"""
    try:
        logger.info("管理台触发数据收集")
        
        # 收集数据
        all_data = data_collector.collect_all_data()
        
        # 保存到数据库
        data_collector.save_data_to_database(all_data)
        
        total_records = sum(len(data) for data in all_data.values())
        
        return jsonify({
            'success': True,
            'message': '数据收集成功',
            'data': {
                'total_records': total_records,
                'asset_types': list(all_data.keys()),
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"数据收集失败: {e}")
        return jsonify({'success': False, 'message': f'数据收集失败: {str(e)}'}), 500

@admin_app.route('/admin/api/analyze_data', methods=['POST'])
@admin_auth.require_auth
@admin_auth.require_permission('read')
def admin_analyze_data():
    """管理台数据分析API"""
    try:
        data = request.get_json()
        days = data.get('days', 30)
        
        # 分析数据
        global_analysis = flow_analyzer.analyze_global_flow_trends(days)
        
        return jsonify({
            'success': True,
            'message': '数据分析完成',
            'data': {
                'analysis': global_analysis,
                'analysis_period': f'{days}天',
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"数据分析失败: {e}")
        return jsonify({'success': False, 'message': f'数据分析失败: {str(e)}'}), 500

@admin_app.route('/admin/api/users')
@admin_auth.require_auth
@admin_auth.require_permission('admin')
def get_users():
    """获取用户列表API"""
    try:
        users = []
        for username, user_info in admin_auth.admin_users.items():
            users.append({
                'username': username,
                'role': user_info['role'],
                'permissions': user_info['permissions']
            })
        
        return jsonify({
            'success': True,
            'data': users
        })
        
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        return jsonify({'success': False, 'message': '获取用户列表失败'}), 500

@admin_app.route('/admin/api/logs')
@admin_auth.require_auth
@admin_auth.require_permission('read')
def get_logs():
    """获取系统日志API"""
    try:
        log_file = 'logs/global_flow_analysis.log'
        logs = []
        
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                # 获取最后100行日志
                lines = f.readlines()[-100:]
                for line in lines:
                    logs.append(line.strip())
        
        return jsonify({
            'success': True,
            'data': {
                'logs': logs,
                'total_lines': len(logs)
            }
        })
        
    except Exception as e:
        logger.error(f"获取日志失败: {e}")
        return jsonify({'success': False, 'message': '获取日志失败'}), 500

@admin_app.route('/admin/api/backup', methods=['POST'])
@admin_auth.require_auth
@admin_auth.require_permission('admin')
def backup_database():
    """数据库备份API"""
    try:
        # 备份主要数据表
        tables = ['global_flow_data', 'market_flow_data', 'asset_flow_data']
        backup_results = {}
        
        for table in tables:
            if db_manager.check_table_exists(table):
                backup_table = db_manager.backup_table(table)
                backup_results[table] = backup_table
        
        return jsonify({
            'success': True,
            'message': '数据库备份完成',
            'data': {
                'backup_tables': backup_results,
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"数据库备份失败: {e}")
        return jsonify({'success': False, 'message': f'数据库备份失败: {str(e)}'}), 500

if __name__ == '__main__':
    admin_app.run(host='0.0.0.0', port=5004, debug=True) 