#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球资金流向分析系统测试脚本
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from utils.logger import setup_logger
from utils.database import DatabaseManager
from core.data_collector import DataCollector
from core.flow_analyzer import FlowAnalyzer
from core.trend_analyzer import TrendAnalyzer
from core.visualizer import FlowVisualizer
from core.predictor import FlowPredictor

def test_database():
    """测试数据库连接"""
    print("测试数据库连接...")
    logger = setup_logger('test_db')
    
    try:
        db_manager = DatabaseManager()
        if db_manager.connect():
            print("✓ 数据库连接成功")
            
            # 测试创建表
            if db_manager.create_tables():
                print("✓ 数据库表创建成功")
            else:
                print("✗ 数据库表创建失败")
                return False
                
            # 测试查询
            stats = db_manager.get_database_stats()
            print(f"✓ 数据库统计信息获取成功: {len(stats)} 个表")
            
            db_manager.close()
            return True
        else:
            print("✗ 数据库连接失败")
            return False
            
    except Exception as e:
        logger.error(f"数据库测试失败: {e}")
        print(f"✗ 数据库测试失败: {e}")
        return False

def test_data_collector():
    """测试数据收集器"""
    print("\n测试数据收集器...")
    logger = setup_logger('test_collector')
    
    try:
        data_collector = DataCollector()
        
        # 测试外汇数据收集
        forex_data = data_collector.collect_forex_data()
        print(f"✓ 外汇数据收集成功: {len(forex_data)} 条记录")
        
        # 测试股票数据收集
        stock_data = data_collector.collect_stock_market_data()
        print(f"✓ 股票数据收集成功: {len(stock_data)} 条记录")
        
        # 测试所有数据收集
        all_data = data_collector.collect_all_data()
        total_records = sum(len(data) for data in all_data.values())
        print(f"✓ 所有数据收集成功: {total_records} 条记录")
        
        return True
        
    except Exception as e:
        logger.error(f"数据收集器测试失败: {e}")
        print(f"✗ 数据收集器测试失败: {e}")
        return False

def test_flow_analyzer():
    """测试资金流向分析器"""
    print("\n测试资金流向分析器...")
    logger = setup_logger('test_analyzer')
    
    try:
        flow_analyzer = FlowAnalyzer()
        
        # 测试全球资金流向趋势分析
        global_analysis = flow_analyzer.analyze_global_flow_trends(30)
        print(f"✓ 全球资金流向趋势分析成功: {len(global_analysis)} 个分析结果")
        
        # 测试市场资金流向分析
        market_analysis = flow_analyzer.analyze_market_flow('US', 30)
        print(f"✓ 市场资金流向分析成功: {len(market_analysis)} 个指标")
        
        # 测试行业资金流向分析
        sector_analysis = flow_analyzer.analyze_sector_flow('tech', 30)
        print(f"✓ 行业资金流向分析成功: {len(sector_analysis)} 个指标")
        
        return True
        
    except Exception as e:
        logger.error(f"资金流向分析器测试失败: {e}")
        print(f"✗ 资金流向分析器测试失败: {e}")
        return False

def test_trend_analyzer():
    """测试趋势分析器"""
    print("\n测试趋势分析器...")
    logger = setup_logger('test_trend')
    
    try:
        trend_analyzer = TrendAnalyzer()
        
        # 测试资金流向趋势分析
        flow_trends = trend_analyzer.analyze_flow_trends('stock', 30)
        print(f"✓ 资金流向趋势分析成功: {len(flow_trends)} 个指标")
        
        # 测试市场趋势分析
        market_trends = trend_analyzer.analyze_market_trends('US', 30)
        print(f"✓ 市场趋势分析成功: {len(market_trends)} 个指标")
        
        # 测试资产趋势分析
        asset_trends = trend_analyzer.analyze_asset_trends('equity', 30)
        print(f"✓ 资产趋势分析成功: {len(asset_trends)} 个指标")
        
        return True
        
    except Exception as e:
        logger.error(f"趋势分析器测试失败: {e}")
        print(f"✗ 趋势分析器测试失败: {e}")
        return False

def test_visualizer():
    """测试可视化器"""
    print("\n测试可视化器...")
    logger = setup_logger('test_visualizer')
    
    try:
        visualizer = FlowVisualizer()
        
        # 测试全球资金流向图表创建
        flow_data = {
            'forex': {'total_net_flow': 150.5},
            'stock': {'total_net_flow': -45.2},
            'bond': {'total_net_flow': 85.3},
            'commodity': {'total_net_flow': 25.8}
        }
        
        chart_path = visualizer.create_global_flow_chart(flow_data)
        print(f"✓ 全球资金流向图表创建成功: {chart_path}")
        
        # 测试市场热力图创建
        market_data = {}
        heatmap_path = visualizer.create_market_heatmap(market_data)
        print(f"✓ 市场热力图创建成功: {heatmap_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"可视化器测试失败: {e}")
        print(f"✗ 可视化器测试失败: {e}")
        return False

def test_predictor():
    """测试预测器"""
    print("\n测试预测器...")
    logger = setup_logger('test_predictor')
    
    try:
        predictor = FlowPredictor()
        
        # 测试资金流向趋势预测
        historical_data = {}
        flow_prediction = predictor.predict_flow_trend(historical_data, 7)
        print(f"✓ 资金流向趋势预测成功: {len(flow_prediction)} 个预测指标")
        
        # 测试市场走势预测
        market_prediction = predictor.predict_market_movement(historical_data, 7)
        print(f"✓ 市场走势预测成功: {len(market_prediction)} 个预测指标")
        
        # 测试行业表现预测
        sector_prediction = predictor.predict_sector_performance(historical_data, 7)
        print(f"✓ 行业表现预测成功: {len(sector_prediction)} 个预测指标")
        
        return True
        
    except Exception as e:
        logger.error(f"预测器测试失败: {e}")
        print(f"✗ 预测器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("全球资金流向分析系统测试")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("数据库连接", test_database),
        ("数据收集器", test_data_collector),
        ("资金流向分析器", test_flow_analyzer),
        ("趋势分析器", test_trend_analyzer),
        ("可视化器", test_visualizer),
        ("预测器", test_predictor)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"正在测试: {test_name}")
        if test_func():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常。")
    else:
        print("⚠️  部分测试失败，请检查相关配置。")
    
    print("=" * 60)

if __name__ == '__main__':
    main() 