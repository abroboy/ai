"""
国内热点数据模块
负责收集、分析和处理国内市场的热点信息
包括新闻热点、政策热点、市场热点等
"""

__version__ = "1.0.0"
__author__ = "PrevailingTrend Team"

from .core.hotspot_collector import HotspotCollector
from .core.hotspot_analyzer import HotspotAnalyzer
from .core.hotspot_manager import HotspotManager
from .models.hotspot_model import HotspotModel
from .utils.config import Config
from .utils.logger import Logger

__all__ = [
    'HotspotCollector',
    'HotspotAnalyzer', 
    'HotspotManager',
    'HotspotModel',
    'Config',
    'Logger'
] 