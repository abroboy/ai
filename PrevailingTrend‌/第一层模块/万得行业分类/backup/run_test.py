"""
万得行业分类模块测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_models():
    """测试数据模型"""
    print("测试数据模型...")
    try:
        from models.industry_model import IndustryModel, IndustryStatus
        from models.stock_industry_model import StockIndustryModel, MappingStatus
        from datetime import datetime
        
        # 测试行业模型
        industry = IndustryModel(
            industry_code="801010",
            industry_name="农林牧渔",
            industry_level=1,  # 使用整数而不是枚举
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
        
        print(f"✅ 行业模型创建成功: {industry}")
        
        # 测试股票行业映射模型
        mapping = StockIndustryModel(
            stock_code="000001",
            stock_name="平安银行",
            industry_code="801010",
            industry_name="农林牧渔",
            industry_level=1,
            mapping_date=datetime.now(),
            status=MappingStatus.ACTIVE,
            confidence=0.95,
            source="wind"
        )
        
        print(f"✅ 股票行业映射模型创建成功: {mapping}")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据模型测试失败: {e}")
        return False

def test_utils():
    """测试工具类"""
    print("\n测试工具类...")
    try:
        # 测试配置
        from utils.config import config
        config.print_config()
        print("✅ 配置管理正常")
        
        # 测试日志器
        from utils.logger import logger
        logger.info("测试日志功能")
        print("✅ 日志器工作正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 工具类测试失败: {e}")
        return False

def test_core():
    """测试核心功能"""
    print("\n测试核心功能...")
    try:
        # 测试简单验证器
        from core.simple_validator import SimpleValidator
        
        validator = SimpleValidator()
        print("✅ 验证器创建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 核心功能测试失败: {e}")
        return False

def test_api():
    """测试API功能"""
    print("\n测试API功能...")
    try:
        # 测试API导入
        from api.industry_api import IndustryAPI
        from api.stock_api import StockAPI
        
        print("✅ API模块导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ API功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始万得行业分类模块测试...")
    print("=" * 50)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(test_models())
    test_results.append(test_utils())
    test_results.append(test_core())
    test_results.append(test_api())
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    passed = sum(test_results)
    total = len(test_results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 万得行业分类模块测试全部通过！")
    else:
        print("⚠️  部分测试失败，请检查错误信息")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 