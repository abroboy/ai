"""
公司名字列表模块
负责收集、整理和维护所有目标公司的基本信息
为整个大势所趋风险框架提供标准化的公司信息基础
"""

__version__ = "1.0.0"
__author__ = "PrevailingTrend Team"

from .core.company_collector import CompanyCollector
from .core.company_validator import CompanyValidator
from .core.company_manager import CompanyManager
from .models.company_model import CompanyModel
from .utils.config import Config
from .utils.logger import Logger

__all__ = [
    'CompanyCollector',
    'CompanyValidator', 
    'CompanyManager',
    'CompanyModel',
    'Config',
    'Logger'
] 