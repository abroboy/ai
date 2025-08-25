#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球资金流向分析系统演示脚本
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from core.data_collector import DataCollector
from core.flow_analyzer import FlowAnalyzer
from core.trend_analyzer import TrendAnalyzer
from core.visualizer import FlowVisualizer
from core.predictor import FlowPredictor
from utils.logger import setup_logger

def run_demo():
    """运行演示"""
    logger = setup_logger('demo')
    
    print("=" * 60)
    print("全球资金流向分析系统演示")
    print("=" * 60)
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 1. 数据收集演示
        print("1. 数据收集演示")
        print("-" * 30)
        
        data_collector = DataCollector()
        all_data = data_collector.collect_all_data()
        
        total_records = sum(len(data) for data in all_data.values())
        print(f"✓ 成功收集 {total_records} 条数据记录")
        print(f"  - 外汇数据: {len(all_data['forex'])} 条")
        print(f"  - 股票数据: {len(all_data['stock'])} 条")
        print(f"  - 债券数据: {len(all_data['bond'])} 条")
        print(f"  - 大宗商品数据: {len(all_data['commodity'])} 条")
        print()
        
        # 2. 资金流向分析演示
        print("2. 资金流向分析演示")
        print("-" * 30)
        
        flow_analyzer = FlowAnalyzer()
        global_analysis = flow_analyzer.analyze_global_flow_trends(30)
        
        print("全球资金流向分析结果:")
        for asset_type, analysis in global_analysis.items():
            if asset_type != 'global':
                print(f"  {asset_type.upper()}:")
                print(f"    - 总净流入: {analysis.get('total_net_flow', 0):.2f}")
                print(f"    - 平均流向比率: {analysis.get('avg_flow_ratio', 0):.2f}")
                print(f"    - 趋势方向: {analysis.get('flow_trend', 'unknown')}")
                print(f"    - 正向流向比例: {analysis.get('positive_flow_percentage', 0):.1f}%")
        print()
        
        # 3. 趋势分析演示
        print("3. 趋势分析演示")
        print("-" * 30)
        
        trend_analyzer = TrendAnalyzer()
        flow_trends = trend_analyzer.analyze_flow_trends('stock', 30)
        
        print("资金流向趋势分析结果:")
        print(f"  - 短期趋势: {flow_trends.get('short_term_trend', 'unknown')}")
        print(f"  - 中期趋势: {flow_trends.get('medium_term_trend', 'unknown')}")
        print(f"  - 长期趋势: {flow_trends.get('long_term_trend', 'unknown')}")
        print(f"  - 趋势强度: {flow_trends.get('trend_strength', 0):.2f}")
        print(f"  - 趋势置信度: {flow_trends.get('trend_confidence', 0):.2f}")
        print()
        
        # 4. 可视化演示
        print("4. 可视化演示")
        print("-" * 30)
        
        visualizer = FlowVisualizer()
        
        # 创建全球资金流向图表
        chart_path = visualizer.create_global_flow_chart(global_analysis)
        print(f"✓ 全球资金流向图表已创建: {chart_path}")
        
        # 创建市场热力图
        market_data = {}
        heatmap_path = visualizer.create_market_heatmap(market_data)
        print(f"✓ 市场热力图已创建: {heatmap_path}")
        print()
        
        # 5. 预测分析演示
        print("5. 预测分析演示")
        print("-" * 30)
        
        predictor = FlowPredictor()
        
        # 资金流向趋势预测
        historical_data = {}
        flow_prediction = predictor.predict_flow_trend(historical_data, 7)
        
        print("资金流向趋势预测结果:")
        print(f"  - 预测趋势: {flow_prediction.get('predicted_trend', 'unknown')}")
        print(f"  - 置信度: {flow_prediction.get('confidence_level', 0):.2f}")
        print(f"  - 预测天数: {len(flow_prediction.get('predicted_values', []))} 天")
        
        # 市场走势预测
        market_prediction = predictor.predict_market_movement(historical_data, 7)
        print("\n市场走势预测结果:")
        print(f"  - 市场方向: {market_prediction.get('market_direction', 'unknown')}")
        print(f"  - 置信度: {market_prediction.get('confidence', 0):.2f}")
        print(f"  - 风险等级: {market_prediction.get('risk_level', 'unknown')}")
        
        # 行业表现预测
        sector_prediction = predictor.predict_sector_performance(historical_data, 7)
        print("\n行业表现预测结果:")
        print(f"  - 预测行业数量: {len(sector_prediction.get('sector_predictions', {}))}")
        print(f"  - 表现最佳行业: {', '.join(sector_prediction.get('top_performing_sectors', []))}")
        print(f"  - 整体市场展望: {sector_prediction.get('overall_market_outlook', 'unknown')}")
        print()
        
        # 6. 生成预测报告
        print("6. 生成预测报告")
        print("-" * 30)
        
        predictions = {
            'flow_trend': flow_prediction,
            'market_movement': market_prediction,
            'sector_performance': sector_prediction
        }
        
        report_path = predictor.generate_forecast_report(predictions)
        print(f"✓ 预测报告已生成: {report_path}")
        print()
        
        # 演示总结
        print("=" * 60)
        print("演示完成！")
        print("=" * 60)
        print("系统功能演示总结:")
        print("✓ 数据收集: 成功收集多源数据")
        print("✓ 流向分析: 完成全球资金流向分析")
        print("✓ 趋势分析: 识别资金流向趋势")
        print("✓ 可视化: 生成交互式图表")
        print("✓ 预测分析: 提供未来趋势预测")
        print("✓ 报告生成: 创建综合分析报告")
        print()
        print("系统已准备就绪，可以开始使用！")
        print("访问 http://localhost:5003 查看Web界面")
        
    except Exception as e:
        logger.error(f"演示过程中出现错误: {e}")
        print(f"✗ 演示失败: {e}")
        return False
    
    return True

if __name__ == '__main__':
    run_demo() 