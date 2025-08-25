"""
公司名字列表模块
负责收集、整理和维护所有目标公司的基本信息
"""

__version__ = "1.0.0"
__author__ = "PrevailingTrend Team"

from .models.company_model import CompanyModel, CompanyStatus, CompanyType
from .core.company_collector import CompanyCollector
from .core.company_manager import CompanyManager

__all__ = [
    'CompanyModel',
    'CompanyStatus', 
    'CompanyType',
    'CompanyCollector',
    'CompanyManager'
] 