"""
万得行业分类模块完整功能测试
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_all():
    """测试所有功能"""
    print("=== 万得行业分类模块完整测试 ===")
    
    results = {}
    
    # 测试核心功能
    try:
        from core.industry_classifier import IndustryClassifier
        classifier = IndustryClassifier()
        classifier.initialize_database()
        print("✓ 核心功能测试通过")
        results['核心功能'] = True
    except Exception as e:
        print(f"❌ 核心功能测试失败: {e}")
        results['核心功能'] = False
    
    # 测试数据库
    try:
        from utils.database import db_manager
        result = db_manager.execute_query("SELECT 1")
        print("✓ 数据库测试通过")
        results['数据库'] = True
    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
        results['数据库'] = False
    
    # 测试管理台
    try:
        # 检查管理台文件是否存在
        if os.path.exists('dashboard.py'):
            print("✓ 管理台文件存在")
            results['管理台'] = True
        else:
            print("❌ 管理台文件不存在")
            results['管理台'] = False
    except Exception as e:
        print(f"❌ 管理台测试失败: {e}")
        results['管理台'] = False
    
    # 输出结果
    print(f"\n测试结果: {sum(results.values())}/{len(results)} 通过")
    return all(results.values())

if __name__ == "__main__":
    success = test_all()
    sys.exit(0 if success else 1) 