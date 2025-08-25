"""
万得行业分类模块基本测试
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_industry_model():
    """测试行业模型"""
    print("测试行业模型...")
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
        
        print(f"✅ 行业模型创建成功: {industry}")
        print(f"完整路径: {industry.get_full_path()}")
        
        return True
        
    except Exception as e:
        print(f"❌ 行业模型测试失败: {e}")
        return False

def test_stock_industry_model():
    """测试股票行业映射模型"""
    print("\n测试股票行业映射模型...")
    try:
        from models.stock_industry_model import StockIndustryModel, MappingStatus
        from datetime import datetime
        
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
        print(f"高置信度: {mapping.is_high_confidence()}")
        
        return True
        
    except Exception as e:
        print(f"❌ 股票行业映射模型测试失败: {e}")
        return False

def test_logger():
    """测试日志器"""
    print("\n测试日志器...")
    try:
        from utils.logger import logger
        
        logger.info("测试信息日志")
        logger.warning("测试警告日志")
        logger.error("测试错误日志")
        
        print("✅ 日志器测试成功")
        return True
        
    except Exception as e:
        print(f"❌ 日志器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始万得行业分类模块基本测试...")
    print("=" * 50)
    
    test_results = []
    
    # 运行测试
    test_results.append(test_industry_model())
    test_results.append(test_stock_industry_model())
    test_results.append(test_logger())
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    passed = sum(test_results)
    total = len(test_results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查错误信息")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 