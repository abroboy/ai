"""
数据模型定义包
包含行业分类相关的数据模型和数据库表结构
"""

from .industry_model import IndustryModel
from .stock_industry_model import StockIndustryModel

__all__ = [
    'IndustryModel',
    'StockIndustryModel'
] 