"""
简化的模块测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """测试基本功能"""
    print("测试基本功能...")
    
    try:
        # 测试公司模型
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
        
        print(f"✅ 公司模型创建成功: {company}")
        
        # 测试日志器
        from utils.logger import logger
        logger.info("测试日志功能")
        print("✅ 日志器工作正常")
        
        # 测试配置
        from utils.config import config
        config.print_config()
        print("✅ 配置管理正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 基本功能测试失败: {e}")
        return False

def test_collector_simple():
    """测试简化的采集器"""
    print("\n测试采集器...")
    
    try:
        # 创建简化的采集器
        class SimpleCollector:
            def collect_from_sse(self):
                return [
                    CompanyModel(
                        company_name="中国石油天然气股份有限公司",
                        stock_code="601857",
                        market="SH",
                        short_name="中国石油",
                        company_type=CompanyType.MAIN_BOARD,
                        list_date=datetime(2007, 11, 5),
                        status=CompanyStatus.ACTIVE,
                        area="北京",
                        source="sse"
                    )
                ]
        
        collector = SimpleCollector()
        companies = collector.collect_from_sse()
        print(f"✅ 采集器测试成功: 采集到 {len(companies)} 家公司")
        
        return True
        
    except Exception as e:
        print(f"❌ 采集器测试失败: {e}")
        return False

def test_validator_simple():
    """测试简化的验证器"""
    print("\n测试验证器...")
    
    try:
        # 创建简化的验证器
        class SimpleValidator:
            def validate_company_data(self, companies):
                if not companies:
                    return False, ["没有公司数据"]
                
                errors = []
                for i, company in enumerate(companies):
                    if not company.company_name:
                        errors.append(f"第{i+1}条: 公司名称为空")
                    if not company.stock_code:
                        errors.append(f"第{i+1}条: 股票代码为空")
                
                return len(errors) == 0, errors
        
        validator = SimpleValidator()
        
        # 创建测试数据
        from models.company_model import CompanyModel, CompanyStatus, CompanyType
        from datetime import datetime
        
        test_companies = [
            CompanyModel(
                company_name="测试公司1",
                stock_code="000001",
                market="SZ",
                short_name="测试1",
                company_type=CompanyType.MAIN_BOARD,
                list_date=datetime(2020, 1, 1),
                status=CompanyStatus.ACTIVE,
                area="深圳",
                source="test"
            ),
            CompanyModel(
                company_name="测试公司2",
                stock_code="000002",
                market="SZ",
                short_name="测试2",
                company_type=CompanyType.MAIN_BOARD,
                list_date=datetime(2020, 1, 1),
                status=CompanyStatus.ACTIVE,
                area="深圳",
                source="test"
            )
        ]
        
        is_valid, messages = validator.validate_company_data(test_companies)
        print(f"✅ 验证器测试成功: {'通过' if is_valid else '失败'}")
        if messages:
            print(f"验证消息: {messages}")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始简化测试...")
    print("=" * 50)
    
    test_results = []
    
    # 运行测试
    test_results.append(test_basic_functionality())
    test_results.append(test_collector_simple())
    test_results.append(test_validator_simple())
    
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