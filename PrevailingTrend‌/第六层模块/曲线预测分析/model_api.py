#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模型API模块
提供模型管理相关的API接口
"""

import os
import json
import logging
import pandas as pd
from flask import jsonify, request
from datetime import datetime
import tempfile

from .curve_prediction_model import ARIMAModel, LSTMModel, EnsembleModel
from .curve_data_processor import DataProcessor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('model_api')

# 模型存储路径
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# 创建数据处理器
data_processor = DataProcessor()

def get_model(model_id):
    """
    获取模型信息
    
    参数:
        model_id: 模型ID
        
    返回:
        模型信息
    """
    try:
        model_path = os.path.join(MODEL_DIR, model_id)
        
        if not os.path.exists(model_path):
            return jsonify({'error': f'模型 {model_id} 不存在'}), 404
        
        # 读取模型信息
        info_path = os.path.join(model_path, 'info.json')
        
        if not os.path.exists(info_path):
            return jsonify({'error': f'模型 {model_id} 信息不存在'}), 404
        
        with open(info_path, 'r') as f:
            info = json.load(f)
        
        return jsonify({
            'success': True,
            'data': info
        })
    
    except Exception as e:
        logger.error(f"获取模型信息失败: {e}")
        return jsonify({'error': str(e)}), 500