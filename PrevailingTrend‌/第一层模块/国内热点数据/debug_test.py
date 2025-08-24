"""
调试测试文件
用于定位TypeError错误
"""

from core.data_collector import DataCollector
from core.data_processor import DataProcessor
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus
from datetime import datetime

def test_single_hotspot():
    """测试单个热点处理"""
    print("测试单个热点处理...")
    
    try:
        # 创建一个简单的热点
        hotspot = HotspotModel(
            hotspot_id="debug_001",
            title="测试热点标题",
            content="测试热点内容",
            hotspot_type=HotspotType.NEWS,
            source="测试来源",
            publish_time=datetime.now()
        )
        
        print(f"✅ 热点创建成功: {hotspot.hotspot_id}")
        print(f"   标题: {hotspot.title}")
        print(f"   类型: {hotspot.hotspot_type.value}")
        print(f"   热度: {hotspot.heat_score}")
        print(f"   情感: {hotspot.sentiment_score}")
        
        # 测试处理器
        processor = DataProcessor()
        
        # 处理单个热点
        processed_hotspots = processor.process_hotspots([hotspot])
        
        print(f"✅ 处理成功: {len(processed_hotspots)} 条")
        
        if processed_hotspots:
            processed = processed_hotspots[0]
            print(f"   处理后热度: {processed.heat_score}")
            print(f"   处理后情感: {processed.sentiment_score}")
            print(f"   关键词: {processed.keywords}")
            print(f"   相关公司: {processed.related_companies}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_collector():
    """测试采集器"""
    print("\n测试采集器...")
    
    try:
        collector = DataCollector()
        
        # 只采集少量数据
        news_hotspots = collector.collect_news_hotspots()
        print(f"✅ 新闻热点采集: {len(news_hotspots)} 条")
        
        if news_hotspots:
            hotspot = news_hotspots[0]
            print(f"   第一个热点:")
            print(f"     标题: {hotspot.title}")
            print(f"     热度: {hotspot.heat_score}")
            print(f"     情感: {hotspot.sentiment_score}")
        
        return True
        
    except Exception as e:
        print(f"❌ 采集器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("开始调试测试...")
    
    # 测试1: 单个热点处理
    test1_ok = test_single_hotspot()
    
    # 测试2: 采集器
    test2_ok = test_collector()
    
    print(f"\n测试结果:")
    print(f"  单个热点处理: {'✅' if test1_ok else '❌'}")
    print(f"  采集器测试: {'✅' if test2_ok else '❌'}")
    
    if test1_ok and test2_ok:
        print("\n🎉 所有测试通过！")
    else:
        print("\n⚠️ 有测试失败")

if __name__ == "__main__":
    main() 