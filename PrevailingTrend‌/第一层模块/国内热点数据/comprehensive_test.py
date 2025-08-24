"""
国内热点数据模块 - 综合测试
测试所有核心功能，包括数据采集、处理、存储和分析
"""

import sys
import os
from datetime import datetime
from loguru import logger

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.data_collector import DataCollector
from core.data_processor import DataProcessor
from core.data_generator import DataGenerator
from core.real_data_collector import RealDataCollector
from core.data_storage import DataStorage
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus

def test_data_collection():
    """测试数据采集功能"""
    print("=" * 60)
    print("测试数据采集功能")
    print("=" * 60)
    
    try:
        # 测试基础采集器
        print("1. 测试基础数据采集器...")
        collector = DataCollector()
        
        news_hotspots = collector.collect_news_hotspots()
        print(f"   ✅ 新闻热点: {len(news_hotspots)} 条")
        
        policy_hotspots = collector.collect_policy_hotspots()
        print(f"   ✅ 政策热点: {len(policy_hotspots)} 条")
        
        industry_hotspots = collector.collect_industry_hotspots()
        print(f"   ✅ 行业热点: {len(industry_hotspots)} 条")
        
        market_hotspots = collector.collect_market_hotspots()
        print(f"   ✅ 市场热点: {len(market_hotspots)} 条")
        
        all_hotspots = news_hotspots + policy_hotspots + industry_hotspots + market_hotspots
        print(f"   📊 总计: {len(all_hotspots)} 条热点数据")
        
        # 测试数据生成器
        print("\n2. 测试数据生成器...")
        generator = DataGenerator()
        generated_hotspots = generator.generate_large_dataset()
        print(f"   ✅ 生成数据: {len(generated_hotspots)} 条")
        
        # 测试真实数据采集器
        print("\n3. 测试真实数据采集器...")
        real_collector = RealDataCollector()
        real_hotspots = real_collector.collect_real_hotspots()
        print(f"   ✅ 真实数据: {len(real_hotspots)} 条")
        
        return all_hotspots + generated_hotspots + real_hotspots
        
    except Exception as e:
        print(f"   ❌ 数据采集测试失败: {e}")
        import traceback
        traceback.print_exc()
        return []

def test_data_processing(hotspots):
    """测试数据处理功能"""
    print("\n" + "=" * 60)
    print("测试数据处理功能")
    print("=" * 60)
    
    if not hotspots:
        print("⚠️ 没有热点数据，跳过处理测试")
        return []
    
    try:
        processor = DataProcessor()
        
        print(f"开始处理 {len(hotspots)} 条热点数据...")
        
        # 批量处理
        processed_hotspots = processor.process_hotspots(hotspots)
        print(f"✅ 处理完成: {len(processed_hotspots)} 条")
        
        # 显示处理结果统计
        if processed_hotspots:
            print("\n处理结果统计:")
            
            # 按类型统计
            type_stats = {}
            for hotspot in processed_hotspots:
                type_name = hotspot.hotspot_type.value
                type_stats[type_name] = type_stats.get(type_name, 0) + 1
            
            print("  按类型分布:")
            for type_name, count in type_stats.items():
                print(f"    {type_name}: {count} 条")
            
            # 按级别统计
            level_stats = {}
            for hotspot in processed_hotspots:
                level_name = hotspot.hotspot_level.value
                level_stats[level_name] = level_stats.get(level_name, 0) + 1
            
            print("  按级别分布:")
            for level_name, count in level_stats.items():
                print(f"    {level_name}: {count} 条")
            
            # 热度统计
            heat_scores = [h.heat_score for h in processed_hotspots if h.heat_score is not None]
            if heat_scores:
                avg_heat = sum(heat_scores) / len(heat_scores)
                max_heat = max(heat_scores)
                min_heat = min(heat_scores)
                print(f"  热度统计: 平均={avg_heat:.1f}, 最高={max_heat:.1f}, 最低={min_heat:.1f}")
            
            # 情感统计
            sentiment_scores = [h.sentiment_score for h in processed_hotspots if h.sentiment_score is not None]
            if sentiment_scores:
                avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
                print(f"  情感统计: 平均={avg_sentiment:.3f}")
        
        return processed_hotspots
        
    except Exception as e:
        print(f"❌ 数据处理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return []

def test_data_analysis(hotspots):
    """测试数据分析功能"""
    print("\n" + "=" * 60)
    print("测试数据分析功能")
    print("=" * 60)
    
    if not hotspots:
        print("⚠️ 没有热点数据，跳过分析测试")
        return False
    
    try:
        processor = DataProcessor()
        
        print("1. 测试趋势分析...")
        analysis = processor.analyze_hotspots_trend(hotspots)
        print(f"   ✅ 趋势分析完成")
        print(f"   总数: {analysis['total_count']}")
        print(f"   类型分布: {analysis['by_type']}")
        print(f"   级别分布: {analysis['by_level']}")
        print(f"   平均热度: {analysis['avg_heat']:.2f}")
        print(f"   平均情感: {analysis['avg_sentiment']:.3f}")
        
        if analysis['top_keywords']:
            print(f"   热门关键词: {[kw[0] for kw in analysis['top_keywords'][:5]]}")
        
        if analysis['top_companies']:
            print(f"   热门公司: {[comp[0] for comp in analysis['top_companies'][:5]]}")
        
        print("\n2. 测试数据过滤...")
        
        # 测试各种过滤条件
        filters = [
            ('news', '新闻热点'),
            ('policy', '政策热点'),
            ('industry', '行业热点'),
            ('market', '市场热点')
        ]
        
        for filter_type, filter_name in filters:
            filtered = processor.filter_hotspots(hotspots, hotspot_type=filter_type)
            print(f"   {filter_name}: {len(filtered)} 条")
        
        # 测试热度过滤
        high_heat = processor.filter_hotspots(hotspots, min_heat_score=70)
        print(f"   高热度热点(≥70): {len(high_heat)} 条")
        
        # 测试情感过滤
        positive = processor.filter_hotspots(hotspots, min_sentiment_score=0.3)
        print(f"   正面情感(≥0.3): {len(positive)} 条")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据分析测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_storage(hotspots):
    """测试数据存储功能"""
    print("\n" + "=" * 60)
    print("测试数据存储功能")
    print("=" * 60)
    
    if not hotspots:
        print("⚠️ 没有热点数据，跳过存储测试")
        return False
    
    try:
        storage = DataStorage()
        
        print("1. 测试数据保存...")
        success_count = storage.batch_insert_hotspots(hotspots)
        print(f"   ✅ 保存成功: {success_count} 条")
        
        print("\n2. 测试数据查询...")
        result = storage.get_hotspots_from_db(page=1, per_page=10)
        print(f"   ✅ 查询成功: {len(result['hotspots'])} 条")
        print(f"   总数: {result['total']}")
        print(f"   当前页: {result['page']}")
        print(f"   每页数量: {result['per_page']}")
        
        if result['hotspots']:
            print("   示例数据:")
            for i, hotspot in enumerate(result['hotspots'][:3]):
                print(f"     {i+1}. {hotspot.title[:50]}...")
                print(f"        类型: {hotspot.hotspot_type.value}")
                print(f"        热度: {hotspot.heat_score}")
                print(f"        情感: {hotspot.sentiment_score}")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据存储测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("国内热点数据模块 - 综合功能测试")
    print("测试时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    test_results = []
    
    # 1. 测试数据采集
    hotspots = test_data_collection()
    test_results.append(len(hotspots) > 0)
    
    # 2. 测试数据处理
    processed_hotspots = test_data_processing(hotspots)
    test_results.append(len(processed_hotspots) > 0)
    
    # 3. 测试数据分析
    analysis_ok = test_data_analysis(processed_hotspots)
    test_results.append(analysis_ok)
    
    # 4. 测试数据存储
    storage_ok = test_data_storage(processed_hotspots)
    test_results.append(storage_ok)
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("综合测试结果汇总")
    print("=" * 60)
    
    test_names = [
        "数据采集",
        "数据处理", 
        "数据分析",
        "数据存储"
    ]
    
    passed = 0
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{i+1}. {name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总体结果: {passed}/{len(test_results)} 项测试通过")
    
    if passed == len(test_results):
        print("\n🎉 所有测试通过！国内热点数据模块功能完整！")
        print("\n模块功能验证:")
        print("✅ 支持多种数据源采集")
        print("✅ 智能数据处理和分析")
        print("✅ 完整的数据存储和查询")
        print("✅ 丰富的过滤和统计功能")
        print("\n下一步建议:")
        print("1. 运行 'python start.py' 启动完整服务")
        print("2. 访问 http://localhost:5002 查看Web管理台")
        print("3. 配置真实数据源进行生产环境部署")
    else:
        print(f"\n⚠️ 有 {len(test_results) - passed} 项测试失败，需要修复")
    
    return passed == len(test_results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 