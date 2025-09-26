#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
预测服务模块
提供预测相关功能
"""

import os
import json
import logging
import pandas as pd
from flask import jsonify
from datetime import datetime, timedelta

from .curve_prediction_model import ARIMAModel, LSTMModel, EnsembleModel
from .curve_data_processor import DataProcessor
from .curve_visualization import CurveVisualizer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('prediction_service')

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

def predict_with_model(model_id, request_data):
    """
    使用指定模型进行预测
    
    参数:
        model_id: 模型ID
        request_data: 请求数据
        
    返回:
        预测结果
    """
    try:
        # 检查模型是否存在
        model_path = os.path.join(MODEL_DIR, model_id)
        
        if not os.path.exists(model_path):
            return jsonify({'error': f'模型 {model_id} 不存在'}), 404
        
        # 读取模型信息
        info_path = os.path.join(model_path, 'info.json')
        
        if not os.path.exists(info_path):
            return jsonify({'error': f'模型 {model_id} 信息不存在'}), 404
        
        with open(info_path, 'r') as f:
            info = json.load(f)
        
        # 解析参数
        data = request_data.get('data')
        steps = int(request_data.get('steps', 30))
        
        # 加载模型
        model_type = info.get('type', 'arima')
        
        if model_type == 'arima':
            model = ARIMAModel.load(os.path.join(model_path, 'model'))
        elif model_type == 'lstm':
            model = LSTMModel.load(os.path.join(model_path, 'model'))
        elif model_type == 'ensemble':
            model = EnsembleModel.load(os.path.join(model_path, 'model'))
        else:
            return jsonify({'error': f'不支持的模型类型 {model_type}'}), 400
        
        # 如果提供了数据，则使用提供的数据进行预测
        if data:
            # 解析数据
            date_column = info['parameters'].get('date_column', 'date')
            value_column = info['parameters'].get('value_column', 'value')
            
            df = data_processor.parse_input_data(data, date_column, value_column)
            series = df[value_column]
            
            # 预测
            if model_type == 'arima':
                forecast, conf_int = model.predict(steps=steps)
                
                # 将预测结果转换为DataFrame
                last_date = series.index[-1]
                date_range = pd.date_range(start=last_date + timedelta(days=1), periods=steps)
                
                forecast_df = pd.DataFrame({
                    'date': date_range,
                    'prediction': forecast,
                    'lower_bound': conf_int.iloc[:, 0],
                    'upper_bound': conf_int.iloc[:, 1]
                })
            elif model_type == 'lstm':
                forecast = model.predict(series, steps=steps)
                
                # 将预测结果转换为DataFrame
                forecast_df = pd.DataFrame({
                    'date': forecast.index,
                    'prediction': forecast.values
                })
            elif model_type == 'ensemble':
                forecast = model.predict(series, steps=steps)
                
                # 将预测结果转换为DataFrame
                forecast_df = pd.DataFrame({
                    'date': forecast.index,
                    'prediction': forecast.values
                })
        else:
            # 使用训练数据进行预测
            training_data_path = os.path.join(model_path, 'training_data.csv')
            
            if not os.path.exists(training_data_path):
                return jsonify({'error': '训练数据不存在，请提供预测数据'}), 400
            
            # 读取训练数据
            df = pd.read_csv(training_data_path)
            date_column = info['parameters'].get('date_column', 'date')
            value_column = info['parameters'].get('value_column', 'value')
            
            # 将日期列转换为日期类型
            df[date_column] = pd.to_datetime(df[date_column])
            
            # 设置日期列为索引
            df = df.set_index(date_column)
            
            # 提取时间序列
            series = df[value_column]
            
            # 预测
            if model_type == 'arima':
                forecast, conf_int = model.predict(steps=steps)
                
                # 将预测结果转换为DataFrame
                last_date = series.index[-1]
                date_range = pd.date_range(start=last_date + timedelta(days=1), periods=steps)
                
                forecast_df = pd.DataFrame({
                    'date': date_range,
                    'prediction': forecast,
                    'lower_bound': conf_int.iloc[:, 0],
                    'upper_bound': conf_int.iloc[:, 1]
                })
            elif model_type == 'lstm':
                forecast = model.predict(series, steps=steps)
                
                # 将预测结果转换为DataFrame
                forecast_df = pd.DataFrame({
                    'date': forecast.index,
                    'prediction': forecast.values
                })
            elif model_type == 'ensemble':
                forecast = model.predict(series, steps=steps)
                
                # 将预测结果转换为DataFrame
                forecast_df = pd.DataFrame({
                    'date': forecast.index,
                    'prediction': forecast.values
                })
        
        # 生成预测图表
        chart_filename = f'prediction_{model_id}_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        chart_path = os.path.join(CHART_DIR, chart_filename)
        
        if model_type == 'arima':
            visualizer.plot_prediction(
                series,
                pd.Series(forecast, index=date_range),
                confidence_intervals=(
                    pd.Series(conf_int.iloc[:, 0], index=date_range),
                    pd.Series(conf_int.iloc[:, 1], index=date_range)
                ),
                title=f'{info["name"]} 预测结果',
                save_path=chart_path
            )
        else:
            visualizer.plot_prediction(
                series,
                forecast,
                title=f'{info["name"]} 预测结果',
                save_path=chart_path
            )
        
        # 返回结果
        return jsonify({
            'success': True,
            'data': forecast_df.to_dict(orient='records'),
            'chart_url': f'/api/charts/{chart_filename}'
        })
    
    except Exception as e:
        logger.error(f"预测失败: {e}")
        return jsonify({'error': str(e)}), 500