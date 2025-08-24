"""
简化测试文件
逐步测试各个组件
"""

import sys
from core.data_collector import DataCollector
from core.data_processor import DataProcessor
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus
from datetime import datetime

def test_step1_collector():
    """测试步骤1: 采集器"""
    print("步骤1: 测试数据采集器...")
    
    try:
        collector = DataCollector()
        
        # 分别测试各种类型的数据采集
        print("  测试新闻热点采集...")
        news_hotspots = collector.collect_news_hotspots()
        print(f"    采集到 {len(news_hotspots)} 条新闻热点")
        
        print("  测试政策热点采集...")
        policy_hotspots = collector.collect_policy_hotspots()
        print(f"    采集到 {len(policy_hotspots)} 条政策热点")
        
        print("  测试行业热点采集...")
        industry_hotspots = collector.collect_industry_hotspots()
        print(f"    采集到 {len(industry_hotspots)} 条行业热点")
        
        print("  测试市场热点采集...")
        market_hotspots = collector.collect_market_hotspots()
        print(f"    采集到 {len(market_hotspots)} 条市场热点")
        
        # 合并所有热点
        all_hotspots = news_hotspots + policy_hotspots + industry_hotspots + market_hotspots
        print(f"  总共采集到 {len(all_hotspots)} 条热点数据")
        
        return all_hotspots
        
    except Exception as e:
        print(f"  ❌ 采集器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return []

def test_step2_processor(hotspots):
    """测试步骤2: 处理器"""
    print("\n步骤2: 测试数据处理器...")
    
    if not hotspots:
        print("  ⚠️ 没有热点数据，跳过处理器测试")
        return []
    
    try:
        processor = DataProcessor()
        
        print(f"  开始处理 {len(hotspots)} 条热点数据...")
        
        # 逐个处理热点，便于定位问题
        processed_hotspots = []
        for i, hotspot in enumerate(hotspots):
            try:
                print(f"    处理第 {i+1} 条热点: {hotspot.title[:30]}...")
                
                # 单独处理每个热点
                processed = processor.process_hotspots([hotspot])
                if processed:
                    processed_hotspots.extend(processed)
                    print(f"      ✅ 处理成功")
                else:
                    print(f"      ⚠️ 处理失败")
                    
            except Exception as e:
                print(f"      ❌ 处理失败: {e}")
                # 继续处理下一个
                continue
        
        print(f"  成功处理 {len(processed_hotspots)} 条热点数据")
        return processed_hotspots
        
    except Exception as e:
        print(f"  ❌ 处理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return []

def test_step3_analysis(hotspots):
    """测试步骤3: 分析功能"""
    print("\n步骤3: 测试分析功能...")
    
    if not hotspots:
        print("  ⚠️ 没有热点数据，跳过分析测试")
        return False
    
    try:
        processor = DataProcessor()
        
        print(f"  开始分析 {len(hotspots)} 条热点数据...")
        
        # 测试趋势分析
        analysis = processor.analyze_hotspots_trend(hotspots)
        print(f"  ✅ 趋势分析完成")
        print(f"    总数: {analysis['total_count']}")
        print(f"    类型分布: {analysis['by_type']}")
        print(f"    级别分布: {analysis['by_level']}")
        print(f"    平均热度: {analysis['avg_heat']:.2f}")
        print(f"    平均情感: {analysis['avg_sentiment']:.2f}")
        
        # 测试数据过滤
        filtered = processor.filter_hotspots(hotspots, hotspot_type='news')
        print(f"  ✅ 数据过滤完成: {len(filtered)} 条新闻热点")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 分析测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("国内热点数据模块 - 简化测试")
    print("=" * 60)
    
    # 步骤1: 测试采集器
    hotspots = test_step1_collector()
    
    # 步骤2: 测试处理器
    processed_hotspots = test_step2_processor(hotspots)
    
    # 步骤3: 测试分析功能
    analysis_ok = test_step3_analysis(processed_hotspots)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    print(f"  采集数据: {len(hotspots)} 条")
    print(f"  处理数据: {len(processed_hotspots)} 条")
    print(f"  分析功能: {'✅ 正常' if analysis_ok else '❌ 失败'}")
    
    if len(processed_hotspots) > 0 and analysis_ok:
        print("\n🎉 简化测试通过！模块基本功能正常！")
        return True
    else:
        print("\n⚠️ 简化测试失败，需要进一步调试")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 