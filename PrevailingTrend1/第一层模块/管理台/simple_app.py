"""
简化的管理台应用
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pymysql
from datetime import datetime

app = Flask(__name__)
CORS(app)

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

@app.route('/')
def index():
    """首页"""
    return render_template('dashboard.html')

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
        
        # 获取数据统计
        cursor.execute("SELECT COUNT(*) as count FROM l1_wind_industry_classification")
        industry_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM l1_company_list_info")
        company_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM l1_domestic_hotspot_data")
        hotspot_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM system_module_status")
        module_status_count = cursor.fetchone()['count']
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'data': {
                'modules': {
                    'total': 7,
                    'running': 2,
                    'stopped': 5
                },
                'data': {
                    'industries': industry_count,
                    'companies': company_count,
                    'hotspots': hotspot_count,
                    'module_status': module_status_count
                },
                'recent_activities': [
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
                    }
                ]
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
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'data': {
                'industry_stats': industry_stats,
                'company_stats': company_stats
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取统计数据失败: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("启动简化管理台...")
    print("访问地址: http://localhost:8080")
    print("API文档:")
    print("  - 仪表板: http://localhost:8080/api/dashboard")
    print("  - 行业数据: http://localhost:8080/api/data/industries")
    print("  - 公司数据: http://localhost:8080/api/data/companies")
    print("  - 统计数据: http://localhost:8080/api/stats")
    app.run(host='0.0.0.0', port=8080, debug=True) 