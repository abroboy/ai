"""
测试数据存储和更新功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.data_storage import DataStorage
from core.data_updater import DataUpdater
from core.web_scraper import WebScraper
from loguru import logger

def test_data_storage():
    """测试数据存储功能"""
    print("开始测试数据存储功能...")
    
    # 创建数据存储实例
    storage = DataStorage()
    
    # 创建数据表
    print("1. 创建数据表...")
    storage.create_table_if_not_exists()
    
    # 测试爬虫获取数据
    print("2. 测试爬虫获取数据...")
    scraper = WebScraper()
    hotspots = scraper.scrape_all_sources()
    print(f"   爬虫获取到 {len(hotspots)} 条数据")
    
    if hotspots:
        # 保存到数据库
        print("3. 保存数据到数据库...")
        saved_count = storage.save_hotspots(hotspots)
        print(f"   成功保存 {saved_count} 条数据")
        
        # 从数据库读取数据
        print("4. 从数据库读取数据...")
        result = storage.get_hotspots_from_db(page=1, per_page=10)
        print(f"   读取到 {len(result['hotspots'])} 条数据，总计 {result['total']} 条")
        
        # 获取统计数据
        print("5. 获取统计数据...")
        stats = storage.get_statistics()
        print(f"   总数据量: {stats['total']}")
        print(f"   今日数据: {stats['today_count']}")
        print(f"   类型分布: {stats['type_distribution']}")
        print(f"   来源分布: {stats['source_distribution']}")
        
        # 测试详情获取
        if result['hotspots']:
            print("6. 测试详情获取...")
            first_hotspot = result['hotspots'][0]
            detail = storage.get_hotspot_detail(first_hotspot.hotspot_id)
            if detail:
                print(f"   成功获取详情: {detail.title}")
            else:
                print("   获取详情失败")
        
        print("\n✅ 数据存储功能测试完成")
    else:
        print("⚠️  未获取到爬虫数据，跳过存储测试")
    
    return hotspots

def test_data_updater():
    """测试数据更新功能"""
    print("\n开始测试数据更新功能...")
    
    # 创建数据更新器
    updater = DataUpdater()
    
    # 测试手动更新
    print("1. 测试手动数据更新...")
    result = updater.manual_update()
    print(f"   更新结果: {result}")
    
    # 测试获取更新状态
    print("2. 测试获取更新状态...")
    status = updater.get_update_status()
    print(f"   更新状态: {status}")
    
    print("\n✅ 数据更新功能测试完成")
    
    return result

def test_full_workflow():
    """测试完整工作流程"""
    print("\n开始测试完整工作流程...")
    
    # 1. 创建数据存储
    storage = DataStorage()
    storage.create_table_if_not_exists()
    
    # 2. 创建数据更新器
    updater = DataUpdater()
    
    # 3. 执行数据更新
    print("1. 执行数据更新...")
    result = updater.manual_update()
    
    if result['success']:
        print(f"   更新成功: {result['message']}")
        
        # 4. 验证数据存储
        print("2. 验证数据存储...")
        stats = storage.get_statistics()
        print(f"   数据库中的数据量: {stats['total']}")
        
        # 5. 测试数据读取
        print("3. 测试数据读取...")
        result = storage.get_hotspots_from_db(page=1, per_page=5)
        print(f"   读取到 {len(result['hotspots'])} 条数据")
        
        if result['hotspots']:
            print("   数据示例:")
            for i, hotspot in enumerate(result['hotspots'][:3]):
                print(f"     {i+1}. {hotspot.title[:50]}... (来源: {hotspot.source})")
        
        print("\n✅ 完整工作流程测试成功")
    else:
        print(f"   更新失败: {result['error']}")
        print("\n⚠️  完整工作流程测试失败")
    
    return result

if __name__ == "__main__":
    print("=== 数据存储和更新功能测试 ===\n")
    
    # 测试数据存储
    test_data_storage()
    
    # 测试数据更新
    test_data_updater()
    
    # 测试完整工作流程
    test_full_workflow()
    
    print("\n=== 测试完成 ===") 