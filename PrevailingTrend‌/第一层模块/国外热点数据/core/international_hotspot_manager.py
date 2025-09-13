"""
国外热点数据管理器
"""

from typing import List, Dict, Any
from loguru import logger
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import Database
from utils.logger import Logger
from core.international_hotspot_collector import InternationalHotspotCollector
from core.international_hotspot_analyzer import InternationalHotspotAnalyzer


class InternationalHotspotManager:
    """国外热点数据管理器"""
    
    def __init__(self):
        # 初始化日志
        Logger.setup()
        self.logger = Logger.get_logger('InternationalHotspotManager')
        
        # 初始化组件
        self.collector = InternationalHotspotCollector()
        self.analyzer = InternationalHotspotAnalyzer()
        self.database = Database()
    
    def run_collection(self) -> bool:
        """运行数据收集流程"""
        try:
            self.logger.info("开始运行国外热点数据收集流程")
            
            # 1. 收集数据
            self.logger.info("步骤1: 开始收集数据")
            hotspots = self.collector.collect_all()
            
            if not hotspots:
                self.logger.warning("未收集到任何数据")
                return False
            
            # 2. 分析数据
            self.logger.info("步骤2: 开始分析数据")
            analyzed_hotspots = self.analyzer.analyze_hotspots(hotspots)
            
            # 3. 存储数据
            self.logger.info("步骤3: 开始存储数据")
            with self.database as db:
                # 创建数据表（如果不存在）
                db.create_table()
                
                # 批量插入数据
                success_count = 0
                for hotspot in analyzed_hotspots:
                    if db.insert_hotspot(hotspot):
                        success_count += 1
                
                self.logger.info(f"数据存储完成，成功: {success_count}/{len(analyzed_hotspots)}")
            
            self.logger.info("国外热点数据收集流程完成")
            return True
            
        except Exception as e:
            self.logger.error(f"运行数据收集流程失败: {e}")
            return False
    
    def get_hotspots(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取热点数据"""
        try:
            with self.database as db:
                return db.get_hotspots(limit)
        except Exception as e:
            self.logger.error(f"获取热点数据失败: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计数据"""
        try:
            with self.database as db:
                return db.get_statistics()
        except Exception as e:
            self.logger.error(f"获取统计数据失败: {e}")
            return {}
    
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            with self.database as db:
                db.create_table()
                self.logger.info("数据库连接测试成功")
                return True
        except Exception as e:
            self.logger.error(f"数据库连接测试失败: {e}")
            return False
    
    def run_test_collection(self) -> bool:
        """运行测试数据收集"""
        try:
            self.logger.info("开始运行测试数据收集")
            
            # 创建测试数据
            test_hotspots = [
                {
                    'hotspot_id': 'test_001',
                    'title': 'Global Markets React to Federal Reserve Policy Changes',
                    'content': 'International markets showed mixed reactions to the latest Federal Reserve policy announcement, with technology stocks leading gains while financial sectors faced pressure.',
                    'hotspot_type': 'news',
                    'region': 'global',
                    'hotspot_level': 'medium',
                    'status': 'active',
                    'source': 'Test Source',
                    'url': 'https://example.com/test1',
                    'publish_time': None,
                    'keywords': [],
                    'related_companies': [],
                    'related_industries': [],
                    'sentiment_score': None,
                    'heat_score': None
                },
                {
                    'hotspot_id': 'test_002',
                    'title': 'European Union Announces New Digital Economy Regulations',
                    'content': 'The European Union has introduced comprehensive new regulations for the digital economy, affecting major technology companies and digital services across the region.',
                    'hotspot_type': 'policy',
                    'region': 'eu',
                    'hotspot_level': 'high',
                    'status': 'active',
                    'source': 'Test Source',
                    'url': 'https://example.com/test2',
                    'publish_time': None,
                    'keywords': [],
                    'related_companies': [],
                    'related_industries': [],
                    'sentiment_score': None,
                    'heat_score': None
                }
            ]
            
            # 分析测试数据
            analyzed_hotspots = self.analyzer.analyze_hotspots(test_hotspots)
            
            # 存储测试数据
            with self.database as db:
                db.create_table()
                
                success_count = 0
                for hotspot in analyzed_hotspots:
                    if db.insert_hotspot(hotspot):
                        success_count += 1
                
                self.logger.info(f"测试数据存储完成，成功: {success_count}/{len(analyzed_hotspots)}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"运行测试数据收集失败: {e}")
            return False 