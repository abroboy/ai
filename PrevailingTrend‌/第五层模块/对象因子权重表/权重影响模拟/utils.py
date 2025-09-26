#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
权重影响模拟模块 - 工具函数
"""

import os
import json
import logging

logger = logging.getLogger('weight_simulator')

def flatten_weights(weight_config):
    """
    将嵌套的权重配置展平
    
    参数:
        weight_config: 权重配置
        
    返回:
        展平后的权重字典
    """
    flattened = {}
    
    def _flatten(config, prefix=''):
        for key, value in config.items():
            if isinstance(value, dict):
                _flatten(value, f"{prefix}{key}.")
            else:
                flattened[f"{prefix}{key}"] = value
    
    _flatten(weight_config)
    return flattened

def save_simulation(simulation, simulation_id, data_path):
    """
    保存模拟结果到文件
    
    参数:
        simulation: 模拟结果
        simulation_id: 模拟ID
        data_path: 数据路径
    """
    try:
        # 创建模拟结果目录
        sim_dir = os.path.join(data_path, 'simulations')
        if not os.path.exists(sim_dir):
            os.makedirs(sim_dir)
        
        # 保存模拟结果
        sim_path = os.path.join(sim_dir, f'{simulation_id}.json')
        with open(sim_path, 'w', encoding='utf-8') as f:
            json.dump(simulation, f, indent=2)
        
        logger.info(f"已保存模拟结果: {sim_path}")
    
    except Exception as e:
        logger.error(f"保存模拟结果失败: {e}")
        raise

def load_simulation(simulation_id, data_path):
    """
    从文件加载模拟结果
    
    参数:
        simulation_id: 模拟ID
        data_path: 数据路径
        
    返回:
        模拟结果，如果不存在则返回None
    """
    try:
        # 模拟结果路径
        sim_path = os.path.join(data_path, 'simulations', f'{simulation_id}.json')
        
        if not os.path.exists(sim_path):
            logger.warning(f"模拟结果文件不存在: {sim_path}")
            return None
        
        # 加载模拟结果
        with open(sim_path, 'r', encoding='utf-8') as f:
            simulation = json.load(f)
        
        logger.info(f"已加载模拟结果: {sim_path}")
        return simulation
    
    except Exception as e:
        logger.error(f"加载模拟结果失败: {e}")
        return None

def normalize_weights(weights):
    """
    归一化权重，使其总和为1
    
    参数:
        weights: 权重字典
        
    返回:
        归一化后的权重字典
    """
    total = sum(weights.values())
    
    if total == 0:
        return weights
    
    return {k: v / total for k, v in weights.items()}