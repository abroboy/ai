#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
曲线预测分析应用入口
"""

import os
import logging
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from .curve_api import app as curve_api_app
from .model_api import get_model
from .model_operations import create_model, delete_model
from .prediction_service import predict_with_model

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('app')

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 启用跨域请求

# 图表存储路径
CHART_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
if not os.path.exists(CHART_DIR):
    os.makedirs(CHART_DIR)

# 注册路由
@app.route('/api/models', methods=['GET'])
def list_models():
    """列出所有模型"""
    return curve_api_app.list_models()

@app.route('/api/models', methods=['POST'])
def create_model_route():
    """创建模型"""
    return create_model(request.get_json())

@app.route('/api/models/<model_id>', methods=['GET'])
def get_model_route(model_id):
    """获取模型信息"""
    return get_model(model_id)

@app.route('/api/models/<model_id>', methods=['DELETE'])
def delete_model_route(model_id):
    """删除模型"""
    return delete_model(model_id)

@app.route('/api/models/<model_id>/predict', methods=['POST'])
def predict_with_model_route(model_id):
    """使用指定模型进行预测"""
    return predict_with_model(model_id, request.get_json())

@app.route('/api/predict', methods=['POST'])
def predict():
    """预测接口"""
    return curve_api_app.predict()

@app.route('/api/charts/<filename>', methods=['GET'])
def get_chart(filename):
    """获取图表"""
    try:
        return send_file(os.path.join(CHART_DIR, filename))
    
    except Exception as e:
        logger.error(f"获取图表失败: {e}")
        return jsonify({'error': str(e)}), 404

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