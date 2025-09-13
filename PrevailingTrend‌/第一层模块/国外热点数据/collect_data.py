"""
国外热点数据收集脚本
专门负责数据收集，与展示服务分离
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """主函数"""
    print("=" * 60)
    print("国外热点数据收集服务")
    print("=" * 60)
    
    try:
        # 导入必要的模块
        from utils.logger import Logger
        from core.international_hotspot_manager import InternationalHotspotManager
        
        # 初始化日志
        Logger.setup()
        logger = Logger.get_logger('DataCollector')
        
        # 初始化管理器
        manager = InternationalHotspotManager()
        
        print("1. 测试数据库连接...")
        if not manager.test_connection():
            print("❌ 数据库连接失败")
            return False
        print("✅ 数据库连接成功")
        
        print("\n2. 开始收集数据...")
        success = manager.run_collection()
        
        if success:
            print("✅ 数据收集完成")
            
            # 显示统计信息
            stats = manager.get_statistics()
            if stats:
                print(f"\n📊 数据统计:")
                print(f"   总数据量: {stats.get('total', 0)}")
                print(f"   新闻热点: {stats.get('by_type', {}).get('news', 0)}")
                print(f"   政策热点: {stats.get('by_type', {}).get('policy', 0)}")
        else:
            print("❌ 数据收集失败")
            return False
        
        print("\n3. 数据收集服务完成")
        return True
        
    except Exception as e:
        print(f"❌ 数据收集服务异常: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 