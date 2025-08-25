"""
第一层模块综合测试脚本
测试所有模块的基本功能
"""

import sys
import os
import importlib.util

def test_module_import(module_name, test_name):
    """测试模块导入"""
    print(f"测试 {test_name} 模块导入...")
    try:
        # 尝试导入模块
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            print(f"❌ {test_name} 模块不存在")
            return False
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✅ {test_name} 模块导入成功")
        return True
        
    except Exception as e:
        print(f"❌ {test_name} 模块导入失败: {e}")
        return False

def test_company_list_module():
    """测试公司名字列表模块"""
    print("\n" + "="*50)
    print("测试公司名字列表模块")
    print("="*50)
    
    results = []
    
    # 测试基本导入
    results.append(test_module_import("models.company_model", "公司模型"))
    results.append(test_module_import("utils.logger", "日志器"))
    results.append(test_module_import("utils.config", "配置管理"))
    
    # 测试公司模型功能
    try:
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
        
        print(f"✅ 公司模型功能正常: {company}")
        results.append(True)
        
    except Exception as e:
        print(f"❌ 公司模型功能异常: {e}")
        results.append(False)
    
    return sum(results) / len(results) >= 0.8

def test_industry_classification_module():
    """测试万得行业分类模块"""
    print("\n" + "="*50)
    print("测试万得行业分类模块")
    print("="*50)
    
    results = []
    
    # 测试基本导入
    results.append(test_module_import("models.industry_model", "行业模型"))
    results.append(test_module_import("models.stock_industry_model", "股票行业映射模型"))
    results.append(test_module_import("utils.logger", "日志器"))
    
    # 测试行业模型功能
    try:
        from models.industry_model import IndustryModel, IndustryLevel, IndustryStatus
        from datetime import datetime
        
        industry = IndustryModel(
            industry_code="801010",
            industry_name="农林牧渔",
            industry_level=IndustryLevel.LEVEL_1,
            parent_code=None,
            sw_code="801010",
            csrc_code="A01",
            status=IndustryStatus.ACTIVE,
            industry_desc="农业、林业、畜牧业、渔业",
            major_companies="牧原股份,温氏股份",
            industry_keywords="农业,养殖,种植",
            market_cap_total=1000000000.0,
            company_count=50,
            update_date=datetime.now(),
            source="wind"
        )
        
        print(f"✅ 行业模型功能正常: {industry}")
        results.append(True)
        
    except Exception as e:
        print(f"❌ 行业模型功能异常: {e}")
        results.append(False)
    
    return sum(results) / len(results) >= 0.8

def test_hotspot_modules():
    """测试热点数据模块"""
    print("\n" + "="*50)
    print("测试热点数据模块")
    print("="*50)
    
    results = []
    
    # 测试国内热点数据模块
    print("测试国内热点数据模块...")
    try:
        # 检查模块文件是否存在
        hotspot_files = [
            "国内热点数据/__init__.py",
            "国内热点数据/models/__init__.py",
            "国外热点数据/__init__.py",
            "雪球等论坛热点数据/__init__.py",
            "其他互联网信息/__init__.py"
        ]
        
        for file_path in hotspot_files:
            if os.path.exists(file_path):
                print(f"✅ {file_path} 存在")
                results.append(True)
            else:
                print(f"❌ {file_path} 不存在")
                results.append(False)
        
    except Exception as e:
        print(f"❌ 热点数据模块测试异常: {e}")
        results.append(False)
    
    return sum(results) / len(results) >= 0.8

def test_index_module():
    """测试腾讯济安指数模块"""
    print("\n" + "="*50)
    print("测试腾讯济安指数模块")
    print("="*50)
    
    results = []
    
    # 检查模块文件是否存在
    index_files = [
        "腾讯济安指数/__init__.py",
        "腾讯济安指数/models/__init__.py"
    ]
    
    for file_path in index_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
            results.append(True)
        else:
            print(f"❌ {file_path} 不存在")
            results.append(False)
    
    return sum(results) / len(results) >= 0.8

def test_project_structure():
    """测试项目结构"""
    print("\n" + "="*50)
    print("测试项目结构")
    print("="*50)
    
    results = []
    
    # 检查必要的目录和文件
    required_structure = [
        "万得行业分类/",
        "公司名字列表/",
        "国内热点数据/",
        "国外热点数据/",
        "腾讯济安指数/",
        "雪球等论坛热点数据/",
        "其他互联网信息/",
        "README.md"
    ]
    
    for item in required_structure:
        if os.path.exists(item):
            print(f"✅ {item} 存在")
            results.append(True)
        else:
            print(f"❌ {item} 不存在")
            results.append(False)
    
    return sum(results) / len(results) >= 0.8

def main():
    """主测试函数"""
    print("开始第一层模块综合测试...")
    print("=" * 60)
    
    # 切换到第一层模块目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    test_results = []
    
    # 运行所有测试
    test_results.append(test_project_structure())
    test_results.append(test_company_list_module())
    test_results.append(test_industry_classification_module())
    test_results.append(test_hotspot_modules())
    test_results.append(test_index_module())
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("综合测试结果汇总:")
    passed = sum(test_results)
    total = len(test_results)
    print(f"通过: {passed}/{total}")
    
    test_names = [
        "项目结构",
        "公司名字列表模块",
        "万得行业分类模块", 
        "热点数据模块",
        "腾讯济安指数模块"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    if passed == total:
        print("\n🎉 所有模块测试通过！")
        print("第一层模块工程化实现完成！")
    else:
        print(f"\n⚠️  {total - passed} 个模块测试失败，请检查错误信息")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 