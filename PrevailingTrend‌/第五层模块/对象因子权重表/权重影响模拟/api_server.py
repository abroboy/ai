#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
权重影响模拟模块 - API服务器
"""

import os
import logging
from flask import Flask, jsonify
from .weight_simulator import WeightSimulator
from .weight_api_industry import register_industry_routes
from .weight_api_company import register_company_routes
from .weight_api_visualization import register_visualization_routes

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('api_server')

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 创建权重模拟器
    simulator = WeightSimulator()
    
    # 注册路由
    register_routes(app, simulator)
    
    return app

def register_routes(app, simulator):
    """注册路由"""
    # 注册权重配置路由
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
    
    # 注册行业相关路由
    register_industry_routes(app, simulator)
    
    # 注册公司相关路由
    register_company_routes(app, simulator)
    
    # 注册可视化相关路由
    register_visualization_routes(app, simulator)
    
    # 注册错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': '接口不存在'
        }), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500

def run_server(host='0.0.0.0', port=5000, debug=False):
    """运行API服务器"""
    app = create_app()
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_server(debug=True)