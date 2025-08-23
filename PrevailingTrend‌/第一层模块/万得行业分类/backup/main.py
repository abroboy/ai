"""
万得行业分类模块主程序
提供完整的行业分类功能运行入口
"""

import sys
import argparse
from datetime import datetime
import json

from .core.industry_classifier import IndustryClassifier
from .utils.logger import logger
from .utils.database import db_manager


def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(description='万得行业分类模块')
    parser.add_argument('--action', choices=['init', 'update', 'query', 'stats'], 
                       default='update', help='执行的操作')
    parser.add_argument('--industry-code', help='行业代码')
    parser.add_argument('--level', type=int, choices=[1, 2, 3], help='行业层级')
    parser.add_argument('--keyword', help='搜索关键词')
    
    args = parser.parse_args()
    
    try:
        classifier = IndustryClassifier()
        
        if args.action == 'init':
            # 初始化数据库
            logger.info("开始初始化数据库...")
            classifier.initialize_database()
            logger.info("数据库初始化完成")
            
        elif args.action == 'update':
            # 更新数据
            logger.info("开始更新行业分类数据...")
            result = classifier.run_full_update()
            
            if result['success']:
                logger.info("数据更新成功")
                print(f"更新结果: {result}")
            else:
                logger.error(f"数据更新失败: {result['message']}")
                sys.exit(1)
                
        elif args.action == 'query':
            # 查询数据
            if args.industry_code:
                # 查询特定行业
                industry = classifier.get_industry_by_code(args.industry_code)
                if industry:
                    print(f"行业信息: {industry}")
                else:
                    print(f"未找到行业代码: {args.industry_code}")
                    
            elif args.level:
                # 查询指定层级的行业
                industries = classifier.get_industries_by_level(args.level)
                print(f"第{args.level}级行业列表:")
                for industry in industries:
                    print(f"  {industry}")
                    
            elif args.keyword:
                # 搜索行业
                industries = classifier.search_industries(args.keyword)
                print(f"搜索结果 (关键词: {args.keyword}):")
                for industry in industries:
                    print(f"  {industry}")
            else:
                print("请指定查询参数: --industry-code, --level, 或 --keyword")
                
        elif args.action == 'stats':
            # 获取统计信息
            stats = classifier.get_industry_statistics()
            print("行业分类统计信息:")
            print(json.dumps(stats, indent=2, ensure_ascii=False))
            
    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 