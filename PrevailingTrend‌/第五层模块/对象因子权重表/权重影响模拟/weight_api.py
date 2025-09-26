#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
权重影响模拟模块 - API接口
"""

import os
import json
import logging
from flask import Flask, request, jsonify, send_file
from .weight_simulator import WeightSimulator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('weight_api')

# 创建Flask应用
app = Flask(__name__)

# 创建权重模拟器
simulator = WeightSimulator()

@app.route('/api/weights', methods=['GET'])
def get_weights():
    """获取当前权重配置"""
    try:
        return jsonify({
            'success': True,
            'data': simulator.weight_config
        })
    except Exception as e:
        logger.error(f"获取权重配置失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/weights', methods=['POST'])
def update_weights():
    """更新权重配置"""
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': '请求数据为空'
            }), 400
        
        # 更新权重配置
        simulator.weight_config = data
        
        # 保存权重配置
        weight_path = os.path.join(simulator.data_path, 'weight_config.json')
        with open(weight_path, 'w', encoding='utf-8') as f:
            json.dump(simulator.weight_config, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': '权重配置已更新'
        })
    except Exception as e:
        logger.error(f"更新权重配置失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500