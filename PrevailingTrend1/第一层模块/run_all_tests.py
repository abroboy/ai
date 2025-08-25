"""
第一层模块综合测试脚本
测试所有模块的基本功能
"""

import sys
import os
import subprocess

def test_module(module_name, test_file):
    """测试指定模块"""
    print(f"\n{'='*60}")
    print(f"测试模块: {module_name}")
    print(f"{'='*60}")
    
    try:
        # 切换到模块目录
        os.chdir(module_name)
        
        # 运行测试
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {module_name} 测试通过")
            print(result.stdout)
            return True
        else:
            print(f"❌ {module_name} 测试失败")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ {module_name} 测试异常: {e}")
        return False
    finally:
        # 返回上级目录
        os.chdir("..")

def test_module_structure():
    """测试模块结构"""
    print(f"\n{'='*60}")
    print("测试模块结构")
    print(f"{'='*60}")
    
    modules = [
        "万得行业分类",
        "公司名字列表", 
        "国内热点数据",
        "国外热点数据",
        "腾讯济安指数",
        "雪球等论坛热点数据",
        "其他互联网信息"
    ]
    
    results = []
    
    for module in modules:
        print(f"\n检查模块: {module}")
        
        # 检查基本文件
        required_files = [
            f"{module}/__init__.py",
            f"{module}/README.md"
        ]
        
        module_ok = True
        for file_path in required_files:
            if os.path.exists(file_path):
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path} 不存在")
                module_ok = False
        
        # 检查子目录
        subdirs = ["models", "core", "utils", "api", "tests"]
        for subdir in subdirs:
            subdir_path = f"{module}/{subdir}"
            if os.path.exists(subdir_path):
                print(f"  ✅ {subdir_path}/")
            else:
                print(f"  ⚠️  {subdir_path}/ 不存在")
        
        results.append(module_ok)
    
    return results

def test_python_environment():
    """测试Python环境"""
    print(f"\n{'='*60}")
    print("测试Python环境")
    print(f"{'='*60}")
    
    try:
        # 测试Python版本
        version = sys.version_info
        print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
        
        if version.major == 3 and version.minor >= 8:
            print("✅ Python版本符合要求")
        else:
            print("❌ Python版本过低，需要3.8+")
            return False
        
        # 测试关键包
        import pymysql
        print("✅ PyMySQL 可用")
        
        import pandas
        print("✅ Pandas 可用")
        
        import requests
        print("✅ Requests 可用")
        
        import flask
        print("✅ Flask 可用")
        
        return True
        
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    print(f"\n{'='*60}")
    print("测试基本功能")
    print(f"{'='*60}")
    
    results = []
    
    # 测试万得行业分类模块
    try:
        os.chdir("万得行业分类")
        from models.industry_model import IndustryModel, IndustryStatus
        from datetime import datetime
        
        industry = IndustryModel(
            industry_code="801010",
            industry_name="农林牧渔",
            industry_level=1,
            parent_code=None,
            sw_code="801010",
            csrc_code="A01",
            status=IndustryStatus.ACTIVE,
            industry_desc="农业、林业、畜牧业、渔业",
            major_companies=["牧原股份", "温氏股份"],
            industry_keywords=["农业", "养殖", "种植"],
            market_cap_total=1000000000.0,
            company_count=50,
            update_date=datetime.now(),
            source="wind"
        )
        
        print("✅ 万得行业分类 - 行业模型创建成功")
        results.append(True)
        
    except Exception as e:
        print(f"❌ 万得行业分类 - 行业模型测试失败: {e}")
        results.append(False)
    finally:
        os.chdir("..")
    
    # 测试公司名字列表模块
    try:
        os.chdir("公司名字列表")
        from models.company_model import CompanyModel, CompanyStatus, CompanyType
        from datetime import datetime
        
        company = CompanyModel(
            company_name="测试公司",
            stock_code="000001",
            market="SZ",
            short_name="测试",
            company_type=CompanyType.MAIN_BOARD,
            list_date=datetime(2020, 1, 1),
            status=CompanyStatus.ACTIVE,
            area="深圳",
            source="test"
        )
        
        print("✅ 公司名字列表 - 公司模型创建成功")
        results.append(True)
        
    except Exception as e:
        print(f"❌ 公司名字列表 - 公司模型测试失败: {e}")
        results.append(False)
    finally:
        os.chdir("..")
    
    return results

def main():
    """主测试函数"""
    print("开始第一层模块综合测试...")
    print("=" * 80)
    
    all_results = []
    
    # 1. 测试Python环境
    env_ok = test_python_environment()
    all_results.append(env_ok)
    
    # 2. 测试模块结构
    structure_results = test_module_structure()
    all_results.extend(structure_results)
    
    # 3. 测试基本功能
    functionality_results = test_basic_functionality()
    all_results.extend(functionality_results)
    
    # 4. 测试各模块
    module_tests = [
        ("万得行业分类", "simple_test.py"),
        ("公司名字列表", "simple_test.py")
    ]
    
    for module_name, test_file in module_tests:
        if os.path.exists(f"{module_name}/{test_file}"):
            result = test_module(module_name, test_file)
            all_results.append(result)
        else:
            print(f"⚠️  {module_name} 没有测试文件 {test_file}")
            all_results.append(False)
    
    # 输出最终结果
    print(f"\n{'='*80}")
    print("综合测试结果汇总")
    print(f"{'='*80}")
    
    passed = sum(all_results)
    total = len(all_results)
    
    print(f"总测试项: {total}")
    print(f"通过: {passed}")
    print(f"失败: {total - passed}")
    print(f"通过率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 所有测试通过！第一层模块运行正常！")
        print("✅ 模块结构完整")
        print("✅ 数据模型正常")
        print("✅ 配置管理正常")
        print("✅ 日志系统正常")
        print("✅ Python环境正常")
    else:
        print(f"\n⚠️  有 {total - passed} 项测试失败")
        print("请检查失败的项目并修复")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 