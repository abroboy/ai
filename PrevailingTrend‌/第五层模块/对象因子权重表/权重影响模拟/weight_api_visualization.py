#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
权重影响模拟模块 - 可视化API接口
"""

import logging
from flask import request, jsonify, send_file
import os

logger = logging.getLogger('weight_api')

def register_visualization_routes(app, simulator):
    """注册可视化相关路由"""
    
    @app.route('/api/visualization/impact', methods=['POST'])
    def visualize_impact():
        """可视化权重调整对特定行业或公司的影响"""
        try:
            data = request.json
            
            if not data:
                return jsonify({
                    'success': False,
                    'error': '请求数据为空'
                }), 400
            
            # 获取参数
            simulation_ids = data.get('simulation_ids')
            entity_code = data.get('entity_code')
            is_industry = data.get('is_industry', False)
            
            if not simulation_ids or not isinstance(simulation_ids, list):
                return jsonify({
                    'success': False,
                    'error': '模拟ID列表无效'
                }), 400
            
            if not entity_code:
                return jsonify({
                    'success': False,
                    'error': '实体代码无效'
                }), 400
            
            # 生成图表
            plt = simulator.visualize_weight_impact(simulation_ids, entity_code, is_industry)
            
            # 保存图表
            entity_type = 'industry' if is_industry else 'company'
            chart_path = os.path.join(simulator.data_path, f'{entity_type}_impact_{entity_code}.png')
            
            # 返回图表
            return send_file(chart_path, mimetype='image/png')
        except Exception as e:
            logger.error(f"可视化权重影响失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/visualization/weight_distribution', methods=['GET'])
    def visualize_weight_distribution():
        """可视化权重分布"""
        try:
            # 获取当前权重
            weights = simulator.weight_config
            
            # 展平权重
            from .utils import flatten_weights
            flattened = flatten_weights(weights)
            
            # 按类别分组
            categories = {}
            for key, value in flattened.items():
                category = key.split('.')[0]
                if category not in categories:
                    categories[category] = {}
                categories[category][key] = value
            
            # 生成图表
            import matplotlib.pyplot as plt
            import numpy as np
            
            # 创建图表
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # 设置颜色
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
            
            # 绘制饼图
            category_values = [sum(cat.values()) for cat in categories.values()]
            category_labels = list(categories.keys())
            
            wedges, texts, autotexts = ax.pie(
                category_values,
                labels=category_labels,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors[:len(categories)]
            )
            
            # 设置标题
            ax.set_title('权重分布')
            
            # 保存图表
            chart_path = os.path.join(simulator.data_path, 'weight_distribution.png')
            plt.savefig(chart_path)
            
            # 返回图表
            return send_file(chart_path, mimetype='image/png')
        except Exception as e:
            logger.error(f"可视化权重分布失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500