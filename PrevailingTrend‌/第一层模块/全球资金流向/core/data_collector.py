# -*- coding: utf-8 -*-
"""
全球资金流向数据收集器
"""

import os
import sys
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Optional, Any

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from config import DATA_SOURCES
from utils.logger import LoggerMixin
from utils.database import DatabaseManager
from models.flow_model import GlobalFlowData

class DataCollector(LoggerMixin):
    """全球资金流向数据收集器"""
    
    def __init__(self, db_manager=None):
        """初始化数据收集器"""
        super().__init__()
        self.db_manager = db_manager or DatabaseManager()
        self.session = None
        self.data_sources = DATA_SOURCES
        
    def connect_database(self):
        """连接数据库"""
        if not self.db_manager.connect():
            raise Exception("数据库连接失败")
        self.session = self.db_manager.get_session()
        self.log_info("数据库连接成功")
    
    def collect_forex_data(self) -> List[Dict]:
        """收集外汇数据"""
        self.log_info("开始收集外汇数据")
        
        forex_data = []
        currencies = self.data_sources['forex']['currencies']
        
        try:
            for currency in currencies:
                if currency == 'USD':
                    continue
                
                # 模拟外汇数据
                flow_data = {
                    'timestamp': datetime.now(),
                    'asset_type': 'forex',
                    'asset_name': f'USD/{currency}',
                    'symbol': f'USD{currency}',
                    'close_price': np.random.uniform(0.5, 2.0),
                    'net_flow': np.random.uniform(-5, 5),
                    'flow_ratio': np.random.uniform(-10, 10),
                    'data_source': 'simulated',
                    'region': self._get_currency_region(currency)
                }
                
                forex_data.append(flow_data)
                
        except Exception as e:
            self.log_error(f"收集外汇数据失败: {e}")
        
        self.log_info(f"外汇数据收集完成，共收集 {len(forex_data)} 条记录")
        return forex_data
    
    def collect_stock_market_data(self) -> List[Dict]:
        """收集股票市场数据"""
        self.log_info("开始收集股票市场数据")
        
        stock_data = []
        
        try:
            # 模拟股票市场数据
            markets = ['US', 'Europe', 'Asia']
            symbols = ['^GSPC', '^DJI', '^IXIC', '^N225', '^HSI']
            
            for symbol in symbols:
                for _ in range(5):  # 生成5天的数据
                    flow_data = {
                        'timestamp': datetime.now() - timedelta(days=_),
                        'asset_type': 'stock',
                        'asset_name': f'Market Index {symbol}',
                        'symbol': symbol,
                        'close_price': np.random.uniform(1000, 5000),
                        'volume': np.random.uniform(1000000, 5000000),
                        'net_flow': np.random.uniform(-100, 100),
                        'flow_ratio': np.random.uniform(-5, 5),
                        'data_source': 'simulated',
                        'region': np.random.choice(markets)
                    }
                    
                    stock_data.append(flow_data)
                    
        except Exception as e:
            self.log_error(f"收集股票市场数据失败: {e}")
        
        self.log_info(f"股票市场数据收集完成，共收集 {len(stock_data)} 条记录")
        return stock_data
    
    def collect_all_data(self) -> Dict[str, List[Dict]]:
        """收集所有数据"""
        self.log_info("开始收集所有全球资金流向数据")
        
        all_data = {
            'forex': self.collect_forex_data(),
            'stock': self.collect_stock_market_data(),
            'bond': [],  # 暂时为空
            'commodity': []  # 暂时为空
        }
        
        total_records = sum(len(data) for data in all_data.values())
        self.log_info(f"所有数据收集完成，共收集 {total_records} 条记录")
        
        return all_data
    
    def save_data_to_database(self, data_dict: Dict[str, List[Dict]]):
        """保存数据到数据库"""
        if not self.session:
            self.connect_database()
        
        try:
            total_saved = 0
            
            for asset_type, data_list in data_dict.items():
                for data in data_list:
                    # 创建GlobalFlowData对象
                    flow_data = GlobalFlowData(**data)
                    self.session.add(flow_data)
                    total_saved += 1
            
            self.session.commit()
            self.log_info(f"数据保存成功，共保存 {total_saved} 条记录")
            
        except Exception as e:
            self.session.rollback()
            self.log_error(f"数据保存失败: {e}")
            raise
    
    def _get_currency_region(self, currency: str) -> str:
        """获取货币所属地区"""
        region_map = {
            'EUR': 'Europe', 'GBP': 'Europe', 'CHF': 'Europe',
            'CNY': 'Asia', 'JPY': 'Asia',
            'AUD': 'Oceania', 'CAD': 'North America'
        }
        return region_map.get(currency, 'Global')
    
    def close(self):
        """关闭数据库连接"""
        if self.session:
            self.db_manager.close_session(self.session)
        if self.db_manager:
            self.db_manager.close() 