# -*- coding: utf-8 -*-
"""
资金流向分析器
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from config import FLOW_ANALYSIS_CONFIG
from utils.logger import LoggerMixin
from utils.database import DatabaseManager
from models.flow_model import GlobalFlowData

class FlowAnalyzer(LoggerMixin):
    """资金流向分析器"""
    
    def __init__(self, db_manager=None):
        """初始化资金流向分析器"""
        super().__init__()
        self.db_manager = db_manager or DatabaseManager()
        self.session = None
        self.config = FLOW_ANALYSIS_CONFIG
        
    def connect_database(self):
        """连接数据库"""
        if not self.db_manager.connect():
            raise Exception("数据库连接失败")
        self.session = self.db_manager.get_session()
        self.log_info("数据库连接成功")
    
    def analyze_global_flow_trends(self, days: int = 30) -> Dict:
        """分析全球资金流向趋势"""
        self.log_info(f"开始分析全球资金流向趋势，时间范围: {days}天")
        
        # 模拟分析结果
        analysis_results = {
            'forex': {
                'total_net_flow': 150.5,
                'avg_flow_ratio': 2.3,
                'flow_trend': 'up',
                'positive_flow_percentage': 65.0
            },
            'stock': {
                'total_net_flow': -45.2,
                'avg_flow_ratio': -1.8,
                'flow_trend': 'down',
                'positive_flow_percentage': 35.0
            },
            'global': {
                'total_net_flow': 105.3,
                'avg_daily_flow': 3.5,
                'flow_trend': 'up',
                'flow_stability': 0.75
            }
        }
        
        self.log_info("全球资金流向趋势分析完成")
        return analysis_results
    
    def analyze_market_flow(self, market_type: str = None, days: int = 30) -> Dict:
        """分析特定市场资金流向"""
        self.log_info(f"开始分析市场资金流向，市场: {market_type}, 时间范围: {days}天")
        
        # 模拟市场分析结果
        market_analysis = {
            'total_net_flow': 85.2,
            'avg_flow_ratio': 1.5,
            'flow_volatility': 12.3,
            'positive_flow_days': 18,
            'negative_flow_days': 12,
            'flow_trend': 'up',
            'top_assets': [
                {'symbol': 'USD', 'net_flow': 25.5},
                {'symbol': 'EUR', 'net_flow': 18.2},
                {'symbol': 'CNY', 'net_flow': 15.8}
            ]
        }
        
        self.log_info(f"市场资金流向分析完成")
        return market_analysis
    
    def analyze_sector_flow(self, sector: str = None, days: int = 30) -> Dict:
        """分析行业/板块资金流向"""
        self.log_info(f"开始分析行业资金流向，行业: {sector}, 时间范围: {days}天")
        
        # 模拟行业分析结果
        sector_analysis = {
            'total_net_flow': 45.8,
            'avg_flow_ratio': 2.1,
            'flow_momentum': 12.5,
            'relative_strength': 65.2,
            'sector_performance': {
                'avg_price_change': 0.025,
                'price_volatility': 0.15,
                'positive_days': 20
            }
        }
        
        self.log_info(f"行业资金流向分析完成")
        return sector_analysis
    
    def close(self):
        """关闭数据库连接"""
        if self.session:
            self.db_manager.close_session(self.session)
        if self.db_manager:
            self.db_manager.close() 