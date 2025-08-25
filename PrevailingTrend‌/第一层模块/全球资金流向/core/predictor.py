# -*- coding: utf-8 -*-
"""
资金流向预测器
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from utils.logger import LoggerMixin

class FlowPredictor(LoggerMixin):
    """资金流向预测器"""
    
    def __init__(self):
        """初始化预测器"""
        super().__init__()
        
    def predict_flow_trend(self, historical_data: Dict, days_ahead: int = 7) -> Dict:
        """预测资金流向趋势"""
        self.log_info(f"开始预测资金流向趋势，预测天数: {days_ahead}")
        
        # 模拟预测结果
        prediction = {
            'predicted_trend': 'up',
            'confidence_level': 0.75,
            'predicted_values': [10.5, 12.3, 11.8, 13.2, 14.1, 13.8, 15.2],
            'prediction_dates': [
                (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
                for i in range(1, days_ahead + 1)
            ],
            'upper_bound': [15.2, 17.1, 16.5, 18.3, 19.2, 18.8, 20.1],
            'lower_bound': [5.8, 7.5, 7.1, 8.1, 9.0, 8.8, 10.3]
        }
        
        self.log_info("资金流向趋势预测完成")
        return prediction
    
    def predict_market_movement(self, market_data: Dict, days_ahead: int = 7) -> Dict:
        """预测市场走势"""
        self.log_info(f"开始预测市场走势，预测天数: {days_ahead}")
        
        # 模拟市场预测结果
        market_prediction = {
            'market_direction': 'bullish',
            'confidence': 0.68,
            'key_factors': [
                '美联储政策预期',
                '地缘政治风险',
                '经济数据表现',
                '技术面支撑'
            ],
            'risk_level': 'medium',
            'recommended_actions': [
                '关注高成长性资产',
                '适度增加风险敞口',
                '保持流动性缓冲'
            ]
        }
        
        self.log_info("市场走势预测完成")
        return market_prediction
    
    def predict_sector_performance(self, sector_data: Dict, days_ahead: int = 7) -> Dict:
        """预测行业表现"""
        self.log_info(f"开始预测行业表现，预测天数: {days_ahead}")
        
        # 模拟行业预测结果
        sectors = ['科技', '金融', '能源', '医疗', '消费', '工业']
        sector_predictions = {}
        
        for sector in sectors:
            sector_predictions[sector] = {
                'predicted_return': np.random.uniform(-5, 10),
                'confidence': np.random.uniform(0.5, 0.9),
                'risk_level': np.random.choice(['low', 'medium', 'high']),
                'trend': np.random.choice(['up', 'down', 'sideways'])
            }
        
        prediction = {
            'sector_predictions': sector_predictions,
            'top_performing_sectors': ['科技', '医疗', '消费'],
            'underperforming_sectors': ['能源', '工业'],
            'overall_market_outlook': 'positive'
        }
        
        self.log_info("行业表现预测完成")
        return prediction
    
    def generate_forecast_report(self, predictions: Dict) -> str:
        """生成预测报告"""
        self.log_info("开始生成预测报告")
        
        # 创建报告目录
        report_dir = os.path.join("static", "reports")
        os.makedirs(report_dir, exist_ok=True)
        
        # 生成报告文件名
        filename = f"flow_forecast_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(report_dir, filename)
        
        # 生成HTML报告
        html_content = self._generate_forecast_html(predictions)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.log_info(f"预测报告已保存: {filepath}")
        return filepath
    
    def _generate_forecast_html(self, predictions: Dict) -> str:
        """生成预测报告HTML"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>全球资金流向预测报告</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .container { max-width: 1200px; margin: 0 auto; }
                .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
                .prediction-item { margin: 10px 0; padding: 10px; background-color: #f9f9f9; }
                .chart-container { width: 100%; height: 400px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>全球资金流向预测报告</h1>
                <p>生成时间: %s</p>
                
                <div class="section">
                    <h2>资金流向趋势预测</h2>
                    <div class="prediction-item">
                        <strong>预测趋势:</strong> %s<br>
                        <strong>置信度:</strong> %.1f%%<br>
                        <strong>预测天数:</strong> %d天
                    </div>
                    <div id="trend-chart" class="chart-container"></div>
                </div>
                
                <div class="section">
                    <h2>市场走势预测</h2>
                    <div class="prediction-item">
                        <strong>市场方向:</strong> %s<br>
                        <strong>置信度:</strong> %.1f%%<br>
                        <strong>风险等级:</strong> %s
                    </div>
                </div>
                
                <div class="section">
                    <h2>行业表现预测</h2>
                    <div id="sector-chart" class="chart-container"></div>
                </div>
            </div>
            
            <script>
                // 趋势预测图表
                var trendData = [{
                    x: %s,
                    y: %s,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: '预测趋势',
                    line: {color: 'blue', width: 2}
                }];
                
                var trendLayout = {
                    title: '资金流向趋势预测',
                    xaxis: { title: '日期' },
                    yaxis: { title: '资金流向' }
                };
                
                Plotly.newPlot('trend-chart', trendData, trendLayout);
                
                // 行业预测图表
                var sectorData = [{
                    x: %s,
                    y: %s,
                    type: 'bar',
                    name: '预测收益率',
                    marker: {
                        color: %s
                    }
                }];
                
                var sectorLayout = {
                    title: '行业表现预测',
                    xaxis: { title: '行业' },
                    yaxis: { title: '预测收益率 (%)' }
                };
                
                Plotly.newPlot('sector-chart', sectorData, sectorLayout);
            </script>
        </body>
        </html>
        """
        
        # 获取预测数据
        flow_prediction = predictions.get('flow_trend', {})
        market_prediction = predictions.get('market_movement', {})
        sector_prediction = predictions.get('sector_performance', {})
        
        # 准备图表数据
        trend_dates = flow_prediction.get('prediction_dates', [])
        trend_values = flow_prediction.get('predicted_values', [])
        
        sectors = list(sector_prediction.get('sector_predictions', {}).keys())
        sector_returns = [sector_prediction['sector_predictions'][s]['predicted_return'] for s in sectors]
        sector_colors = ['green' if ret > 0 else 'red' for ret in sector_returns]
        
        return html_template % (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            flow_prediction.get('predicted_trend', 'unknown'),
            flow_prediction.get('confidence_level', 0) * 100,
            len(trend_dates),
            market_prediction.get('market_direction', 'unknown'),
            market_prediction.get('confidence', 0) * 100,
            market_prediction.get('risk_level', 'unknown'),
            str(trend_dates),
            str(trend_values),
            str(sectors),
            str(sector_returns),
            str(sector_colors)
        ) 