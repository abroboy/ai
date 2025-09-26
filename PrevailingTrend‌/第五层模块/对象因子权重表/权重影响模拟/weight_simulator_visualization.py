#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
权重影响模拟模块 - 可视化功能
"""

import os
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from .utils import load_simulation

logger = logging.getLogger('weight_simulator')

def visualize_company_ranking(self, simulation_id, industry_code=None, top_n=20):
    """
    可视化公司排名
    
    参数:
        simulation_id: 模拟ID
        industry_code: 行业代码，如果为None则显示所有公司
        top_n: 显示前N个公司
        
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
        
        if sim_result['type'] != 'company':
            raise ValueError(f"模拟类型不是公司: {simulation_id}")
        
        # 提取结果
        df = pd.DataFrame(sim_result['result'])
        
        # 如果指定了行业代码，则筛选该行业的公司
        if industry_code:
            df = df[df['industry_code'] == industry_code]
            
            if len(df) == 0:
                raise ValueError(f"未找到行业代码为 {industry_code} 的公司")
        
        # 取前N个公司
        top_df = df.sort_values('total_score', ascending=False).head(top_n)
        
        # 创建图表
        plt.figure(figsize=(12, 8))
        sns.barplot(x='total_score', y='company_name', data=top_df)
        plt.title(f'公司排名 (前{top_n}名)')
        plt.xlabel('总分')
        plt.ylabel('公司')
        plt.tight_layout()
        
        # 保存图表
        chart_path = os.path.join(self.data_path, f'company_ranking_{simulation_id}.png')
        plt.savefig(chart_path)
        
        return plt
    
    except Exception as e:
        logger.error(f"可视化公司排名失败: {e}")
        raise

def visualize_weight_impact(self, simulation_ids, entity_code, is_industry=False):
    """
    可视化权重调整对特定行业或公司的影响
    
    参数:
        simulation_ids: 模拟ID列表
        entity_code: 行业代码或公司代码
        is_industry: 是否为行业
        
    返回:
        图表对象
    """
    try:
        results = []
        labels = []
        
        for i, sim_id in enumerate(simulation_ids):
            if sim_id not in self.simulation_results:
                # 尝试从文件加载
                sim_result = load_simulation(sim_id, self.data_path)
                if sim_result:
                    self.simulation_results[sim_id] = sim_result
                else:
                    raise ValueError(f"模拟结果不存在: {sim_id}")
            
            sim_result = self.simulation_results[sim_id]
            
            # 检查模拟类型
            if is_industry and sim_result['type'] != 'industry':
                raise ValueError(f"模拟类型不是行业: {sim_id}")
            elif not is_industry and sim_result['type'] != 'company':
                raise ValueError(f"模拟类型不是公司: {sim_id}")
            
            # 提取结果
            df = pd.DataFrame(sim_result['result'])
            
            # 查找特定实体
            if is_industry:
                entity = df[df['industry_code'] == entity_code]
                if len(entity) == 0:
                    raise ValueError(f"未找到行业代码为 {entity_code} 的行业")
                entity_name = entity['industry_name'].iloc[0]
            else:
                entity = df[df['company_code'] == entity_code]
                if len(entity) == 0:
                    raise ValueError(f"未找到公司代码为 {entity_code} 的公司")
                entity_name = entity['company_name'].iloc[0]
            
            # 提取得分和排名
            score = entity['total_score'].iloc[0]
            rank = entity['rank'].iloc[0]
            
            results.append({
                'simulation_id': sim_id,
                'score': score,
                'rank': rank
            })
            
            # 生成标签
            if i == 0:
                labels.append('基准')
            else:
                # 提取权重调整
                adjustments = sim_result['adjustments']
                if adjustments:
                    adj_str = ', '.join([f"{k.split('.')[-1]}:{v:.2f}" for k, v in adjustments.items()])
                    labels.append(f"调整 {i}: {adj_str}")
                else:
                    labels.append(f"调整 {i}")
        
        # 创建图表
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 得分图表
        scores = [r['score'] for r in results]
        ax1.bar(labels, scores)
        ax1.set_title(f"{entity_name} 得分比较")
        ax1.set_ylabel('得分')
        ax1.tick_params(axis='x', rotation=45)
        
        # 排名图表
        ranks = [r['rank'] for r in results]
        ax2.bar(labels, ranks)
        ax2.set_title(f"{entity_name} 排名比较")
        ax2.set_ylabel('排名')
        ax2.tick_params(axis='x', rotation=45)
        ax2.invert_yaxis()  # 排名越小越好
        
        plt.tight_layout()
        
        # 保存图表
        entity_type = 'industry' if is_industry else 'company'
        chart_path = os.path.join(self.data_path, f'{entity_type}_impact_{entity_code}.png')
        plt.savefig(chart_path)
        
        return plt
    
    except Exception as e:
        logger.error(f"可视化权重影响失败: {e}")
        raise