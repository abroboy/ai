#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
权重影响模拟模块 - 行业API接口
"""

import logging
from flask import request, jsonify, send_file
import os
import matplotlib.pyplot as plt

logger = logging.getLogger('weight_api')

def register_industry_routes(app, simulator):
    """注册行业相关路由"""
    
    @app.route('/api/industry/simulate', methods=['POST'])
    def simulate_industry():
        """模拟权重调整对行业排名的影响"""
        try:
            data = request.json
            
            if not data:
                return jsonify({
                    'success': False,
                    'error': '请求数据为空'
                }), 400
            
            # 获取权重调整
            weight_adjustments = data.get('weight_adjustments')
            
            # 模拟行业排名
            result = simulator.simulate_industry_ranking(weight_adjustments)
            
            # 转换结果为JSON格式
            df = result['result']
            records = df.to_dict('records')
            
            return jsonify({
                'success': True,
                'simulation_id': result['simulation_id'],
                'data': records
            })
        except Exception as e:
            logger.error(f"模拟行业排名失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/industry/compare', methods=['POST'])
    def compare_industry():
        """比较多个行业模拟结果"""
        try:
            data = request.json
            
            if not data:
                return jsonify({
                    'success': False,
                    'error': '请求数据为空'
                }), 400
            
            # 获取模拟ID列表
            simulation_ids = data.get('simulation_ids')
            
            if not simulation_ids or not isinstance(simulation_ids, list):
                return jsonify({
                    'success': False,
                    'error': '模拟ID列表无效'
                }), 400
            
            # 比较模拟结果
            results = simulator.compare_industry_simulations(simulation_ids)
            
            # 转换结果为JSON格式
            json_results = {}
            for key, value in results.items():
                if key == 'base':
                    json_results[key] = {
                        'id': value['id'],
                        'weights': value['weights'],
                        'adjustments': value['adjustments'],
                        'result': value['result'].to_dict('records')
                    }
                else:
                    json_results[key] = {
                        'id': value['id'],
                        'weights': value['weights'],
                        'adjustments': value['adjustments'],
                        'result': value['result'].to_dict('records'),
                        'changes': value['changes'].to_dict('records')
                    }
            
            return jsonify({
                'success': True,
                'data': json_results
            })
        except Exception as e:
            logger.error(f"比较行业模拟结果失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/industry/chart/<simulation_id>', methods=['GET'])
    def industry_chart(simulation_id):
        """获取行业排名图表"""
        try:
            # 获取参数
            top_n = request.args.get('top_n', default=20, type=int)
            
            # 生成图表
            plt = simulator.visualize_industry_ranking(simulation_id, top_n)
            
            # 保存图表
            chart_path = os.path.join(simulator.data_path, f'industry_ranking_{simulation_id}.png')
            
            # 返回图表
            return send_file(chart_path, mimetype='image/png')
        except Exception as e:
            logger.error(f"获取行业排名图表失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500