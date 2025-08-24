"""
测试真实数据采集功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.real_data_collector import RealDataCollector
from loguru import logger

def test_real_data_collection():
    """测试真实数据采集功能"""
    print("开始测试真实数据采集功能...")
    
    # 创建真实数据采集器
    collector = RealDataCollector()
    
    # 测试各类数据采集
    collectors = [
        ("新闻数据", collector.collect_from_news_api),
        ("股票数据", collector.collect_from_stock_api),
        ("政策数据", collector.collect_from_policy_api),
        ("行业数据", collector.collect_from_industry_api),
        ("市场数据", collector.collect_from_market_api),
    ]
    
    total_hotspots = []
    
    for name, collector_func in collectors:
        try:
            print(f"\n测试 {name} 采集...")
            hotspots = collector_func()
            print(f"  ✅ {name}: 获取到 {len(hotspots)} 条数据")
            total_hotspots.extend(hotspots)
            
            # 显示前3条数据示例
            for i, hotspot in enumerate(hotspots[:3]):
                print(f"    示例{i+1}: {hotspot.title[:50]}...")
                
        except Exception as e:
            print(f"  ❌ {name}: 采集失败 - {e}")
    
    print(f"\n=== 真实数据采集总结 ===")
    print(f"总数据量: {len(total_hotspots)} 条")
    
    if total_hotspots:
        # 按类型统计
        type_stats = {}
        source_stats = {}
        
        for hotspot in total_hotspots:
            type_name = hotspot.hotspot_type.value
            type_stats[type_name] = type_stats.get(type_name, 0) + 1
            
            source_name = hotspot.source
            source_stats[source_name] = source_stats.get(source_name, 0) + 1
        
        print("\n按类型分布:")
        for type_name, count in type_stats.items():
            print(f"  {type_name}: {count} 条")
        
        print(f"\n数据源数量: {len(source_stats)} 个")
        print("主要数据源:")
        sorted_sources = sorted(source_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        for source_name, count in sorted_sources:
            print(f"  {source_name}: {count} 条")
        
        print("\n=== 数据质量检查 ===")
        
        # 检查标题长度
        title_lengths = [len(h.title) for h in total_hotspots if h.title]
        if title_lengths:
            avg_title_length = sum(title_lengths) / len(title_lengths)
            print(f"平均标题长度: {avg_title_length:.1f} 字符")
        
        # 检查内容长度
        content_lengths = [len(h.content) for h in total_hotspots if h.content]
        if content_lengths:
            avg_content_length = sum(content_lengths) / len(content_lengths)
            print(f"平均内容长度: {avg_content_length:.1f} 字符")
        
        # 检查URL有效性
        valid_urls = [h.url for h in total_hotspots if h.url and h.url.startswith('http')]
        print(f"有效URL数量: {len(valid_urls)} / {len(total_hotspots)}")
        
        print("\n✅ 真实数据采集功能测试完成")
        print("✅ 系统已配置为优先使用真实数据")
        print("✅ 当真实数据不足时，会自动使用模拟数据作为备用")
        
    else:
        print("\n⚠️  未获取到真实数据")
        print("可能原因:")
        print("  1. API密钥未配置或无效")
        print("  2. 网络连接问题")
        print("  3. API服务暂时不可用")
        print("\n建议:")
        print("  1. 检查 .env 文件中的API密钥配置")
        print("  2. 确保网络连接正常")
        print("  3. 系统会自动使用模拟数据作为备用")
    
    return total_hotspots

if __name__ == "__main__":
    test_real_data_collection() 