#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
权重影响模拟模块
提供权重调整对行业和公司排名的影响模拟功能
"""

import os
import json
import logging
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from .utils import flatten_weights, save_simulation, load_simulation

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('weight_simulator')

class WeightSimulator:
    """权重影响模拟类"""
    
    def __init__(self, data_path=None):
        """
        初始化权重影响模拟器
        
        参数:
            data_path: 数据文件路径，如果为None则使用默认路径
        """
        self.data_path = data_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        self.industry_data = None
        self.company_data = None
        self.weight_config = None
        self.simulation_results = {}
        
        # 创建数据目录
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        
        # 加载数据
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        try:
            # 加载行业数据
            industry_path = os.path.join(self.data_path, 'industry_data.csv')
            if os.path.exists(industry_path):
                self.industry_data = pd.read_csv(industry_path)
                logger.info(f"已加载行业数据: {len(self.industry_data)} 条记录")
            else:
                logger.warning(f"行业数据文件不存在: {industry_path}")
            
            # 加载公司数据
            company_path = os.path.join(self.data_path, 'company_data.csv')
            if os.path.exists(company_path):
                self.company_data = pd.read_csv(company_path)
                logger.info(f"已加载公司数据: {len(self.company_data)} 条记录")
            else:
                logger.warning(f"公司数据文件不存在: {company_path}")
            
            # 加载权重配置
            weight_path = os.path.join(self.data_path, 'weight_config.json')
            if os.path.exists(weight_path):
                with open(weight_path, 'r', encoding='utf-8') as f:
                    self.weight_config = json.load(f)
                logger.info(f"已加载权重配置: {len(self.weight_config)} 个因子")
            else:
                logger.warning(f"权重配置文件不存在: {weight_path}")
                # 创建默认权重配置
                self.weight_config = {
                    "fundamental": {
                        "revenue_growth": 0.15,
                        "profit_margin": 0.15,
                        "debt_ratio": 0.10,
                        "cash_flow": 0.10
                    },
                    "market": {
                        "price_momentum": 0.10,
                        "volatility": 0.05,
                        "liquidity": 0.05
                    },
                    "sentiment": {
                        "analyst_rating": 0.10,
                        "social_media": 0.05,
                        "news_sentiment": 0.05
                    },
                    "industry": {
                        "industry_growth": 0.10,
                        "industry_concentration": 0.05
                    }
                }
                
                # 保存默认权重配置
                with open(weight_path, 'w', encoding='utf-8') as f:
                    json.dump(self.weight_config, f, indent=2)
        
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
            raise
    
    def simulate_industry_ranking(self, weight_adjustments=None):
        """
        模拟权重调整对行业排名的影响
        
        参数:
            weight_adjustments: 权重调整，格式为字典，如 {'fundamental.revenue_growth': 0.2}
            
        返回:
            模拟结果
        """
        try:
            if self.industry_data is None:
                raise ValueError("行业数据不可用")
            
            # 复制原始数据
            df = self.industry_data.copy()
            
            # 获取当前权重
            weights = flatten_weights(self.weight_config)
            
            # 应用权重调整
            if weight_adjustments:
                for key, value in weight_adjustments.items():
                    if key in weights:
                        weights[key] = value
            
            # 计算加权得分
            score_columns = [col for col in df.columns if col not in ['industry_code', 'industry_name', 'total_score', 'rank']]
            
            df['total_score'] = 0
            for col in score_columns:
                if col in weights:
                    df['total_score'] += df[col] * weights[col]
            
            # 计算排名
            df['rank'] = df['total_score'].rank(ascending=False)
            
            # 保存模拟结果
            simulation_id = f"industry_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.simulation_results[simulation_id] = {
                'type': 'industry',
                'weights': weights,
                'adjustments': weight_adjustments,
                'result': df.sort_values('rank').to_dict('records')
            }
            
            # 保存到文件
            save_simulation(self.simulation_results[simulation_id], simulation_id, self.data_path)
            
            return {
                'simulation_id': simulation_id,
                'result': df.sort_values('rank')
            }
        
        except Exception as e:
            logger.error(f"模拟行业排名失败: {e}")
            raise