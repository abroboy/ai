# -*- coding: utf-8 -*-
"""
资金流向可视化器
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Any

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from utils.logger import LoggerMixin

class FlowVisualizer(LoggerMixin):
    """资金流向可视化器"""
    
    def __init__(self):
        """初始化可视化器"""
        super().__init__()
        
    def create_global_flow_chart(self, flow_data: Dict) -> str:
        """创建全球资金流向图表"""
        self.log_info("开始创建全球资金流向图表")
        
        # 创建图表目录
        chart_dir = os.path.join("static", "charts")
        os.makedirs(chart_dir, exist_ok=True)
        
        # 生成图表文件名
        filename = f"global_flow_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(chart_dir, filename)
        
        # 创建简单的HTML图表
        html_content = self._generate_html_chart(flow_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.log_info(f"全球资金流向图表已保存: {filepath}")
        return filepath
    
    def create_market_heatmap(self, market_data: Dict) -> str:
        """创建市场热力图"""
        self.log_info("开始创建市场热力图")
        
        # 创建图表目录
        chart_dir = os.path.join("static", "charts")
        os.makedirs(chart_dir, exist_ok=True)
        
        # 生成图表文件名
        filename = f"market_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(chart_dir, filename)
        
        # 创建简单的HTML热力图
        html_content = self._generate_heatmap_html(market_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.log_info(f"市场热力图已保存: {filepath}")
        return filepath
    
    def _generate_html_chart(self, flow_data: Dict) -> str:
        """生成HTML图表"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>全球资金流向分析</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .chart-container { width: 100%; height: 600px; }
            </style>
        </head>
        <body>
            <h1>全球资金流向分析</h1>
            <div id="chart" class="chart-container"></div>
            
            <script>
                var data = [
                    {
                        x: ['外汇', '股票', '债券', '大宗商品'],
                        y: [%s, %s, %s, %s],
                        type: 'bar',
                        marker: {
                            color: ['%s', '%s', '%s', '%s']
                        },
                        name: '资金流向'
                    }
                ];
                
                var layout = {
                    title: '全球资金流向分析',
                    xaxis: { title: '资产类别' },
                    yaxis: { title: '净流入（亿元）' }
                };
                
                Plotly.newPlot('chart', data, layout);
            </script>
        </body>
        </html>
        """
        
        # 获取数据
        forex_flow = flow_data.get('forex', {}).get('total_net_flow', 0)
        stock_flow = flow_data.get('stock', {}).get('total_net_flow', 0)
        bond_flow = flow_data.get('bond', {}).get('total_net_flow', 0)
        commodity_flow = flow_data.get('commodity', {}).get('total_net_flow', 0)
        
        # 设置颜色
        colors = ['green' if flow > 0 else 'red' for flow in [forex_flow, stock_flow, bond_flow, commodity_flow]]
        
        return html_template % (
            forex_flow, stock_flow, bond_flow, commodity_flow,
            colors[0], colors[1], colors[2], colors[3]
        )
    
    def _generate_heatmap_html(self, market_data: Dict) -> str:
        """生成热力图HTML"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>市场资金流向热力图</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .chart-container { width: 100%; height: 500px; }
            </style>
        </head>
        <body>
            <h1>市场资金流向热力图</h1>
            <div id="heatmap" class="chart-container"></div>
            
            <script>
                var data = [{
                    z: [
                        [%s, %s, %s, %s, %s],
                        [%s, %s, %s, %s, %s],
                        [%s, %s, %s, %s, %s],
                        [%s, %s, %s, %s, %s]
                    ],
                    x: ['净流入', '流向比率', '波动率', '相对强度', '动量'],
                    y: ['美国', '欧洲', '亚洲', '新兴市场'],
                    type: 'heatmap',
                    colorscale: 'RdYlGn',
                    zmid: 0
                }];
                
                var layout = {
                    title: '全球市场资金流向热力图',
                    xaxis: { title: '指标' },
                    yaxis: { title: '市场' }
                };
                
                Plotly.newPlot('heatmap', data, layout);
            </script>
        </body>
        </html>
        """
        
        # 生成随机数据
        import random
        data_values = []
        for i in range(4):  # 4个市场
            row = []
            for j in range(5):  # 5个指标
                row.append(random.uniform(-10, 10))
            data_values.extend(row)
        
        return html_template % tuple(data_values) 