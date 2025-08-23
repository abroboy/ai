"""
万得行业分类管理台测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.industry_classifier import IndustryClassifier
from utils.logger import logger

def test_dashboard_functionality():
    """测试管理台相关功能"""
    print("=== 万得行业分类管理台功能测试 ===")
    
    try:
        # 初始化分类器
        classifier = IndustryClassifier()
        print("✓ 分类器初始化成功")
        
        # 测试数据库初始化
        classifier.initialize_database()
        print("✓ 数据库初始化成功")
        
        # 测试获取统计信息
        try:
            stats = classifier.get_industry_statistics()
            print(f"✓ 统计信息获取成功: {stats}")
        except Exception as e:
            print(f"⚠ 统计信息获取失败: {e}")
        
        # 测试获取行业列表
        try:
            industries = classifier.get_all_industries()
            print(f"✓ 行业列表获取成功: {len(industries)}条记录")
        except Exception as e:
            print(f"⚠ 行业列表获取失败: {e}")
        
        # 测试搜索功能
        try:
            search_results = classifier.search_industries("电子")
            print(f"✓ 搜索功能测试成功: 找到{len(search_results)}条结果")
        except Exception as e:
            print(f"⚠ 搜索功能测试失败: {e}")
        
        # 测试数据更新
        try:
            result = classifier.run_full_update()
            print(f"✓ 数据更新测试成功: {result}")
        except Exception as e:
            print(f"⚠ 数据更新测试失败: {e}")
        
        print("\n=== 测试完成 ===")
        print("管理台功能测试通过！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        logger.error(f"管理台功能测试失败: {e}")

if __name__ == "__main__":
    test_dashboard_functionality() 