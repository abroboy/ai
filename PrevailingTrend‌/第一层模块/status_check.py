"""
第一层模块状态检查脚本
"""

import os
import sys

def check_modules():
    """检查所有模块状态"""
    print("第一层模块状态检查")
    print("=" * 50)
    
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
        
        # 检查__init__.py
        init_file = f"{module}/__init__.py"
        if os.path.exists(init_file):
            print(f"  ✅ {init_file}")
            results.append(True)
        else:
            print(f"  ❌ {init_file} 不存在")
            results.append(False)
        
        # 检查README.md
        readme_file = f"{module}/README.md"
        if os.path.exists(readme_file):
            print(f"  ✅ {readme_file}")
        else:
            print(f"  ⚠️  {readme_file} 不存在")
        
        # 检查子目录
        subdirs = ["models", "core", "utils", "api", "tests"]
        for subdir in subdirs:
            subdir_path = f"{module}/{subdir}"
            if os.path.exists(subdir_path):
                print(f"  ✅ {subdir_path}/")
            else:
                print(f"  ⚠️  {subdir_path}/ 不存在")
    
    return results

def test_core_functionality():
    """测试核心功能"""
    print(f"\n{'='*50}")
    print("测试核心功能")
    print("=" * 50)
    
    results = []
    
    # 测试万得行业分类
    print("\n测试万得行业分类模块...")
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
        
        print("  ✅ 行业模型创建成功")
        results.append(True)
        
    except Exception as e:
        print(f"  ❌ 行业模型测试失败: {e}")
        results.append(False)
    finally:
        os.chdir("..")
    
    # 测试公司名字列表
    print("\n测试公司名字列表模块...")
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
        
        print("  ✅ 公司模型创建成功")
        results.append(True)
        
    except Exception as e:
        print(f"  ❌ 公司模型测试失败: {e}")
        results.append(False)
    finally:
        os.chdir("..")
    
    return results

def test_python_environment():
    """测试Python环境"""
    print(f"\n{'='*50}")
    print("测试Python环境")
    print("=" * 50)
    
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

def main():
    """主函数"""
    print("开始第一层模块状态检查...")
    
    all_results = []
    
    # 1. 检查模块结构
    structure_results = check_modules()
    all_results.extend(structure_results)
    
    # 2. 测试Python环境
    env_ok = test_python_environment()
    all_results.append(env_ok)
    
    # 3. 测试核心功能
    functionality_results = test_core_functionality()
    all_results.extend(functionality_results)
    
    # 输出结果
    print(f"\n{'='*50}")
    print("检查结果汇总")
    print("=" * 50)
    
    passed = sum(all_results)
    total = len(all_results)
    
    print(f"总检查项: {total}")
    print(f"通过: {passed}")
    print(f"失败: {total - passed}")
    print(f"通过率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 所有检查通过！第一层模块运行正常！")
    else:
        print(f"\n⚠️  有 {total - passed} 项检查失败")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 