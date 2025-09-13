"""
国外热点数据模块测试脚本
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.logger import Logger
from core.international_hotspot_manager import InternationalHotspotManager
from config import Config

def test_database_connection():
    """测试数据库连接"""
    print("=== 测试数据库连接 ===")
    manager = InternationalHotspotManager()
    
    try:
        success = manager.test_connection()
        if success:
            print("✅ 数据库连接成功")
        else:
            print("❌ 数据库连接失败")
        return success
    except Exception as e:
        print(f"❌ 数据库连接异常: {e}")
        return False

def test_data_collection():
    """测试数据收集"""
    print("\n=== 测试数据收集 ===")
    manager = InternationalHotspotManager()
    
    try:
        success = manager.run_test_collection()
        if success:
            print("✅ 测试数据收集成功")
        else:
            print("❌ 测试数据收集失败")
        return success
    except Exception as e:
        print(f"❌ 数据收集异常: {e}")
        return False

def test_data_retrieval():
    """测试数据获取"""
    print("\n=== 测试数据获取 ===")
    manager = InternationalHotspotManager()
    
    try:
        # 获取热点数据
        hotspots = manager.get_hotspots(limit=10)
        print(f"✅ 获取到 {len(hotspots)} 条热点数据")
        
        # 获取统计数据
        stats = manager.get_statistics()
        print(f"✅ 统计数据: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ 数据获取异常: {e}")
        return False

def test_configuration():
    """测试配置"""
    print("\n=== 测试配置 ===")
    
    try:
        print(f"数据库配置: {Config.DATABASE}")
        print(f"Web服务配置: {Config.WEB}")
        print(f"数据源数量: {len([s for sources in Config.DATA_SOURCES.values() for s in sources if s.get('enabled')])}")
        print("✅ 配置加载成功")
        return True
    except Exception as e:
        print(f"❌ 配置加载异常: {e}")
        return False

def main():
    """主测试函数"""
    # 初始化日志
    Logger.setup()
    
    print("开始测试国外热点数据模块...\n")
    
    tests = [
        test_configuration,
        test_database_connection,
        test_data_collection,
        test_data_retrieval
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ 测试执行异常: {e}")
            results.append(False)
    
    # 输出测试结果
    print("\n=== 测试结果汇总 ===")
    passed = sum(results)
    total = len(results)
    
    print(f"通过测试: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return True
    else:
        print("⚠️  部分测试失败，请检查配置和依赖")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 