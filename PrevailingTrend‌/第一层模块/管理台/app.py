"""
第一层模块管理台
提供Web界面来管理和查看各个模块的数据
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
import json
import os
import sys
import pymysql
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

# 配置
app.config['SECRET_KEY'] = 'prevailing_trend_admin_2025'
app.config['DEBUG'] = True

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

class ModuleManager:
    """模块管理器"""
    
    def __init__(self):
        self.modules = {
            'wind_industry': {
                'name': '万得行业分类',
                'path': '../万得行业分类',
                'status': 'running',
                'description': '行业分类数据管理',
                'endpoints': [
                    {'name': '行业列表', 'url': '/api/industries'},
                    {'name': '股票映射', 'url': '/api/stocks'},
                    {'name': '数据统计', 'url': '/api/stats'}
                ]
            },
            'company_list': {
                'name': '公司名字列表',
                'path': '../公司名字列表',
                'status': 'running',
                'description': '公司基础信息管理',
                'endpoints': [
                    {'name': '公司列表', 'url': '/api/companies'},
                    {'name': '市场分类', 'url': '/api/markets'},
                    {'name': '数据统计', 'url': '/api/stats'}
                ]
            },
            'domestic_hotspot': {
                'name': '国内热点数据',
                'path': '../国内热点数据',
                'status': 'stopped',
                'description': '国内热点信息采集',
                'endpoints': [
                    {'name': '热点列表', 'url': '/api/hotspots'},
                    {'name': '热度排行', 'url': '/api/ranking'},
                    {'name': '情感分析', 'url': '/api/sentiment'}
                ]
            },
            'foreign_hotspot': {
                'name': '国外热点数据',
                'path': '../国外热点数据',
                'status': 'stopped',
                'description': '国外热点信息采集',
                'endpoints': [
                    {'name': '热点列表', 'url': '/api/hotspots'},
                    {'name': '热度排行', 'url': '/api/ranking'},
                    {'name': '情感分析', 'url': '/api/sentiment'}
                ]
            },
            'tencent_index': {
                'name': '腾讯济安指数',
                'path': '../腾讯济安指数',
                'status': 'stopped',
                'description': '腾讯济安指数数据',
                'endpoints': [
                    {'name': '指数数据', 'url': '/api/indices'},
                    {'name': '历史数据', 'url': '/api/history'},
                    {'name': '趋势分析', 'url': '/api/trends'}
                ]
            },
            'forum_hotspot': {
                'name': '雪球等论坛热点数据',
                'path': '../雪球等论坛热点数据',
                'status': 'stopped',
                'description': '论坛热点信息采集',
                'endpoints': [
                    {'name': '论坛列表', 'url': '/api/forums'},
                    {'name': '热点话题', 'url': '/api/topics'},
                    {'name': '用户活跃度', 'url': '/api/activity'}
                ]
            },
            'internet_info': {
                'name': '其他互联网信息',
                'path': '../其他互联网信息',
                'status': 'stopped',
                'description': '其他互联网信息采集',
                'endpoints': [
                    {'name': '信息列表', 'url': '/api/info'},
                    {'name': '分类统计', 'url': '/api/categories'},
                    {'name': '数据质量', 'url': '/api/quality'}
                ]
            }
        }
    
    def get_modules(self):
        """获取所有模块信息"""
        return self.modules
    
    def get_module(self, module_id):
        """获取指定模块信息"""
        return self.modules.get(module_id)
    
    def update_module_status(self, module_id, status):
        """更新模块状态"""
        if module_id in self.modules:
            self.modules[module_id]['status'] = status
            return True
        return False

# 创建模块管理器实例
module_manager = ModuleManager()

@app.route('/')
def index():
    """管理台首页"""
    return render_template('index.html', modules=module_manager.get_modules())

@app.route('/api/modules')
def get_modules():
    """获取所有模块信息"""
    return jsonify({
        'success': True,
        'data': module_manager.get_modules(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/modules/<module_id>')
def get_module(module_id):
    """获取指定模块信息"""
    module = module_manager.get_module(module_id)
    if module:
        return jsonify({
            'success': True,
            'data': module,
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({
            'success': False,
            'message': '模块不存在'
        }), 404

@app.route('/api/modules/<module_id>/status', methods=['POST'])
def update_module_status(module_id):
    """更新模块状态"""
    data = request.get_json()
    status = data.get('status', 'stopped')
    
    if module_manager.update_module_status(module_id, status):
        return jsonify({
            'success': True,
            'message': f'模块状态已更新为 {status}',
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({
            'success': False,
            'message': '模块不存在'
        }), 404

@app.route('/api/dashboard')
def dashboard():
    """仪表板数据"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({
                'success': False,
                'message': '数据库连接失败'
            }), 500
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 获取模块统计
        modules = module_manager.get_modules()
        total_modules = len(modules)
        running_modules = sum(1 for m in modules.values() if m['status'] == 'running')
        stopped_modules = total_modules - running_modules
        
        # 获取数据统计
        cursor.execute("SELECT COUNT(*) as count FROM l1_wind_industry_classification")
        industry_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM l1_company_list_info")
        company_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM l1_domestic_hotspot_data")
        hotspot_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM system_module_status")
        module_status_count = cursor.fetchone()['count']
        
        # 获取最近活动
        recent_activities = [
            {
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'module': '万得行业分类',
                'action': '数据更新',
                'status': 'success',
                'details': f'更新了 {industry_count} 条行业数据'
            },
            {
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'module': '公司名字列表',
                'action': '数据验证',
                'status': 'success',
                'details': f'验证了 {company_count} 条公司数据'
            },
            {
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'module': '国内热点数据',
                'action': '数据采集',
                'status': 'success',
                'details': f'采集了 {hotspot_count} 条热点数据'
            }
        ]
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'data': {
                'modules': {
                    'total': total_modules,
                    'running': running_modules,
                    'stopped': stopped_modules
                },
                'data': {
                    'industries': industry_count,
                    'companies': company_count,
                    'hotspots': hotspot_count,
                    'module_status': module_status_count
                },
                'recent_activities': recent_activities
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取仪表板数据失败: {str(e)}'
        }), 500

@app.route('/api/data/<data_type>')
def get_data(data_type):
    """获取指定类型的数据"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({
                'success': False,
                'message': '数据库连接失败'
            }), 500
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        if data_type == 'industries':
            cursor.execute("SELECT * FROM l1_wind_industry_classification ORDER BY industry_code LIMIT 20")
            data = cursor.fetchall()
            
        elif data_type == 'companies':
            cursor.execute("SELECT * FROM l1_company_list_info ORDER BY stock_code LIMIT 20")
            data = cursor.fetchall()
            
        elif data_type == 'hotspots':
            cursor.execute("SELECT * FROM l1_domestic_hotspot_data ORDER BY update_date DESC LIMIT 20")
            data = cursor.fetchall()
            
        elif data_type == 'module_status':
            cursor.execute("SELECT * FROM system_module_status ORDER BY updated_at DESC LIMIT 20")
            data = cursor.fetchall()
            
        else:
            return jsonify({
                'success': False,
                'message': '不支持的数据类型'
            }), 400
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取数据失败: {str(e)}'
        }), 500

@app.route('/api/stats')
def get_stats():
    """获取统计数据"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({
                'success': False,
                'message': '数据库连接失败'
            }), 500
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 行业统计
        cursor.execute("SELECT industry_level, COUNT(*) as count FROM l1_wind_industry_classification GROUP BY industry_level")
        industry_stats = cursor.fetchall()
        
        # 公司统计
        cursor.execute("SELECT market, COUNT(*) as count FROM l1_company_list_info GROUP BY market")
        company_stats = cursor.fetchall()
        
        # 热点统计
        cursor.execute("SELECT hotspot_type, COUNT(*) as count FROM l1_domestic_hotspot_data GROUP BY hotspot_type")
        hotspot_stats = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'data': {
                'industry_stats': industry_stats,
                'company_stats': company_stats,
                'hotspot_stats': hotspot_stats
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取统计数据失败: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("启动第一层模块管理台...")
    print("访问地址: http://localhost:8080")
    print("API文档: http://localhost:8080/api/modules")
    app.run(host='0.0.0.0', port=8080, debug=True) 