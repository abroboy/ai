"""
万得行业分类模块完整功能测试
测试所有核心功能和管理台功能
"""

import sys
import os
import time
import requests
import json
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_core_functionality():
    """测试核心功能"""
    print("=== 测试核心功能 ===")
    
    try:
        from core.industry_classifier import IndustryClassifier
        from utils.logger import logger
        
        # 初始化分类器
        classifier = IndustryClassifier()
        print("✓ 分类器初始化成功")
        
        # 测试数据库初始化
        classifier.initialize_database()
        print("✓ 数据库初始化成功")
        
        # 测试数据采集和验证
        result = classifier.collect_and_validate_data()
        print(f"✓ 数据采集验证成功: {len(result.get('industry_data', []))}条行业数据")
        
        # 测试统计信息
        stats = classifier.get_industry_statistics()
        print(f"✓ 统计信息获取成功: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ 核心功能测试失败: {e}")
        return False

def test_api_functionality():
    """测试API功能"""
    print("\n=== 测试API功能 ===")
    
    try:
        # 启动API服务器（在后台）
        import subprocess
        import threading
        
        def start_api_server():
            subprocess.run([sys.executable, "api_server.py", "--service", "combined"], 
                         capture_output=True, text=True)
        
        # 启动API服务器
        api_thread = threading.Thread(target=start_api_server, daemon=True)
        api_thread.start()
        
        # 等待服务器启动
        time.sleep(3)
        
        # 测试API接口
        base_url = "http://localhost:5000"
        
        # 测试健康检查
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✓ API健康检查通过")
        else:
            print("❌ API健康检查失败")
            return False
        
        # 测试行业API
        response = requests.get(f"{base_url}/industry/api/industries", timeout=5)
        if response.status_code == 200:
            print("✓ 行业API测试通过")
        else:
            print("❌ 行业API测试失败")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API功能测试失败: {e}")
        return False

def test_dashboard_functionality():
    """测试管理台功能"""
    print("\n=== 测试管理台功能 ===")
    
    try:
        # 启动管理台（在后台）
        import subprocess
        import threading
        
        def start_dashboard():
            subprocess.run([sys.executable, "run_dashboard.py"], 
                         capture_output=True, text=True)
        
        # 启动管理台
        dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)
        dashboard_thread.start()
        
        # 等待管理台启动
        time.sleep(3)
        
        # 测试管理台API
        base_url = "http://localhost:5001"
        
        # 测试仪表板统计
        response = requests.get(f"{base_url}/api/dashboard/stats", timeout=5)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ 管理台统计API测试通过")
            else:
                print("❌ 管理台统计API返回失败")
                return False
        else:
            print("❌ 管理台统计API测试失败")
            return False
        
        # 测试行业列表API
        response = requests.get(f"{base_url}/api/industries", timeout=5)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ 管理台行业API测试通过")
            else:
                print("❌ 管理台行业API返回失败")
                return False
        else:
            print("❌ 管理台行业API测试失败")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 管理台功能测试失败: {e}")
        return False

def test_data_operations():
    """测试数据操作"""
    print("\n=== 测试数据操作 ===")
    
    try:
        from core.industry_classifier import IndustryClassifier
        
        classifier = IndustryClassifier()
        
        # 测试数据更新
        result = classifier.run_full_update()
        if result.get('success'):
            print("✓ 数据更新操作成功")
        else:
            print(f"⚠ 数据更新操作失败: {result.get('message')}")
        
        # 测试数据查询
        industries = classifier.get_all_industries()
        print(f"✓ 数据查询成功: {len(industries)}条记录")
        
        # 测试搜索功能
        if industries:
            search_results = classifier.search_industries("电子")
            print(f"✓ 搜索功能测试成功: {len(search_results)}条结果")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据操作测试失败: {e}")
        return False

def test_database_operations():
    """测试数据库操作"""
    print("\n=== 测试数据库操作 ===")
    
    try:
        from utils.database import db_manager
        
        # 测试数据库连接
        result = db_manager.execute_query("SELECT 1 as test")
        if result and result[0]['test'] == 1:
            print("✓ 数据库连接测试通过")
        else:
            print("❌ 数据库连接测试失败")
            return False
        
        # 测试表存在性
        tables = ['wind_industry_classification', 'stock_industry_mapping']
        for table in tables:
            if db_manager.table_exists(table):
                print(f"✓ 表 {table} 存在")
            else:
                print(f"❌ 表 {table} 不存在")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库操作测试失败: {e}")
        return False

def generate_test_report(results):
    """生成测试报告"""
    print("\n" + "="*50)
    print("测试报告")
    print("="*50)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests
    
    print(f"总测试数: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"失败测试: {failed_tests}")
    print(f"通过率: {passed_tests/total_tests*100:.1f}%")
    
    print("\n详细结果:")
    for test_name, result in results.items():
        status = "✓ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    if failed_tests == 0:
        print("\n🎉 所有测试通过！模块功能正常。")
    else:
        print(f"\n⚠️ 有 {failed_tests} 个测试失败，请检查相关功能。")
    
    # 保存测试报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'failed_tests': failed_tests,
        'pass_rate': passed_tests/total_tests*100,
        'results': results
    }
    
    with open('test_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n测试报告已保存到: test_report.json")

def main():
    """主测试函数"""
    print("万得行业分类模块完整功能测试")
    print("="*50)
    
    results = {}
    
    # 执行各项测试
    results['核心功能'] = test_core_functionality()
    results['数据库操作'] = test_database_operations()
    results['数据操作'] = test_data_operations()
    results['API功能'] = test_api_functionality()
    results['管理台功能'] = test_dashboard_functionality()
    
    # 生成测试报告
    generate_test_report(results)
    
    # 返回测试结果
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 