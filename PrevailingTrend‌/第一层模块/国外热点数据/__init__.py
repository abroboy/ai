"""
国外热点数据模块
负责收集、分析和处理国外市场的热点信息
包括国际新闻、政策变化、市场动态等
"""

__version__ = "1.0.0"
__author__ = "PrevailingTrend Team"

from .core.international_hotspot_collector import InternationalHotspotCollector
from .core.international_hotspot_analyzer import InternationalHotspotAnalyzer
from .core.international_hotspot_manager import InternationalHotspotManager
from .models.international_hotspot_model import InternationalHotspotModel
from .config import Config
from .utils.logger import Logger

__all__ = [
    'InternationalHotspotCollector',
    'InternationalHotspotAnalyzer', 
    'InternationalHotspotManager',
    'InternationalHotspotModel',
    'Config',
    'Logger'
] 