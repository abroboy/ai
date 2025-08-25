"""
雪球等论坛热点数据模块
负责收集、分析和处理雪球、东方财富等论坛的热点信息
包括用户讨论、热门话题、情感分析等
"""

__version__ = "1.0.0"
__author__ = "PrevailingTrend Team"

from .core.forum_collector import ForumCollector
from .core.forum_analyzer import ForumAnalyzer
from .core.forum_manager import ForumManager
from .models.forum_model import ForumModel
from .utils.config import Config
from .utils.logger import Logger

__all__ = [
    'ForumCollector',
    'ForumAnalyzer', 
    'ForumManager',
    'ForumModel',
    'Config',
    'Logger'
] 