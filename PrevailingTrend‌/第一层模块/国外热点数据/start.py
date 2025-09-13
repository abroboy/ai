"""
国外热点数据管理台启动脚本
按照最新规范：127.0.0.1:5004只做国外热点数据的数据展示，不涉及数据拉取
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
import time

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='国外热点数据管理台')
    parser.add_argument('--host', default='127.0.0.1', help='服务主机地址')
    parser.add_argument('--port', type=int, default=5004, help='服务端口')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    
    args = parser.parse_args()
    
    try:
        # 检查templates目录
        templates_dir = Path(__file__).parent / 'templates'
        if not templates_dir.exists():
            print(f"创建templates目录: {templates_dir}")
            templates_dir.mkdir(parents=True, exist_ok=True)
        
        # 启动管理台
        print(f"启动国外热点数据管理台...")
        print(f"访问地址: http://{args.host}:{args.port}")
        print("按 Ctrl+C 停止服务")
        
        # 直接启动Flask应用
        from flask import Flask, render_template, jsonify, request
        from flask_cors import CORS
        import pymysql
        import json
        
        app = Flask(__name__, static_folder='static')
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
                return pymysql.connect(**DB_CONFIG)
            except Exception as e:
                print(f"数据库连接失败: {e}")
                return None
        
        def get_statistics():
            """获取统计信息"""
            try:
                connection = get_db_connection()
                if not connection:
                    return None
                
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                
                cursor.execute("""
                    SELECT 
                        (SELECT COUNT(*) FROM international_hotspot_data) as total_hotspots,
                        (SELECT COUNT(*) FROM international_hotspot_data WHERE hotspot_type = 'news') as news_count,
                        (SELECT COUNT(*) FROM international_hotspot_data WHERE hotspot_type = 'policy') as policy_count,
                        (SELECT COUNT(*) FROM international_hotspot_data WHERE region = 'global') as global_count,
                        (SELECT COUNT(*) FROM international_hotspot_data WHERE region = 'us') as us_count
                """)
                
                stats = cursor.fetchone()
                connection.close()
                return stats
                
            except Exception as e:
                print(f"获取统计信息失败: {e}")
                return None
        
        def get_hotspots(limit=50):
            """获取热点数据"""
            try:
                connection = get_db_connection()
                if not connection:
                    return []
                
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                cursor.execute("""
                    SELECT * FROM international_hotspot_data 
                    ORDER BY created_at DESC 
                    LIMIT %s
                """, (limit,))
                
                hotspots = cursor.fetchall()
                connection.close()
                return hotspots
                
            except Exception as e:
                print(f"获取热点数据失败: {e}")
                return []
        
        # 路由定义
        @app.route('/')
        def index():
            """首页"""
            return render_template('index.html')
        
        @app.route('/dashboard')
        def dashboard():
            """仪表盘"""
            return render_template('dashboard.html')
        
        @app.route('/api/health')
        def health_check():
            """健康检查"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'service': 'International Hotspot Data Service',
                'port': args.port
            })
        
        @app.route('/api/statistics')
        def api_get_statistics():
            """获取统计数据"""
            stats = get_statistics()
            if stats:
                return jsonify({
                    'success': True,
                    'data': stats
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '获取统计数据失败'
                }), 500
        
        @app.route('/api/hotspots')
        def api_get_hotspots():
            """获取热点数据API"""
            try:
                limit = request.args.get('limit', 50, type=int)
                hotspots = get_hotspots(limit)
                
                return jsonify({
                    'success': True,
                    'data': hotspots,
                    'count': len(hotspots)
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        # 启动应用
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug
        )
        
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == '__main__':
    main() 