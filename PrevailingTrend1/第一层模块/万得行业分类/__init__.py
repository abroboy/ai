"""
万得行业分类模块
负责获取、维护和管理标准化的行业分类数据
为整个大势所趋风险框架提供统一的行业分类基准
"""

__version__ = "1.0.0"
__author__ = "PrevailingTrend Team"

from .core.industry_classifier import IndustryClassifier
from .core.data_collector import DataCollector
from .core.data_validator import DataValidator
from .models.industry_model import IndustryModel
from .utils.config import Config
from .utils.logger import Logger

__all__ = [
    'IndustryClassifier',
    'DataCollector', 
    'DataValidator',
    'IndustryModel',
    'Config',
    'Logger'
] 