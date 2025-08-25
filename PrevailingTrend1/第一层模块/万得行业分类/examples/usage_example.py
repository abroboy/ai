"""
万得行业分类模块使用示例
展示如何使用行业分类模块的各种功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from 万得行业分类 import IndustryClassifier, logger


def example_basic_usage():
    """基础使用示例"""
    print("=== 基础使用示例 ===")
    
    # 创建行业分类器实例
    classifier = IndustryClassifier()
    
    # 初始化数据库
    print("1. 初始化数据库...")
    classifier.initialize_database()
    
    # 运行完整更新
    print("2. 运行数据更新...")
    result = classifier.run_full_update()
    print(f"更新结果: {result['success']}")
    
    # 查询行业数据
    print("3. 查询行业数据...")
    industries = classifier.get_industries_by_level(1)
    print(f"一级行业数量: {len(industries)}")
    for industry in industries[:5]:  # 显示前5个
        print(f"  {industry}")
    
    # 搜索行业
    print("4. 搜索行业...")
    search_results = classifier.search_industries("电子")
    print(f"搜索结果数量: {len(search_results)}")
    for result in search_results[:3]:  # 显示前3个
        print(f"  {result}")
    
    # 获取统计信息
    print("5. 获取统计信息...")
    stats = classifier.get_industry_statistics()
    print(f"统计信息: {stats}")


def example_advanced_queries():
    """高级查询示例"""
    print("\n=== 高级查询示例 ===")
    
    classifier = IndustryClassifier()
    
    # 查询特定行业
    print("1. 查询特定行业...")
    industry = classifier.get_industry_by_code("010000")
    if industry:
        print(f"行业信息: {industry}")
        
        # 获取行业层级结构
        print("2. 获取行业层级结构...")
        hierarchy = classifier.get_industry_hierarchy("010000")
        print(f"层级结构: {hierarchy}")
        
        # 获取行业下的股票
        print("3. 获取行业下的股票...")
        stocks = classifier.get_stocks_by_industry("010000")
        print(f"股票数量: {len(stocks)}")
        for stock in stocks[:3]:  # 显示前3个
            print(f"  {stock}")
    else:
        print("未找到行业代码: 010000")


def example_data_validation():
    """数据验证示例"""
    print("\n=== 数据验证示例 ===")
    
    from 万得行业分类.core.data_collector import DataCollector
    from 万得行业分类.core.data_validator import DataValidator
    
    # 创建数据采集器和验证器
    collector = DataCollector()
    validator = DataValidator()
    
    # 采集数据
    print("1. 采集数据...")
    industry_data = collector.get_primary_industry_data()
    stock_mapping_data = collector.get_primary_stock_mapping_data()
    
    print(f"采集到行业数据: {len(industry_data)}条")
    print(f"采集到股票映射数据: {len(stock_mapping_data)}条")
    
    # 验证数据
    print("2. 验证行业数据...")
    industry_valid, industry_issues = validator.validate_industry_data(industry_data)
    print(f"行业数据验证结果: {'通过' if industry_valid else '失败'}")
    if industry_issues:
        print("问题列表:")
        for issue in industry_issues[:3]:  # 显示前3个问题
            print(f"  - {issue}")
    
    print("3. 验证股票映射数据...")
    mapping_valid, mapping_issues = validator.validate_stock_mapping_data(stock_mapping_data)
    print(f"股票映射数据验证结果: {'通过' if mapping_valid else '失败'}")
    if mapping_issues:
        print("问题列表:")
        for issue in mapping_issues[:3]:  # 显示前3个问题
            print(f"  - {issue}")
    
    print("4. 验证数据一致性...")
    consistency_valid, consistency_issues = validator.validate_data_consistency(
        industry_data, stock_mapping_data
    )
    print(f"数据一致性验证结果: {'通过' if consistency_valid else '失败'}")
    if consistency_issues:
        print("问题列表:")
        for issue in consistency_issues[:3]:  # 显示前3个问题
            print(f"  - {issue}")


def example_custom_queries():
    """自定义查询示例"""
    print("\n=== 自定义查询示例 ===")
    
    from 万得行业分类.utils.database import db_manager
    
    # 直接使用数据库管理器进行查询
    print("1. 自定义SQL查询...")
    
    # 查询所有活跃的行业
    sql = """
    SELECT industry_code, industry_name, industry_level, company_count 
    FROM wind_industry_classification 
    WHERE status = 'active' 
    ORDER BY industry_level, industry_name
    """
    results = db_manager.execute_query(sql)
    print(f"活跃行业数量: {len(results)}")
    
    # 查询高置信度的股票映射
    sql = """
    SELECT stock_code, stock_name, industry_name, confidence 
    FROM stock_industry_mapping 
    WHERE confidence >= 0.9 AND status = 'active'
    ORDER BY confidence DESC
    LIMIT 10
    """
    results = db_manager.execute_query(sql)
    print(f"高置信度股票映射数量: {len(results)}")
    for result in results[:3]:
        print(f"  {result['stock_code']} -> {result['industry_name']} (置信度: {result['confidence']})")
    
    # 使用DataFrame进行数据分析
    print("2. 数据分析...")
    sql = """
    SELECT industry_level, COUNT(*) as count, AVG(company_count) as avg_companies
    FROM wind_industry_classification 
    WHERE status = 'active'
    GROUP BY industry_level
    ORDER BY industry_level
    """
    df = db_manager.query_to_dataframe(sql)
    print("行业层级统计:")
    print(df)


def example_error_handling():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")
    
    classifier = IndustryClassifier()
    
    try:
        # 尝试查询不存在的行业
        print("1. 查询不存在的行业...")
        industry = classifier.get_industry_by_code("999999")
        if industry:
            print(f"找到行业: {industry}")
        else:
            print("行业不存在")
        
        # 尝试查询无效的层级
        print("2. 查询无效层级...")
        industries = classifier.get_industries_by_level(99)
        print(f"查询结果数量: {len(industries)}")
        
        # 尝试搜索空关键词
        print("3. 搜索空关键词...")
        results = classifier.search_industries("")
        print(f"搜索结果数量: {len(results)}")
        
    except Exception as e:
        logger.error(f"查询过程中发生错误: {e}")
        print(f"错误信息: {e}")


def main():
    """主函数"""
    print("万得行业分类模块使用示例")
    print("=" * 50)
    
    try:
        # 运行各种示例
        example_basic_usage()
        example_advanced_queries()
        example_data_validation()
        example_custom_queries()
        example_error_handling()
        
        print("\n所有示例执行完成！")
        
    except Exception as e:
        logger.error(f"示例执行失败: {e}")
        print(f"执行失败: {e}")


if __name__ == "__main__":
    main() 