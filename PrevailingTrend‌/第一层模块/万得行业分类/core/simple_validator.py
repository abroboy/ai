"""
简化的数据验证器
提供基本的数据验证功能
"""

from typing import List, Tuple
from ..models.industry_model import IndustryModel
from ..models.stock_industry_model import StockIndustryModel
from ..utils.logger import logger


class SimpleValidator:
    """简化的数据验证器"""
    
    def validate_industry_data(self, industries: List[IndustryModel]) -> Tuple[bool, List[str]]:
        """验证行业数据"""
        errors = []
        warnings = []
        
        logger.info(f"验证行业数据: {len(industries)}条")
        
        for i, industry in enumerate(industries):
            # 基本验证
            if not industry.industry_code:
                errors.append(f"第{i+1}条: 行业代码为空")
            
            if not industry.industry_name:
                errors.append(f"第{i+1}条: 行业名称为空")
            
            if industry.industry_level not in [1, 2, 3]:
                errors.append(f"第{i+1}条: 无效层级 {industry.industry_level}")
        
        # 数据量检查
        if len(industries) < 10:
            warnings.append("行业数据量较少")
        
        is_valid = len(errors) == 0
        logger.info(f"行业数据验证: {'通过' if is_valid else '失败'}")
        
        return is_valid, errors + warnings
    
    def validate_stock_mapping_data(self, mappings: List[StockIndustryModel]) -> Tuple[bool, List[str]]:
        """验证股票映射数据"""
        errors = []
        warnings = []
        
        logger.info(f"验证股票映射数据: {len(mappings)}条")
        
        for i, mapping in enumerate(mappings):
            # 基本验证
            if not mapping.stock_code:
                errors.append(f"第{i+1}条: 股票代码为空")
            
            if not mapping.stock_name:
                errors.append(f"第{i+1}条: 股票名称为空")
            
            if not mapping.industry_name:
                errors.append(f"第{i+1}条: 行业名称为空")
            
            if not 0 <= mapping.confidence <= 1:
                errors.append(f"第{i+1}条: 置信度超出范围 {mapping.confidence}")
        
        # 数据量检查
        if len(mappings) < 50:
            warnings.append("股票映射数据量较少")
        
        is_valid = len(errors) == 0
        logger.info(f"股票映射数据验证: {'通过' if is_valid else '失败'}")
        
        return is_valid, errors + warnings 