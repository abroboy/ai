# -*- coding: utf-8 -*-
"""
全球资金流向数据模型包
"""

from .flow_model import GlobalFlowData, MarketFlowData, AssetFlowData
from .trend_model import FlowTrend, MarketTrend, AssetTrend

__all__ = [
    'GlobalFlowData',
    'MarketFlowData', 
    'AssetFlowData',
    'FlowTrend',
    'MarketTrend',
    'AssetTrend'
] 