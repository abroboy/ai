# -*- coding: utf-8 -*-
"""
全球资金流向分析Web应用
"""

import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from config import API_CONFIG
from core.data_collector import DataCollector
from core.flow_analyzer import FlowAnalyzer
from core.trend_analyzer import TrendAnalyzer
from core.visualizer import FlowVisualizer
from core.predictor import FlowPredictor
from utils.logger import setup_logger
from utils.database import DatabaseManager
from admin.admin_app import admin_app

# 设置日志
logger = setup_logger('global_flow_app')

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 初始化组件
db_manager = DatabaseManager()
data_collector = DataCollector(db_manager)
flow_analyzer = FlowAnalyzer(db_manager)
trend_analyzer = TrendAnalyzer(db_manager)
visualizer = FlowVisualizer()
predictor = FlowPredictor()

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """仪表盘页面"""
    return render_template('dashboard.html')

@app.route('/api/collect_data', methods=['POST'])
def collect_data():
    """收集数据API"""
    try:
        logger.info("开始收集数据")
        
        # 收集所有数据
        all_data = data_collector.collect_all_data()
        
        # 保存到数据库
        data_collector.save_data_to_database(all_data)
        
        return jsonify({
            'success': True,
            'message': '数据收集成功',
            'data': {
                'total_records': sum(len(data) for data in all_data.values()),
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"数据收集失败: {e}")
        return jsonify({
            'success': False,
            'message': f'数据收集失败: {str(e)}'
        }), 500

@app.route('/api/analyze_flow', methods=['GET'])
def analyze_flow():
    """分析资金流向API"""
    try:
        days = request.args.get('days', 30, type=int)
        asset_type = request.args.get('asset_type')
        
        logger.info(f"开始分析资金流向，天数: {days}, 资产类型: {asset_type}")
        
        # 分析全球资金流向趋势
        global_analysis = flow_analyzer.analyze_global_flow_trends(days)
        
        # 分析趋势
        trend_analysis = trend_analyzer.analyze_flow_trends(asset_type, days)
        
        return jsonify({
            'success': True,
            'message': '分析完成',
            'data': {
                'global_analysis': global_analysis,
                'trend_analysis': trend_analysis,
                'analysis_period': f'{days}天',
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"资金流向分析失败: {e}")
        return jsonify({
            'success': False,
            'message': f'分析失败: {str(e)}'
        }), 500

@app.route('/api/analyze_market', methods=['GET'])
def analyze_market():
    """分析市场API"""
    try:
        days = request.args.get('days', 30, type=int)
        market_type = request.args.get('market_type')
        
        logger.info(f"开始分析市场，天数: {days}, 市场类型: {market_type}")
        
        # 分析市场资金流向
        market_analysis = flow_analyzer.analyze_market_flow(market_type, days)
        
        # 分析市场趋势
        market_trends = trend_analyzer.analyze_market_trends(market_type, days)
        
        return jsonify({
            'success': True,
            'message': '市场分析完成',
            'data': {
                'market_analysis': market_analysis,
                'market_trends': market_trends,
                'analysis_period': f'{days}天',
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"市场分析失败: {e}")
        return jsonify({
            'success': False,
            'message': f'市场分析失败: {str(e)}'
        }), 500

@app.route('/api/create_charts', methods=['POST'])
def create_charts():
    """创建图表API"""
    try:
        data = request.get_json()
        flow_data = data.get('flow_data', {})
        market_data = data.get('market_data', {})
        
        logger.info("开始创建图表")
        
        # 创建各种图表
        global_chart = visualizer.create_global_flow_chart(flow_data)
        market_heatmap = visualizer.create_market_heatmap(market_data)
        
        return jsonify({
            'success': True,
            'message': '图表创建成功',
            'data': {
                'global_chart': global_chart,
                'market_heatmap': market_heatmap,
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"图表创建失败: {e}")
        return jsonify({
            'success': False,
            'message': f'图表创建失败: {str(e)}'
        }), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """预测API"""
    try:
        data = request.get_json()
        historical_data = data.get('historical_data', {})
        days_ahead = data.get('days_ahead', 7)
        
        logger.info(f"开始预测，预测天数: {days_ahead}")
        
        # 进行各种预测
        flow_prediction = predictor.predict_flow_trend(historical_data, days_ahead)
        market_prediction = predictor.predict_market_movement(historical_data, days_ahead)
        sector_prediction = predictor.predict_sector_performance(historical_data, days_ahead)
        
        # 生成预测报告
        predictions = {
            'flow_trend': flow_prediction,
            'market_movement': market_prediction,
            'sector_performance': sector_prediction
        }
        report_path = predictor.generate_forecast_report(predictions)
        
        return jsonify({
            'success': True,
            'message': '预测完成',
            'data': {
                'flow_prediction': flow_prediction,
                'market_prediction': market_prediction,
                'sector_prediction': sector_prediction,
                'report_path': report_path,
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"预测失败: {e}")
        return jsonify({
            'success': False,
            'message': f'预测失败: {str(e)}'
        }), 500

@app.route('/api/status')
def status():
    """系统状态API"""
    try:
        status_info = {
            'system_status': 'running',
            'database_connected': True,
            'last_update': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        
        return jsonify({
            'success': True,
            'message': '系统状态正常',
            'data': status_info
        })
        
    except Exception as e:
        logger.error(f"获取系统状态失败: {e}")
        return jsonify({
            'success': False,
            'message': f'获取状态失败: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'message': '页面未找到'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        'success': False,
        'message': '服务器内部错误'
    }), 500

# 注册管理台应用
app.register_blueprint(admin_app, url_prefix='/admin')

if __name__ == '__main__':
    # 创建必要的目录
    os.makedirs('static/charts', exist_ok=True)
    os.makedirs('static/reports', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # 启动应用
    app.run(
        host=API_CONFIG['host'],
        port=API_CONFIG['port'],
        debug=API_CONFIG['debug'],
        threaded=API_CONFIG['threaded']
    ) 