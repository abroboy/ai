"""
数据库工具类
"""

import pymysql
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from models.international_hotspot_model import INTERNATIONAL_HOTSPOT_TABLE_SQL


class Database:
    """数据库操作类"""
    
    def __init__(self):
        self.config = Config.DATABASE
        self.connection = None
    
    def connect(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                charset=self.config['charset'],
                autocommit=True
            )
            logger.info("数据库连接成功")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("数据库连接已断开")
    
    def create_table(self):
        """创建数据表"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(INTERNATIONAL_HOTSPOT_TABLE_SQL)
                logger.info("国外热点数据表创建成功")
        except Exception as e:
            logger.error(f"创建数据表失败: {e}")
            raise
    
    def insert_hotspot(self, hotspot_data: Dict[str, Any]) -> bool:
        """插入热点数据"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                INSERT INTO international_hotspot_data (
                    hotspot_id, title, content, hotspot_type, region,
                    hotspot_level, status, source, url, publish_time,
                    keywords, related_companies, related_industries,
                    sentiment_score, heat_score, update_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    title = VALUES(title),
                    content = VALUES(content),
                    updated_at = CURRENT_TIMESTAMP
                """
                
                cursor.execute(sql, (
                    hotspot_data['hotspot_id'],
                    hotspot_data['title'],
                    hotspot_data['content'],
                    hotspot_data['hotspot_type'],
                    hotspot_data['region'],
                    hotspot_data['hotspot_level'],
                    hotspot_data['status'],
                    hotspot_data['source'],
                    hotspot_data.get('url'),
                    hotspot_data.get('publish_time'),
                    json.dumps(hotspot_data.get('keywords', [])),
                    json.dumps(hotspot_data.get('related_companies', [])),
                    json.dumps(hotspot_data.get('related_industries', [])),
                    hotspot_data.get('sentiment_score'),
                    hotspot_data.get('heat_score'),
                    datetime.now()
                ))
                
                logger.info(f"热点数据插入成功: {hotspot_data['hotspot_id']}")
                return True
                
        except Exception as e:
            logger.error(f"插入热点数据失败: {e}")
            return False
    
    def get_hotspots(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取热点数据列表"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM international_hotspot_data ORDER BY created_at DESC LIMIT %s"
                cursor.execute(sql, (limit,))
                results = cursor.fetchall()
                
                # 处理JSON字段
                for result in results:
                    if result.get('keywords'):
                        result['keywords'] = json.loads(result['keywords'])
                    if result.get('related_companies'):
                        result['related_companies'] = json.loads(result['related_companies'])
                    if result.get('related_industries'):
                        result['related_industries'] = json.loads(result['related_industries'])
                
                return results
                
        except Exception as e:
            logger.error(f"获取热点数据失败: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计数据"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                stats = {}
                
                # 总数量
                cursor.execute("SELECT COUNT(*) as total FROM international_hotspot_data")
                stats['total'] = cursor.fetchone()['total']
                
                # 按类型统计
                cursor.execute("""
                    SELECT hotspot_type, COUNT(*) as count 
                    FROM international_hotspot_data 
                    GROUP BY hotspot_type
                """)
                stats['by_type'] = {row['hotspot_type']: row['count'] for row in cursor.fetchall()}
                
                return stats
                
        except Exception as e:
            logger.error(f"获取统计数据失败: {e}")
            return {}
    
    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect() 