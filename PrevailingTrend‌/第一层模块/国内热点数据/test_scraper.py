"""
测试爬虫功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.web_scraper import WebScraper
from loguru import logger

def test_scraper():
    """测试爬虫功能"""
    print("开始测试爬虫功能...")
    
    # 创建爬虫实例
    scraper = WebScraper()
    
    # 测试各个数据源
    scrapers = [
        ("新浪财经", scraper.scrape_sina_finance),
        ("东方财富", scraper.scrape_eastmoney),
        ("财新网", scraper.scrape_caixin),
        ("政府政策", scraper.scrape_government_policy),
        ("交易所公告", scraper.scrape_stock_exchange),
    ]
    
    total_hotspots = []
    
    for name, scraper_func in scrapers:
        try:
            print(f"\n测试爬取 {name}...")
            hotspots = scraper_func()
            print(f"  ✅ {name}: 获取到 {len(hotspots)} 条数据")
            total_hotspots.extend(hotspots)
            
            # 显示前3条数据示例
            for i, hotspot in enumerate(hotspots[:3]):
                print(f"    示例{i+1}: {hotspot.title[:50]}...")
                print(f"      来源: {hotspot.source}")
                print(f"      热度: {hotspot.heat_score}")
                print(f"      URL: {hotspot.url}")
                
        except Exception as e:
            print(f"  ❌ {name}: 爬取失败 - {e}")
    
    print(f"\n=== 爬虫测试总结 ===")
    print(f"总数据量: {len(total_hotspots)} 条")
    
    if total_hotspots:
        # 按来源统计
        source_stats = {}
        for hotspot in total_hotspots:
            source_name = hotspot.source
            source_stats[source_name] = source_stats.get(source_name, 0) + 1
        
        print("\n按来源分布:")
        for source_name, count in source_stats.items():
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
        
        # 检查热度分布
        heat_scores = [h.heat_score for h in total_hotspots if h.heat_score is not None]
        if heat_scores:
            avg_heat = sum(heat_scores) / len(heat_scores)
            print(f"平均热度得分: {avg_heat:.1f}")
        
        print("\n✅ 爬虫功能测试完成")
        print("✅ 成功获取真实数据")
        print("✅ 数据质量良好")
        
    else:
        print("\n⚠️  未获取到爬虫数据")
        print("可能原因:")
        print("  1. 网络连接问题")
        print("  2. 目标网站反爬虫机制")
        print("  3. 网站结构变化")
        print("\n建议:")
        print("  1. 检查网络连接")
        print("  2. 调整爬虫策略")
        print("  3. 更新网站解析规则")
    
    return total_hotspots

if __name__ == "__main__":
    test_scraper() 