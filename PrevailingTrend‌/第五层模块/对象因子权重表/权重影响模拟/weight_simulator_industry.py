#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
权重影响模拟模块 - 行业排名相关功能
"""

import logging
import pandas as pd
from datetime import datetime
from .utils import flatten_weights, save_simulation, load_simulation

logger = logging.getLogger('weight_simulator')

def compare_industry_simulations(self, simulation_ids):
    """
    比较多个行业模拟结果
    
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
                sim_result = load_simulation(sim_id, self.data_path)
                if sim_result:
                    self.simulation_results[sim_id] = sim_result
                else:
                    raise ValueError(f"模拟结果不存在: {sim_id}")
            
            sim_result = self.simulation_results[sim_id]
            
            if sim_result['type'] != 'industry':
                raise ValueError(f"模拟类型不是行业: {sim_id}")
            
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
                    base_result[['industry_code', 'rank']],
                    df[['industry_code', 'rank']],
                    on='industry_code',
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
        logger.error(f"比较行业模拟结果失败: {e}")
        raise

def visualize_industry_ranking(self, simulation_id, top_n=20):
    """
    可视化行业排名
    
    参数:
        simulation_id: 模拟ID
        top_n: 显示前N个行业
        
    返回:
        图表对象
    """
    try:
        if simulation_id not in self.simulation_results:
            # 尝试从文件加载
            sim_result = load_simulation(simulation_id, self.data_path)
            if sim_result:
                self.simulation_results[simulation_id] = sim_result
            else:
                raise ValueError(f"模拟结果不存在: {simulation_id}")
        
        sim_result = self.simulation_results[simulation_id]
        
        if sim_result['type'] != 'industry':
            raise ValueError(f"模拟类型不是行业: {simulation_id}")
        
        # 提取结果
        df = pd.DataFrame(sim_result['result'])
        
        # 取前N个行业
        top_df = df.sort_values('total_score', ascending=False).head(top_n)
        
        # 创建图表
        plt.figure(figsize=(12, 8))
        sns.barplot(x='total_score', y='industry_name', data=top_df)
        plt.title(f'行业排名 (前{top_n}名)')
        plt.xlabel('总分')
        plt.ylabel('行业')
        plt.tight_layout()
        
        # 保存图表
        chart_path = os.path.join(self.data_path, f'industry_ranking_{simulation_id}.png')
        plt.savefig(chart_path)
        
        return plt
    
    except Exception as e:
        logger.error(f"可视化行业排名失败: {e}")
        raise