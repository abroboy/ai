#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模型操作模块
提供模型创建、删除、预测等功能
"""

import os
import json
import logging
import pandas as pd
from flask import jsonify, request
from datetime import datetime, timedelta
import tempfile
import shutil

from .curve_prediction_model import ARIMAModel, LSTMModel, EnsembleModel
from .curve_data_processor import DataProcessor
from .curve_visualization import CurveVisualizer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('model_operations')

# 模型存储路径
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# 图表存储路径
CHART_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
if not os.path.exists(CHART_DIR):
    os.makedirs(CHART_DIR)

# 创建数据处理器
data_processor = DataProcessor()

# 创建可视化器
visualizer = CurveVisualizer()

def delete_model(model_id):
    """
    删除模型
    
    参数:
        model_id: 模型ID
        
    返回:
        删除结果
    """
    try:
        model_path = os.path.join(MODEL_DIR, model_id)
        
        if not os.path.exists(model_path):
            return jsonify({'error': f'模型 {model_id} 不存在'}), 404
        
        # 删除模型目录
        shutil.rmtree(model_path)
        
        return jsonify({
            'success': True,
            'message': f'模型 {model_id} 已删除'
        })
    
    except Exception as e:
        logger.error(f"删除模型失败: {e}")
        return jsonify({'error': str(e)}), 500

def create_model(request_data):
    """
    创建模型
    
    参数:
        request_data: 请求数据
        
    返回:
        创建结果
    """
    try:
        # 解析参数
        name = request_data.get('name')
        model_type = request_data.get('type', 'arima')
        description = request_data.get('description', '')
        data = request_data.get('data')
        date_column = request_data.get('date_column', 'date')
        value_column = request_data.get('value_column', 'value')
        
        # 验证参数
        if not name:
            return jsonify({'error': '模型名称不能为空'}), 400
        
        if not data:
            return jsonify({'error': '训练数据不能为空'}), 400
        
        # 解析数据
        df = data_processor.parse_input_data(data, date_column, value_column)
        
        # 提取时间序列
        series = df[value_column]
        
        # 创建模型ID
        model_id = f"{name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 创建模型目录
        model_path = os.path.join(MODEL_DIR, model_id)
        os.makedirs(model_path, exist_ok=True)
        
        # 创建模型
        if model_type == 'arima':
            model = ARIMAModel()
            model.fit(series)
            model.save(os.path.join(model_path, 'model'))
        elif model_type == 'lstm':
            model = LSTMModel()
            model.fit(series)
            model.save(os.path.join(model_path, 'model'))
        elif model_type == 'ensemble':
            # 创建ARIMA模型
            arima_model = ARIMAModel()
            arima_model.fit(series)
            
            # 创建LSTM模型
            lstm_model = LSTMModel()
            lstm_model.fit(series)
            
            # 创建集成模型
            model = EnsembleModel([arima_model, lstm_model])
            model.save(os.path.join(model_path, 'model'))
        else:
            return jsonify({'error': f'不支持的模型类型 {model_type}'}), 400
        
        # 保存模型信息
        info = {
            'id': model_id,
            'name': name,
            'type': model_type,
            'description': description,
            'created_at': datetime.now().isoformat(),
            'parameters': {
                'date_column': date_column,
                'value_column': value_column
            }
        }
        
        with open(os.path.join(model_path, 'info.json'), 'w') as f:
            json.dump(info, f, indent=2)
        
        # 保存训练数据
        df.to_csv(os.path.join(model_path, 'training_data.csv'))
        
        return jsonify({
            'success': True,
            'data': {
                'id': model_id,
                'name': name,
                'type': model_type,
                'created_at': info['created_at']
            },
            'message': f'模型 {name} 已创建'
        })
    
    except Exception as e:
        logger.error(f"创建模型失败: {e}")
        return jsonify({'error': str(e)}), 500