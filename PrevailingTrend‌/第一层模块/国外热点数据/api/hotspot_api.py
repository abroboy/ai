"""
国外热点数据API接口
"""

from flask import Flask, request, jsonify
import pymysql
import json

class HotspotAPI:
    """热点数据API类"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self._setup_routes()
        
        # 数据库配置
        self.DB_CONFIG = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'rr1234RR',
            'database': 'pt',
            'charset': 'utf8mb4'
        }
    
    def _setup_routes(self):
        """设置路由"""
        
        @self.app.route('/api/hotspots', methods=['GET'])
        def get_hotspots():
            """获取热点数据列表"""
            try:
                limit = request.args.get('limit', 50, type=int)
                hotspots = self._get_hotspots(limit)
                
                result = {
                    'success': True,
                    'data': hotspots,
                    'count': len(hotspots)
                }
                return jsonify(result)
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/statistics', methods=['GET'])
        def get_statistics():
            """获取统计数据"""
            try:
                stats = self._get_statistics()
                result = {
                    'success': True,
                    'data': stats
                }
                return jsonify(result)
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
    
    def _get_db_connection(self):
        """获取数据库连接"""
        try:
            return pymysql.connect(**self.DB_CONFIG)
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return None
    
    def _get_hotspots(self, limit=50):
        """获取热点数据"""
        try:
            connection = self._get_db_connection()
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
    
    def _get_statistics(self):
        """获取统计数据"""
        try:
            connection = self._get_db_connection()
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