"""
万得行业分类模块简单测试
"""

import os
import sys

def test_files_exist():
    """测试关键文件是否存在"""
    print("=== 文件存在性测试 ===")
    
    required_files = [
        'dashboard.py',
        'run_dashboard.py',
        'templates/dashboard.html',
        'core/industry_classifier.py',
        'utils/database.py',
        'utils/logger.py',
        'models/industry_model.py',
        'models/stock_industry_model.py'
    ]
    
    results = {}
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
            results[file_path] = True
        else:
            print(f"❌ {file_path}")
            results[file_path] = False
    
    return results

def test_dashboard_startup():
    """测试管理台启动"""
    print("\n=== 管理台启动测试 ===")
    
    try:
        # 检查templates目录
        if not os.path.exists('templates'):
            os.makedirs('templates')
            print("✓ 创建templates目录")
        
        # 检查dashboard.html
        if os.path.exists('templates/dashboard.html'):
            print("✓ dashboard.html模板存在")
            return True
        else:
            print("❌ dashboard.html模板不存在")
            return False
    except Exception as e:
        print(f"❌ 管理台启动测试失败: {e}")
        return False

def test_config():
    """测试配置文件"""
    print("\n=== 配置测试 ===")
    
    config_files = ['config.py', 'env.example']
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✓ {config_file} 存在")
        else:
            print(f"❌ {config_file} 不存在")

def main():
    """主测试函数"""
    print("万得行业分类模块简单测试")
    print("="*50)
    
    # 测试文件存在性
    file_results = test_files_exist()
    
    # 测试管理台
    dashboard_ok = test_dashboard_startup()
    
    # 测试配置
    test_config()
    
    # 输出总结
    print("\n=== 测试总结 ===")
    total_files = len(file_results)
    existing_files = sum(file_results.values())
    
    print(f"文件存在性: {existing_files}/{total_files}")
    print(f"管理台启动: {'✓' if dashboard_ok else '❌'}")
    
    if existing_files == total_files and dashboard_ok:
        print("\n🎉 所有测试通过！模块结构完整。")
        return True
    else:
        print("\n⚠️ 部分测试失败，请检查缺失的文件。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 