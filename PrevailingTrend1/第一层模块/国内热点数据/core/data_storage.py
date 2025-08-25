"""
数据存储模块
负责将爬取的数据存储到数据库
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from loguru import logger
import pymysql
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus
from utils.database import db_manager


class DataStorage:
    """数据存储类"""
    
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'pt'),
            'charset': 'utf8mb4'
        }
    
    def create_table_if_not_exists(self):
        """创建数据表（如果不存在）"""
        try:
            db_manager.create_tables()
            logger.info("数据表创建成功")
        except Exception as e:
            logger.error(f"创建数据表失败: {e}")
            raise
            
            # 创建热点数据表
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS l1_domestic_hotspot_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hotspot_id VARCHAR(100) UNIQUE NOT NULL,
                title VARCHAR(500) NOT NULL,
                content TEXT,
                hotspot_type VARCHAR(20) NOT NULL,
                hotspot_level VARCHAR(20) NOT NULL,
                status VARCHAR(20) NOT NULL,
                source VARCHAR(100) NOT NULL,
                url VARCHAR(500),
                publish_time DATETIME,
                keywords JSON,
                related_companies JSON,
                related_industries JSON,
                sentiment_score DECIMAL(3,2),
                heat_score DECIMAL(5,2),
                update_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_hotspot_type (hotspot_type),
                INDEX idx_source (source),
                INDEX idx_publish_time (publish_time),
                INDEX idx_heat_score (heat_score),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            cursor.execute(create_table_sql)
            conn.commit()
            logger.info("数据表创建成功")
            
        except Exception as e:
            logger.error(f"创建数据表失败: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def save_hotspots(self, hotspots: List[HotspotModel]) -> int:
        """保存热点数据到数据库"""
        if not hotspots:
            return 0
        
        try:
            saved_count = db_manager.batch_insert_hotspots(hotspots)
            logger.info(f"成功保存 {saved_count} 条热点数据到数据库")
            return saved_count
            
        except Exception as e:
            logger.error(f"保存热点数据到数据库失败: {e}")
            return 0
    
    def get_hotspots_from_db(self, 
                           page: int = 1, 
                           per_page: int = 20,
                           hotspot_type: Optional[str] = None,
                           source: Optional[str] = None,
                           sort_by: str = 'publish_time',
                           sort_order: str = 'desc') -> Dict[str, Any]:
        """从数据库获取热点数据"""
        try:
            # 计算偏移量
            offset = (page - 1) * per_page
            
            # 获取热点数据
            hotspots = db_manager.get_hotspots(
                hotspot_type=hotspot_type,
                source=source,
                sort_by=sort_by,
                sort_order=sort_order,
                limit=per_page,
                offset=offset
            )
            
            # 获取总数（简化处理，实际应该单独查询）
            total = len(hotspots) + offset  # 临时处理
            
            return {
                'hotspots': hotspots,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page,
                'sort_by': sort_by,
                'sort_order': sort_order
            }
            
        except Exception as e:
            logger.error(f"从数据库获取热点数据失败: {e}")
            return {
                'hotspots': [],
                'total': 0,
                'page': page,
                'per_page': per_page,
                'total_pages': 0,
                'sort_by': sort_by,
                'sort_order': sort_order
            }
    
    def get_hotspot_detail(self, hotspot_id: str) -> Optional[HotspotModel]:
        """获取热点详情"""
        try:
            return db_manager.get_hotspot_by_id(hotspot_id)
        except Exception as e:
            logger.error(f"获取热点详情失败: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计数据"""
        try:
            stats = db_manager.get_hotspots_statistics()
            return {
                'total_count': stats.get('total', 0),
                'today_count': 0,  # 临时处理
                'avg_heat': round(float(stats.get('avg_heat_score', 0)), 2),
                'avg_sentiment': round(float(stats.get('avg_sentiment_score', 0)), 2),
                'by_type': stats.get('by_type', {}),
                'by_level': stats.get('by_level', {}),
                'by_status': stats.get('by_status', {}),
                'by_source': stats.get('by_source', {})
            }
        except Exception as e:
            logger.error(f"获取统计数据失败: {e}")
            return {
                'total_count': 0,
                'today_count': 0,
                'avg_heat': 0,
                'avg_sentiment': 0,
                'by_type': {},
                'by_level': {},
                'by_status': {},
                'by_source': {}
            }
    
    def clean_old_data(self, days: int = 30):
        """清理旧数据"""
        try:
            # 简化处理，暂时跳过清理功能
            logger.info(f"清理旧数据功能暂时跳过")
        except Exception as e:
            logger.error(f"清理旧数据失败: {e}")
    
    def _json_encode(self, data) -> str:
        """JSON编码"""
        import json
        if data is None:
            return '[]'
        return json.dumps(data, ensure_ascii=False)
    
    def _json_decode(self, data) -> List:
        """JSON解码"""
        import json
        if not data:
            return []
        try:
            return json.loads(data)
        except:
            return [] 

    def get_industry_rankings(self) -> List[Dict[str, Any]]:
        """获取行业热度排名"""
        try:
            # 从数据库获取行业热度数据
            rankings = db_manager.get_industry_rankings()
            return rankings
        except Exception as e:
            logger.error(f"获取行业热度排名失败: {e}")
            # 返回模拟数据
            return [
                {'industry': '新能源汽车', 'heat_score': 95.2, 'count': 28, 'trend': 'up'},
                {'industry': '人工智能', 'heat_score': 92.8, 'count': 25, 'trend': 'up'},
                {'industry': '芯片产业', 'heat_score': 89.5, 'count': 22, 'trend': 'up'},
                {'industry': '生物医药', 'heat_score': 87.3, 'count': 20, 'trend': 'stable'},
                {'industry': '绿色能源', 'heat_score': 85.1, 'count': 18, 'trend': 'up'},
                {'industry': '数字经济', 'heat_score': 82.7, 'count': 16, 'trend': 'up'},
                {'industry': '智能制造', 'heat_score': 80.4, 'count': 15, 'trend': 'stable'},
                {'industry': '新材料', 'heat_score': 78.2, 'count': 14, 'trend': 'up'},
                {'industry': '高端装备', 'heat_score': 76.9, 'count': 13, 'trend': 'stable'},
                {'industry': '节能环保', 'heat_score': 74.5, 'count': 12, 'trend': 'up'}
            ]
    
    def get_company_rankings(self) -> List[Dict[str, Any]]:
        """获取公司热度排名"""
        try:
            # 从数据库获取公司热度数据
            rankings = db_manager.get_company_rankings()
            return rankings
        except Exception as e:
            logger.error(f"获取公司热度排名失败: {e}")
            # 返回模拟数据
            return [
                {'company': '比亚迪', 'heat_score': 96.8, 'count': 15, 'trend': 'up', 'industry': '新能源汽车'},
                {'company': '华为', 'heat_score': 94.5, 'count': 12, 'trend': 'up', 'industry': '通信设备'},
                {'company': '宁德时代', 'heat_score': 92.3, 'count': 10, 'trend': 'up', 'industry': '新能源'},
                {'company': '腾讯', 'heat_score': 90.1, 'count': 9, 'trend': 'stable', 'industry': '互联网'},
                {'company': '阿里巴巴', 'heat_score': 88.7, 'count': 8, 'trend': 'stable', 'industry': '互联网'},
                {'company': '中芯国际', 'heat_score': 86.4, 'count': 7, 'trend': 'up', 'industry': '芯片'},
                {'company': '恒瑞医药', 'heat_score': 84.2, 'count': 6, 'trend': 'stable', 'industry': '医药'},
                {'company': '隆基绿能', 'heat_score': 82.9, 'count': 6, 'trend': 'up', 'industry': '新能源'},
                {'company': '海康威视', 'heat_score': 80.6, 'count': 5, 'trend': 'stable', 'industry': '安防'},
                {'company': '美的集团', 'heat_score': 78.3, 'count': 5, 'trend': 'stable', 'industry': '家电'}
            ]
    
    def get_trend_rankings(self) -> List[Dict[str, Any]]:
        """获取趋势热度排名"""
        try:
            # 从数据库获取趋势热度数据
            rankings = db_manager.get_trend_rankings()
            return rankings
        except Exception as e:
            logger.error(f"获取趋势热度排名失败: {e}")
            # 返回模拟数据
            return [
                {'trend': '电动化转型', 'heat_score': 95.5, 'count': 30, 'category': '产业趋势'},
                {'trend': '数字化转型', 'heat_score': 93.2, 'count': 28, 'category': '技术趋势'},
                {'trend': '绿色低碳', 'heat_score': 91.8, 'count': 25, 'category': '政策趋势'},
                {'trend': '科技创新', 'heat_score': 89.4, 'count': 22, 'category': '发展趋势'},
                {'trend': '智能制造', 'heat_score': 87.1, 'count': 20, 'category': '产业趋势'},
                {'trend': '消费升级', 'heat_score': 84.7, 'count': 18, 'category': '市场趋势'},
                {'trend': '对外开放', 'heat_score': 82.3, 'count': 16, 'category': '政策趋势'},
                {'trend': '乡村振兴', 'heat_score': 80.0, 'count': 15, 'category': '政策趋势'},
                {'trend': '区域协调', 'heat_score': 77.6, 'count': 14, 'category': '发展趋势'},
                {'trend': '健康中国', 'heat_score': 75.3, 'count': 13, 'category': '民生趋势'}
            ] 