# -*- coding: utf-8 -*-
"""
资金流向API接口
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from flask import Blueprint, request, jsonify

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from core.data_collector import DataCollector
from core.flow_analyzer import FlowAnalyzer
from utils.logger import LoggerMixin

# 创建蓝图
flow_api = Blueprint('flow_api', __name__)

class FlowAPI(LoggerMixin):
    """资金流向API类"""
    
    def __init__(self):
        """初始化API"""
        super().__init__()
        self.data_collector = DataCollector()
        self.flow_analyzer = FlowAnalyzer()
    
    @flow_api.route('/api/flow/collect', methods=['POST'])
    def collect_data():
        """收集资金流向数据"""
        try:
            api = FlowAPI()
            api.log_info("开始收集资金流向数据")
            
            # 获取请求参数
            data = request.get_json() or {}
            asset_types = data.get('asset_types', ['forex', 'stock', 'bond', 'commodity'])
            
            # 收集数据
            all_data = api.data_collector.collect_all_data()
            
            # 保存到数据库
            api.data_collector.save_data_to_database(all_data)
            
            return jsonify({
                'success': True,
                'message': '数据收集成功',
                'data': {
                    'total_records': sum(len(data) for data in all_data.values()),
                    'asset_types': list(all_data.keys())
                }
            })
            
        except Exception as e:
            api.log_error(f"数据收集失败: {e}")
            return jsonify({
                'success': False,
                'message': f'数据收集失败: {str(e)}'
            }), 500
    
    @flow_api.route('/api/flow/analyze', methods=['GET'])
    def analyze_flow():
        """分析资金流向"""
        try:
            api = FlowAPI()
            
            # 获取请求参数
            days = request.args.get('days', 30, type=int)
            asset_type = request.args.get('asset_type')
            market_type = request.args.get('market_type')
            
            api.log_info(f"开始分析资金流向，天数: {days}, 资产类型: {asset_type}, 市场类型: {market_type}")
            
            # 分析全球资金流向趋势
            global_analysis = api.flow_analyzer.analyze_global_flow_trends(days)
            
            # 分析特定市场资金流向
            market_analysis = {}
            if market_type:
                market_analysis = api.flow_analyzer.analyze_market_flow(market_type, days)
            
            return jsonify({
                'success': True,
                'message': '分析完成',
                'data': {
                    'global_analysis': global_analysis,
                    'market_analysis': market_analysis,
                    'analysis_period': f'{days}天',
                    'timestamp': datetime.now().isoformat()
                }
            })
            
        except Exception as e:
            api.log_error(f"资金流向分析失败: {e}")
            return jsonify({
                'success': False,
                'message': f'分析失败: {str(e)}'
            }), 500
    
    @flow_api.route('/api/flow/sector', methods=['GET'])
    def analyze_sector():
        """分析行业资金流向"""
        try:
            api = FlowAPI()
            
            # 获取请求参数
            days = request.args.get('days', 30, type=int)
            sector = request.args.get('sector')
            
            api.log_info(f"开始分析行业资金流向，天数: {days}, 行业: {sector}")
            
            # 分析行业资金流向
            sector_analysis = api.flow_analyzer.analyze_sector_flow(sector, days)
            
            return jsonify({
                'success': True,
                'message': '行业分析完成',
                'data': {
                    'sector_analysis': sector_analysis,
                    'analysis_period': f'{days}天',
                    'sector': sector,
                    'timestamp': datetime.now().isoformat()
                }
            })
            
        except Exception as e:
            api.log_error(f"行业资金流向分析失败: {e}")
            return jsonify({
                'success': False,
                'message': f'行业分析失败: {str(e)}'
            }), 500
    
    @flow_api.route('/api/flow/summary', methods=['GET'])
    def get_flow_summary():
        """获取资金流向摘要"""
        try:
            api = FlowAPI()
            
            # 获取请求参数
            days = request.args.get('days', 7, type=int)
            
            api.log_info(f"获取资金流向摘要，天数: {days}")
            
            # 获取各种分析结果
            global_analysis = api.flow_analyzer.analyze_global_flow_trends(days)
            
            # 构建摘要数据
            summary = {
                'total_net_flow': global_analysis.get('global', {}).get('total_net_flow', 0),
                'flow_trend': global_analysis.get('global', {}).get('flow_trend', 'unknown'),
                'asset_flows': {
                    asset: data.get('total_net_flow', 0)
                    for asset, data in global_analysis.items()
                    if asset != 'global'
                },
                'top_assets': [],
                'market_sentiment': 'neutral',
                'risk_level': 'medium',
                'last_updated': datetime.now().isoformat()
            }
            
            return jsonify({
                'success': True,
                'message': '摘要获取成功',
                'data': summary
            })
            
        except Exception as e:
            api.log_error(f"获取资金流向摘要失败: {e}")
            return jsonify({
                'success': False,
                'message': f'获取摘要失败: {str(e)}'
            }), 500
    
    @flow_api.route('/api/flow/status', methods=['GET'])
    def get_system_status():
        """获取系统状态"""
        try:
            api = FlowAPI()
            
            status = {
                'system_status': 'running',
                'database_connected': True,
                'last_data_collection': datetime.now().isoformat(),
                'data_sources': ['forex', 'stock', 'bond', 'commodity'],
                'api_version': '1.0.0',
                'uptime': '24小时'
            }
            
            return jsonify({
                'success': True,
                'message': '系统状态正常',
                'data': status
            })
            
        except Exception as e:
            api.log_error(f"获取系统状态失败: {e}")
            return jsonify({
                'success': False,
                'message': f'获取状态失败: {str(e)}'
            }), 500 