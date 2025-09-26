#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
权重影响模拟模块 - 公司排名相关功能
"""

import logging
from datetime import datetime
from .utils import flatten_weights, save_simulation

logger = logging.getLogger('weight_simulator')

def simulate_company_ranking(self, industry_code=None, weight_adjustments=None):
    """
    模拟权重调整对公司排名的影响
    
    参数:
        industry_code: 行业代码，如果为None则模拟所有公司
        weight_adjustments: 权重调整，格式为字典，如 {'fundamental.revenue_growth': 0.2}
        
    返回:
        模拟结果
    """
    try:
        if self.company_data is None:
            raise ValueError("公司数据不可用")
        
        # 复制原始数据
        df = self.company_data.copy()
        
        # 如果指定了行业代码，则筛选该行业的公司
        if industry_code:
            df = df[df['industry_code'] == industry_code]
            
            if len(df) == 0:
                raise ValueError(f"未找到行业代码为 {industry_code} 的公司")
        
        # 获取当前权重
        weights = flatten_weights(self.weight_config)
        
        # 应用权重调整
        if weight_adjustments:
            for key, value in weight_adjustments.items():
                if key in weights:
                    weights[key] = value
        
        # 计算加权得分
        score_columns = [col for col in df.columns if col not in ['company_code', 'company_name', 'industry_code', 'industry_name', 'total_score', 'rank']]
        
        df['total_score'] = 0
        for col in score_columns:
            if col in weights:
                df['total_score'] += df[col] * weights[col]
        
        # 计算排名
        if industry_code:
            # 行业内排名
            df['rank'] = df['total_score'].rank(ascending=False)
        else:
            # 全市场排名
            df['rank'] = df['total_score'].rank(ascending=False)
        
        # 保存模拟结果
        simulation_id = f"company_{industry_code or 'all'}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.simulation_results[simulation_id] = {
            'type': 'company',
            'industry_code': industry_code,
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
        logger.error(f"模拟公司排名失败: {e}")
        raise

def compare_company_simulations(self, simulation_ids):
    """
    比较多个公司模拟结果
    
    参数:
        simulation_ids: 模拟ID列表
        
    返回:
        比较结果
    """
    try:
        results = {}
        base_result = None
        
        for i, sim_id in enumerate(simulation_ids):
            if sim_id not in self.simulation_results:
                # 尝试从文件加载
                from .utils import load_simulation
                sim_result = load_simulation(sim_id, self.data_path)
                if sim_result:
                    self.simulation_results[sim_id] = sim_result
                else:
                    raise ValueError(f"模拟结果不存在: {sim_id}")
            
            sim_result = self.simulation_results[sim_id]
            
            if sim_result['type'] != 'company':
                raise ValueError(f"模拟类型不是公司: {sim_id}")
            
            # 提取结果
            df = pd.DataFrame(sim_result['result'])
            
            if i == 0:
                # 第一个模拟结果作为基准
                base_result = df
                results['base'] = {
                    'id': sim_id,
                    'weights': sim_result['weights'],
                    'adjustments': sim_result['adjustments'],
                    'result': df
                }
            else:
                # 计算排名变化
                merged = pd.merge(
                    base_result[['company_code', 'rank']],
                    df[['company_code', 'rank']],
                    on='company_code',
                    suffixes=('_base', f'_{i}')
                )
                
                merged['rank_change'] = merged[f'rank_{i}'] - merged['rank_base']
                
                results[f'sim_{i}'] = {
                    'id': sim_id,
                    'weights': sim_result['weights'],
                    'adjustments': sim_result['adjustments'],
                    'result': df,
                    'changes': merged
                }
        
        return results
    
    except Exception as e:
        logger.error(f"比较公司模拟结果失败: {e}")
        raise