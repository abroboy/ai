#!/usr/bin/env python3
"""
国内热点数据模块测试脚本
"""

import sys
import os
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus
from core.data_collector import DataCollector
from core.data_processor import DataProcessor


def test_config():
    """测试配置"""
    print("测试配置...")
    print(f"数据库配置: {config.DATABASE}")
    print(f"Web配置: {config.WEB}")
    print(f"数据源配置: {len(config.DATA_SOURCES['news_sources'])} 个新闻源")
    print(f"分析配置: {config.ANALYSIS}")
    print("✅ 配置测试通过")


def test_models():
    """测试数据模型"""
    print("\n测试数据模型...")
    
    try:
        # 创建热点模型
        hotspot = HotspotModel(
            hotspot_id="test_001",
            title="测试热点标题",
            content="这是一个测试热点内容",
            hotspot_type=HotspotType.NEWS,
            hotspot_level=HotspotLevel.MEDIUM,
            status=HotspotStatus.ACTIVE,
            source="测试源",
            url="http://test.com",
            publish_time=datetime.now(),
            keywords=["测试", "热点"],
            related_companies=["测试公司"],
            related_industries=["801080"],
            sentiment_score=0.5,
            heat_score=75.0,
            update_date=datetime.now()
        )
        
        print(f"✅ 热点模型创建成功: {hotspot.hotspot_id}")
        print(f"   标题: {hotspot.title}")
        print(f"   类型: {hotspot.hotspot_type.value}")
        print(f"   级别: {hotspot.hotspot_level.value}")
        print(f"   热度: {hotspot.heat_score}")
        print(f"   情感: {hotspot.sentiment_score}")
        
        # 测试转换方法
        hotspot_dict = hotspot.to_dict()
        print(f"✅ 转换为字典成功: {len(hotspot_dict)} 个字段")
        
        # 测试从字典创建
        hotspot_from_dict = HotspotModel.from_dict(hotspot_dict)
        print(f"✅ 从字典创建成功: {hotspot_from_dict.hotspot_id}")
        
        # 测试判断方法
        print(f"   是否活跃: {hotspot.is_active()}")
        print(f"   是否高热度: {hotspot.is_high_heat()}")
        print(f"   是否正面情感: {hotspot.is_positive_sentiment()}")
        print(f"   情感标签: {hotspot.get_sentiment_label()}")
        print(f"   热度标签: {hotspot.get_heat_label()}")
        
    except Exception as e:
        print(f"❌ 数据模型测试失败: {e}")
        return False
    
    return True


def test_data_collector():
    """测试数据采集器"""
    print("\n测试数据采集器...")
    
    try:
        collector = DataCollector()
        
        # 测试新闻热点采集
        news_hotspots = collector.collect_news_hotspots()
        print(f"✅ 新闻热点采集成功: {len(news_hotspots)} 条")
        
        # 测试政策热点采集
        policy_hotspots = collector.collect_policy_hotspots()
        print(f"✅ 政策热点采集成功: {len(policy_hotspots)} 条")
        
        # 测试全部热点采集
        all_hotspots = collector.collect_all_hotspots()
        print(f"✅ 全部热点采集成功: {len(all_hotspots)} 条")
        
        # 显示部分热点信息
        for i, hotspot in enumerate(all_hotspots[:3]):
            print(f"   热点 {i+1}: {hotspot.title[:30]}...")
            print(f"     类型: {hotspot.hotspot_type.value}")
            print(f"     来源: {hotspot.source}")
            print(f"     热度: {hotspot.heat_score}")
        
    except Exception as e:
        print(f"❌ 数据采集器测试失败: {e}")
        return False
    
    return True


def test_data_processor():
    """测试数据处理器"""
    print("\n测试数据处理器...")
    
    try:
        processor = DataProcessor()
        collector = DataCollector()
        
        # 获取原始热点数据
        raw_hotspots = collector.collect_all_hotspots()
        print(f"✅ 获取原始热点数据: {len(raw_hotspots)} 条")
        
        # 处理热点数据
        processed_hotspots = processor.process_hotspots(raw_hotspots)
        print(f"✅ 处理热点数据成功: {len(processed_hotspots)} 条")
        
        # 显示处理结果
        for i, hotspot in enumerate(processed_hotspots[:3]):
            print(f"   处理后的热点 {i+1}:")
            print(f"     标题: {hotspot.title[:30]}...")
            print(f"     关键词: {hotspot.keywords}")
            print(f"     相关公司: {hotspot.related_companies}")
            print(f"     热度: {hotspot.heat_score}")
            print(f"     情感: {hotspot.sentiment_score}")
            print(f"     状态: {hotspot.status.value}")
        
        # 测试趋势分析
        analysis = processor.analyze_hotspots_trend(processed_hotspots)
        print(f"✅ 趋势分析成功:")
        print(f"   总数: {analysis['total_count']}")
        print(f"   平均热度: {analysis['avg_heat']}")
        print(f"   平均情感: {analysis['avg_sentiment']}")
        print(f"   类型分布: {analysis['by_type']}")
        
        # 测试数据过滤
        filtered_hotspots = processor.filter_hotspots(
            processed_hotspots,
            hotspot_type='news',
            min_heat_score=50
        )
        print(f"✅ 数据过滤成功: {len(filtered_hotspots)} 条")
        
    except Exception as e:
        print(f"❌ 数据处理器测试失败: {e}")
        return False
    
    return True


def test_integration():
    """测试集成功能"""
    print("\n测试集成功能...")
    
    try:
        # 完整的采集-处理流程
        collector = DataCollector()
        processor = DataProcessor()
        
        print("1. 开始数据采集...")
        raw_hotspots = collector.collect_all_hotspots()
        print(f"   采集完成: {len(raw_hotspots)} 条")
        
        print("2. 开始数据处理...")
        processed_hotspots = processor.process_hotspots(raw_hotspots)
        print(f"   处理完成: {len(processed_hotspots)} 条")
        
        print("3. 开始数据分析...")
        analysis = processor.analyze_hotspots_trend(processed_hotspots)
        print(f"   分析完成: {analysis['total_count']} 条数据")
        
        print("4. 生成报告...")
        print(f"   热点类型分布: {analysis['by_type']}")
        print(f"   热度级别分布: {analysis['by_level']}")
        print(f"   数据来源分布: {analysis['by_source']}")
        print(f"   平均热度得分: {analysis['avg_heat']:.2f}")
        print(f"   平均情感得分: {analysis['avg_sentiment']:.2f}")
        
        if analysis['top_keywords']:
            print(f"   热门关键词: {[kw[0] for kw in analysis['top_keywords'][:5]]}")
        
        if analysis['top_companies']:
            print(f"   热门公司: {[comp[0] for comp in analysis['top_companies'][:5]]}")
        
        print("✅ 集成测试完成")
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False
    
    return True


def main():
    """主测试函数"""
    print("=" * 60)
    print("国内热点数据模块测试")
    print("=" * 60)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(test_config())
    test_results.append(test_models())
    test_results.append(test_data_collector())
    test_results.append(test_data_processor())
    test_results.append(test_integration())
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    passed = sum(test_results)
    total = len(test_results)
    print(f"通过: {passed}/{total}")
    
    test_names = [
        "配置测试",
        "数据模型测试",
        "数据采集器测试",
        "数据处理器测试",
        "集成测试"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    if passed == total:
        print("\n🎉 所有测试通过！国内热点数据模块功能正常！")
        print("\n下一步:")
        print("1. 运行 'python start.py' 启动完整服务")
        print("2. 访问 http://localhost:5002 查看Web管理台")
        print("3. 运行 'python hotspot_test.py' 进行数据库测试")
    else:
        print(f"\n⚠️  有 {total - passed} 项测试失败，需要修复")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 