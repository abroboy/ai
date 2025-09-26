#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
曲线预测分析API模块
提供RESTful API接口
"""

import os
import json
import logging
import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
import tempfile

from .curve_prediction_model import ARIMAModel, LSTMModel, EnsembleModel, evaluate_model
from .curve_visualization import CurveVisualizer
from .curve_data_processor import DataProcessor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('curve_api')

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 启用跨域请求

# 模型存储路径
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# 图表存储路径
CHART_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
if not os.path.exists(CHART_DIR):
    os.makedirs(CHART_DIR)

# 数据存储路径
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 创建可视化器
visualizer = CurveVisualizer()

# 创建数据处理器
data_processor = DataProcessor()

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    预测接口
    
    请求参数:
        data: 时间序列数据，格式为JSON数组或CSV字符串
        date_column: 日期列名
        value_column: 值列名
        model_type: 模型类型，可选值为'arima', 'lstm', 'ensemble'
        steps: 预测步数
        
    返回:
        预测结果
    """
    try:
        # 获取请求参数
        request_data = request.get_json()
        
        # 解析数据
        data = request_data.get('data')
        date_column = request_data.get('date_column', 'date')
        value_column = request_data.get('value_column', 'value')
        model_type = request_data.get('model_type', 'arima')
        steps = int(request_data.get('steps', 30))
        
        # 将数据转换为DataFrame
        df = data_processor.parse_input_data(data, date_column, value_column)
        
        # 提取时间序列
        series = df[value_column]
        
        # 创建模型
        if model_type == 'arima':
            model = ARIMAModel()
            model.fit(series)
        elif model_type == 'lstm':
            model = LSTMModel()
            model.fit(series)
        elif model_type == 'ensemble':
            # 创建ARIMA模型
            arima_model = ARIMAModel()
            arima_model.fit(series)
            
            # 创建LSTM模型
            lstm_model = LSTMModel()
            lstm_model.fit(series)
            
            # 创建集成模型
            model = EnsembleModel([arima_model, lstm_model])
        else:
            return jsonify({'error': f'不支持的模型类型 {model_type}'}), 400
        
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
        chart_filename = f'prediction_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        chart_path = os.path.join(CHART_DIR, chart_filename)
        
        if model_type == 'arima':
            visualizer.plot_prediction(
                series,
                pd.Series(forecast, index=date_range),
                confidence_intervals=(
                    pd.Series(conf_int.iloc[:, 0], index=date_range),
                    pd.Series(conf_int.iloc[:, 1], index=date_range)
                ),
                title='ARIMA预测结果',
                save_path=chart_path
            )
        else:
            visualizer.plot_prediction(
                series,
                forecast,
                title=f'{model_type.upper()}预测结果',
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

@app.route('/api/charts/<filename>', methods=['GET'])
def get_chart(filename):
    """
    获取图表
    
    参数:
        filename: 图表文件名
        
    返回:
        图表文件
    """
    try:
        return send_file(os.path.join(CHART_DIR, filename))
    
    except Exception as e:
        logger.error(f"获取图表失败: {e}")
        return jsonify({'error': str(e)}), 404

@app.route('/api/models', methods=['GET'])
def list_models():
    """
    列出所有模型
    
    返回:
        模型列表
    """
    try:
        models = []
        
        for model_dir in os.listdir(MODEL_DIR):
            model_path = os.path.join(MODEL_DIR, model_dir)
            
            if os.path.isdir(model_path):
                # 读取模型信息
                info_path = os.path.join(model_path, 'info.json')
                
                if os.path.exists(info_path):
                    with open(info_path, 'r') as f:
                        info = json.load(f)
                    
                    models.append({
                        'id': model_dir,
                        'name': info.get('name', model_dir),
                        'type': info.get('type', 'unknown'),
                        'created_at': info.get('created_at'),
                        'description': info.get('description', '')
                    })
        
        return jsonify({
            'success': True,
            'data': models
        })
    
    except Exception as e:
        logger.error(f"列出模型失败: {e}")
        return jsonify({'error': str(e)}), 500

def run_server(host='0.0.0.0', port=5000, debug=False):
    """
    运行API服务器
    
    参数:
        host: 主机地址
        port: 端口号
        debug: 是否启用调试模式
    """
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_server(debug=True)