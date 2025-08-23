"""
公司名字列表模块主程序
提供命令行接口和主要功能入口
"""

import sys
import argparse
from datetime import datetime
import json

from .core.company_collector import CompanyCollector
from .core.company_validator import CompanyValidator
from .core.company_manager import CompanyManager
from .utils.logger import logger
from .utils.database import db_manager


def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(description='公司名字列表模块')
    parser.add_argument('--action', choices=['init', 'collect', 'validate', 'query', 'stats'],
                        default='collect', help='执行的操作')
    parser.add_argument('--market', choices=['SH', 'SZ', 'HK', 'US'], help='市场类型')
    parser.add_argument('--company-type', choices=['main_board', 'sme_board', 'gem', 'star', 'new_third'], 
                        help='公司类型')
    parser.add_argument('--stock-code', help='股票代码')
    parser.add_argument('--keyword', help='搜索关键词')
    parser.add_argument('--area', help='地区')

    args = parser.parse_args()

    try:
        if args.action == 'init':
            # 初始化数据库
            logger.info("开始初始化数据库...")
            init_database()
            logger.info("数据库初始化完成")

        elif args.action == 'collect':
            # 采集数据
            logger.info("开始采集公司数据...")
            collect_companies(args.market, args.company_type)
            logger.info("数据采集完成")

        elif args.action == 'validate':
            # 验证数据
            logger.info("开始验证公司数据...")
            validate_companies()
            logger.info("数据验证完成")

        elif args.action == 'query':
            # 查询数据
            query_companies(args)

        elif args.action == 'stats':
            # 获取统计信息
            get_statistics()

    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        sys.exit(1)


def init_database():
    """初始化数据库"""
    try:
        # 创建数据库连接
        if not db_manager.connect():
            logger.error("数据库连接失败")
            return False
        
        # 创建公司信息表
        from .models.company_model import COMPANY_TABLE_SQL
        success = db_manager.create_table('company_list', COMPANY_TABLE_SQL)
        
        if success:
            logger.info("数据库表创建成功")
        else:
            logger.error("数据库表创建失败")
        
        return success
        
    except Exception as e:
        logger.error(f"初始化数据库失败: {e}")
        return False


def collect_companies(market=None, company_type=None):
    """采集公司数据"""
    try:
        collector = CompanyCollector()
        manager = CompanyManager()
        
        # 根据参数采集数据
        if market:
            companies = collector.collect_by_market(market)
        elif company_type:
            from .models.company_model import CompanyType
            company_type_enum = CompanyType(company_type)
            companies = collector.collect_by_company_type(company_type_enum)
        else:
            companies = collector.collect_all()
        
        if companies:
            # 保存到数据库
            success = manager.save_companies(companies)
            if success:
                logger.info(f"成功保存 {len(companies)} 家公司数据")
            else:
                logger.error("保存公司数据失败")
        else:
            logger.warning("没有采集到公司数据")
        
        return companies
        
    except Exception as e:
        logger.error(f"采集公司数据失败: {e}")
        return []


def validate_companies():
    """验证公司数据"""
    try:
        validator = CompanyValidator()
        manager = CompanyManager()
        
        # 获取所有公司数据
        companies = manager.get_companies_by_market('SH') + manager.get_companies_by_market('SZ')
        
        if companies:
            # 验证数据
            is_valid, messages = validator.validate_company_data(companies)
            
            # 验证一致性
            is_consistent, consistency_messages = validator.validate_company_consistency(companies)
            
            # 验证完整性
            is_complete, completeness_messages = validator.validate_data_completeness(companies)
            
            # 输出验证结果
            print("数据验证结果:")
            print(f"  数据有效性: {'通过' if is_valid else '失败'}")
            print(f"  数据一致性: {'通过' if is_consistent else '失败'}")
            print(f"  数据完整性: {'通过' if is_complete else '失败'}")
            
            if messages:
                print("  验证消息:")
                for msg in messages:
                    print(f"    - {msg}")
            
            if consistency_messages:
                print("  一致性消息:")
                for msg in consistency_messages:
                    print(f"    - {msg}")
            
            if completeness_messages:
                print("  完整性消息:")
                for msg in completeness_messages:
                    print(f"    - {msg}")
        else:
            logger.warning("没有公司数据可供验证")
        
    except Exception as e:
        logger.error(f"验证公司数据失败: {e}")


def query_companies(args):
    """查询公司数据"""
    try:
        manager = CompanyManager()
        
        if args.stock_code and args.market:
            # 查询特定公司
            company = manager.get_company_by_code(args.stock_code, args.market)
            if company:
                print(f"公司信息: {company}")
            else:
                print(f"未找到公司: {args.stock_code}.{args.market}")
        
        elif args.market:
            # 查询指定市场的公司
            companies = manager.get_companies_by_market(args.market)
            print(f"{args.market}市场公司列表:")
            for company in companies[:10]:  # 只显示前10家
                print(f"  {company}")
            if len(companies) > 10:
                print(f"  ... 还有 {len(companies) - 10} 家公司")
        
        elif args.company_type:
            # 查询指定类型的公司
            from .models.company_model import CompanyType
            company_type_enum = CompanyType(args.company_type)
            companies = manager.get_companies_by_type(company_type_enum)
            print(f"{args.company_type}类型公司列表:")
            for company in companies[:10]:  # 只显示前10家
                print(f"  {company}")
            if len(companies) > 10:
                print(f"  ... 还有 {len(companies) - 10} 家公司")
        
        elif args.keyword:
            # 搜索公司
            companies = manager.search_companies(args.keyword)
            print(f"搜索结果 (关键词: {args.keyword}):")
            for company in companies[:10]:  # 只显示前10家
                print(f"  {company}")
            if len(companies) > 10:
                print(f"  ... 还有 {len(companies) - 10} 家公司")
        
        elif args.area:
            # 查询指定地区的公司
            companies = manager.get_companies_by_area(args.area)
            print(f"{args.area}地区公司列表:")
            for company in companies[:10]:  # 只显示前10家
                print(f"  {company}")
            if len(companies) > 10:
                print(f"  ... 还有 {len(companies) - 10} 家公司")
        
        else:
            print("请指定查询参数: --stock-code, --market, --company-type, --keyword, 或 --area")
        
    except Exception as e:
        logger.error(f"查询公司数据失败: {e}")


def get_statistics():
    """获取统计信息"""
    try:
        manager = CompanyManager()
        stats = manager.get_company_statistics()
        
        print("公司数据统计信息:")
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")


if __name__ == "__main__":
    main() 