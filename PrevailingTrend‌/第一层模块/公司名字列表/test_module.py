"""
公司名字列表模块测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_company_model():
    """测试公司模型"""
    print("测试公司模型...")
    try:
        from models.company_model import CompanyModel, CompanyStatus, MarketType, CompanyType
        from datetime import datetime
        
        # 创建公司模型实例
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
        
        print(f"公司模型创建成功: {company}")
        print(f"完整股票代码: {company.get_full_stock_code()}")
        print(f"市场名称: {company.get_market_name()}")
        print(f"是否为活跃状态: {company.is_active()}")
        
        # 测试序列化
        company_dict = company.to_dict()
        print(f"序列化成功: {company_dict}")
        
        # 测试反序列化
        company_from_dict = CompanyModel.from_dict(company_dict)
        print(f"反序列化成功: {company_from_dict}")
        
        print("✅ 公司模型测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 公司模型测试失败: {e}")
        return False

def test_collector():
    """测试采集器"""
    print("\n测试采集器...")
    try:
        from core.company_collector import CompanyCollector
        
        collector = CompanyCollector()
        
        # 测试采集上交所数据
        sse_companies = collector.collect_from_sse()
        print(f"上交所采集结果: {len(sse_companies)} 家公司")
        
        # 测试采集深交所数据
        szse_companies = collector.collect_from_szse()
        print(f"深交所采集结果: {len(szse_companies)} 家公司")
        
        # 测试采集所有数据
        all_companies = collector.collect_all()
        print(f"所有数据采集结果: {len(all_companies)} 家公司")
        
        print("✅ 采集器测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 采集器测试失败: {e}")
        return False

def test_validator():
    """测试验证器"""
    print("\n测试验证器...")
    try:
        from core.company_validator import CompanyValidator
        from core.company_collector import CompanyCollector
        
        validator = CompanyValidator()
        collector = CompanyCollector()
        
        # 获取测试数据
        companies = collector.collect_all()
        
        if companies:
            # 测试数据验证
            is_valid, messages = validator.validate_company_data(companies)
            print(f"数据验证结果: {'通过' if is_valid else '失败'}")
            if messages:
                print(f"验证消息: {messages[:3]}...")  # 只显示前3条
            
            # 测试一致性验证
            is_consistent, consistency_messages = validator.validate_company_consistency(companies)
            print(f"一致性验证结果: {'通过' if is_consistent else '失败'}")
            
            # 测试完整性验证
            is_complete, completeness_messages = validator.validate_data_completeness(companies)
            print(f"完整性验证结果: {'通过' if is_complete else '失败'}")
        
        print("✅ 验证器测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 验证器测试失败: {e}")
        return False

def test_manager():
    """测试管理器"""
    print("\n测试管理器...")
    try:
        from core.company_manager import CompanyManager
        from core.company_collector import CompanyCollector
        
        manager = CompanyManager()
        collector = CompanyCollector()
        
        # 获取测试数据
        companies = collector.collect_all()
        
        if companies:
            # 测试统计功能
            stats = manager.get_company_statistics()
            print(f"统计信息: {stats}")
        
        print("✅ 管理器测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 管理器测试失败: {e}")
        return False

def test_logger():
    """测试日志器"""
    print("\n测试日志器...")
    try:
        from utils.logger import logger
        
        logger.info("这是一条信息日志")
        logger.warning("这是一条警告日志")
        logger.error("这是一条错误日志")
        logger.debug("这是一条调试日志")
        
        print("✅ 日志器测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 日志器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试公司名字列表模块...")
    print("=" * 50)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(test_company_model())
    test_results.append(test_collector())
    test_results.append(test_validator())
    test_results.append(test_manager())
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