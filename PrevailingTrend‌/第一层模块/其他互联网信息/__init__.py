"""
其他互联网信息模块
负责收集、分析和处理其他互联网信息源的数据
包括社交媒体、博客、新闻网站等
"""

__version__ = "1.0.0"
__author__ = "PrevailingTrend Team"

from .core.internet_collector import InternetCollector
from .core.internet_analyzer import InternetAnalyzer
from .core.internet_manager import InternetManager
from .models.internet_model import InternetModel
from .utils.config import Config
from .utils.logger import Logger

__all__ = [
    'InternetCollector',
    'InternetAnalyzer', 
    'InternetManager',
    'InternetModel',
    'Config',
    'Logger'
] 