"""
简化的行业分类器
提供基本的行业分类功能
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models.industry_model import IndustryModel
from ..models.stock_industry_model import StockIndustryModel
from ..utils.logger import logger
from ..utils.database import db_manager
from .data_collector import DataCollector
from .simple_validator import SimpleValidator


class SimpleIndustryClassifier:
    """简化的行业分类器"""
    
    def __init__(self):
        self.data_collector = DataCollector()
        self.validator = SimpleValidator()
    
    def initialize_database(self):
        """初始化数据库"""
        try:
            from ..models.industry_model import INDUSTRY_TABLE_SQL
            from ..models.stock_industry_model import STOCK_INDUSTRY_TABLE_SQL
            
            # 创建行业分类表
            if not db_manager.table_exists("wind_industry_classification"):
                db_manager.create_table(INDUSTRY_TABLE_SQL)
                logger.info("行业分类表创建成功")
            
            # 创建股票行业映射表
            if not db_manager.table_exists("stock_industry_mapping"):
                db_manager.create_table(STOCK_INDUSTRY_TABLE_SQL)
                logger.info("股票行业映射表创建成功")
            
            logger.info("数据库初始化完成")
            
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    def collect_and_validate_data(self) -> Dict[str, Any]:
        """采集并验证数据"""
        logger.info("开始采集和验证数据")
        
        # 采集数据
        industry_data = self.data_collector.get_primary_industry_data()
        stock_mapping_data = self.data_collector.get_primary_stock_mapping_data()
        
        # 验证数据
        industry_valid, industry_issues = self.validator.validate_industry_data(industry_data)
        mapping_valid, mapping_issues = self.validator.validate_stock_mapping_data(stock_mapping_data)
        
        return {
            'industry_data': industry_data,
            'stock_mapping_data': stock_mapping_data,
            'industry_valid': industry_valid,
            'mapping_valid': mapping_valid,
            'industry_issues': industry_issues,
            'mapping_issues': mapping_issues
        }
    
    def save_data_to_database(self, industry_data: List[IndustryModel], 
                            stock_mapping_data: List[StockIndustryModel]) -> bool:
        """保存数据到数据库"""
        try:
            logger.info("开始保存数据到数据库")
            
            # 保存行业数据
            industry_dicts = [industry.to_dict() for industry in industry_data]
            db_manager.insert_many("wind_industry_classification", industry_dicts)
            logger.info(f"行业数据保存成功: {len(industry_data)}条")
            
            # 保存股票映射数据
            mapping_dicts = [mapping.to_dict() for mapping in stock_mapping_data]
            db_manager.insert_many("stock_industry_mapping", mapping_dicts)
            logger.info(f"股票映射数据保存成功: {len(stock_mapping_data)}条")
            
            return True
            
        except Exception as e:
            logger.error(f"数据保存失败: {e}")
            return False
    
    def get_industry_by_code(self, industry_code: str) -> Optional[IndustryModel]:
        """根据行业代码获取行业信息"""
        try:
            sql = "SELECT * FROM wind_industry_classification WHERE industry_code = %s"
            result = db_manager.execute_query(sql, (industry_code,))
            
            if result:
                return IndustryModel.from_dict(result[0])
            return None
            
        except Exception as e:
            logger.error(f"获取行业信息失败: {e}")
            return None
    
    def get_industries_by_level(self, level: int) -> List[IndustryModel]:
        """根据层级获取行业列表"""
        try:
            sql = "SELECT * FROM wind_industry_classification WHERE industry_level = %s AND status = 'active'"
            results = db_manager.execute_query(sql, (level,))
            
            return [IndustryModel.from_dict(result) for result in results]
            
        except Exception as e:
            logger.error(f"获取行业列表失败: {e}")
            return []
    
    def search_industries(self, keyword: str) -> List[IndustryModel]:
        """搜索行业"""
        try:
            sql = """
            SELECT * FROM wind_industry_classification 
            WHERE (industry_name LIKE %s OR industry_code LIKE %s) 
            AND status = 'active'
            ORDER BY industry_level, industry_name
            """
            search_pattern = f"%{keyword}%"
            results = db_manager.execute_query(sql, (search_pattern, search_pattern))
            
            return [IndustryModel.from_dict(result) for result in results]
            
        except Exception as e:
            logger.error(f"搜索行业失败: {e}")
            return []
    
    def get_industry_statistics(self) -> Dict[str, Any]:
        """获取行业统计信息"""
        try:
            # 各层级行业数量
            level_stats = {}
            for level in [1, 2, 3]:
                sql = "SELECT COUNT(*) as count FROM wind_industry_classification WHERE industry_level = %s AND status = 'active'"
                result = db_manager.execute_query(sql, (level,))
                level_stats[f'level_{level}'] = result[0]['count']
            
            # 股票映射统计
            sql = "SELECT COUNT(*) as count FROM stock_industry_mapping WHERE status = 'active'"
            result = db_manager.execute_query(sql)
            total_stocks = result[0]['count']
            
            return {
                'industry_levels': level_stats,
                'total_stocks': total_stocks,
                'last_update': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return {}
    
    def run_full_update(self) -> Dict[str, Any]:
        """运行完整的数据更新流程"""
        logger.info("开始运行完整数据更新流程")
        
        try:
            # 1. 初始化数据库
            self.initialize_database()
            
            # 2. 采集并验证数据
            validation_result = self.collect_and_validate_data()
            
            # 3. 检查验证结果
            if not validation_result['industry_valid']:
                logger.error("行业数据验证失败，停止更新")
                return {
                    'success': False,
                    'message': '行业数据验证失败',
                    'issues': validation_result['industry_issues']
                }
            
            # 4. 保存数据到数据库
            save_success = self.save_data_to_database(
                validation_result['industry_data'],
                validation_result['stock_mapping_data']
            )
            
            if not save_success:
                return {
                    'success': False,
                    'message': '数据保存失败'
                }
            
            # 5. 获取统计信息
            statistics = self.get_industry_statistics()
            
            logger.info("完整数据更新流程完成")
            
            return {
                'success': True,
                'message': '数据更新成功',
                'statistics': statistics,
                'industry_count': len(validation_result['industry_data']),
                'stock_count': len(validation_result['stock_mapping_data']),
                'issues': validation_result['industry_issues'] + validation_result['mapping_issues']
            }
            
        except Exception as e:
            logger.error(f"完整数据更新流程失败: {e}")
            return {
                'success': False,
                'message': f'更新流程失败: {str(e)}'
            } 