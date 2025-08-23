"""
数据库设置脚本
用于初始化数据库和创建必要的表结构
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from utils.logger import logger
from config import config


def create_database():
    """创建数据库"""
    try:
        # 连接MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=config.database.host,
            port=config.database.port,
            user=config.database.username,
            password=config.database.password,
            charset=config.database.charset
        )
        
        cursor = connection.cursor()
        
        # 创建数据库
        sql = f"CREATE DATABASE IF NOT EXISTS {config.database.database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        cursor.execute(sql)
        
        logger.info(f"数据库 {config.database.database} 创建成功")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        logger.error(f"创建数据库失败: {e}")
        raise


def create_tables():
    """创建数据表"""
    try:
        from utils.database import db_manager
        from models.industry_model import INDUSTRY_TABLE_SQL
        from models.stock_industry_model import STOCK_INDUSTRY_TABLE_SQL
        
        # 连接数据库
        db_manager.connect()
        
        # 创建行业分类表
        if not db_manager.table_exists("wind_industry_classification"):
            db_manager.create_table(INDUSTRY_TABLE_SQL)
            logger.info("行业分类表创建成功")
        else:
            logger.info("行业分类表已存在")
        
        # 创建股票行业映射表
        if not db_manager.table_exists("stock_industry_mapping"):
            db_manager.create_table(STOCK_INDUSTRY_TABLE_SQL)
            logger.info("股票行业映射表创建成功")
        else:
            logger.info("股票行业映射表已存在")
        
        # 创建索引
        create_indexes()
        
        db_manager.disconnect()
        
    except Exception as e:
        logger.error(f"创建数据表失败: {e}")
        raise


def create_indexes():
    """创建索引"""
    try:
        from utils.database import db_manager
        
        # 行业分类表索引
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_industry_code ON wind_industry_classification(industry_code)",
            "CREATE INDEX IF NOT EXISTS idx_industry_level ON wind_industry_classification(industry_level)",
            "CREATE INDEX IF NOT EXISTS idx_parent_code ON wind_industry_classification(parent_code)",
            "CREATE INDEX IF NOT EXISTS idx_status ON wind_industry_classification(status)",
            "CREATE INDEX IF NOT EXISTS idx_source ON wind_industry_classification(source)",
            "CREATE INDEX IF NOT EXISTS idx_update_date ON wind_industry_classification(update_date)",
        ]
        
        # 股票行业映射表索引
        stock_indexes = [
            "CREATE INDEX IF NOT EXISTS idx_stock_code ON stock_industry_mapping(stock_code)",
            "CREATE INDEX IF NOT EXISTS idx_industry_code_mapping ON stock_industry_mapping(industry_code)",
            "CREATE INDEX IF NOT EXISTS idx_industry_level_mapping ON stock_industry_mapping(industry_level)",
            "CREATE INDEX IF NOT EXISTS idx_status_mapping ON stock_industry_mapping(status)",
            "CREATE INDEX IF NOT EXISTS idx_confidence ON stock_industry_mapping(confidence)",
            "CREATE INDEX IF NOT EXISTS idx_source_mapping ON stock_industry_mapping(source)",
            "CREATE INDEX IF NOT EXISTS idx_mapping_date ON stock_industry_mapping(mapping_date)",
        ]
        
        all_indexes = indexes + stock_indexes
        
        for index_sql in all_indexes:
            try:
                db_manager.execute_update(index_sql)
                logger.info(f"索引创建成功: {index_sql}")
            except Exception as e:
                logger.warning(f"索引创建失败: {e}")
        
    except Exception as e:
        logger.error(f"创建索引失败: {e}")
        raise


def insert_sample_data():
    """插入示例数据"""
    try:
        from utils.database import db_manager
        from models.industry_model import IndustryModel
        from models.stock_industry_model import StockIndustryModel
        
        # 连接数据库
        db_manager.connect()
        
        # 检查是否已有数据
        count = db_manager.get_table_count("wind_industry_classification")
        if count > 0:
            logger.info(f"行业分类表已有 {count} 条数据，跳过示例数据插入")
            return
        
        # 示例行业数据
        sample_industries = [
            IndustryModel("010000", "农林牧渔", 1, industry_desc="农业、林业、畜牧业、渔业相关行业"),
            IndustryModel("020000", "采掘", 1, industry_desc="采矿业相关行业"),
            IndustryModel("030000", "化工", 1, industry_desc="化学工业相关行业"),
            IndustryModel("040000", "钢铁", 1, industry_desc="钢铁工业相关行业"),
            IndustryModel("050000", "有色金属", 1, industry_desc="有色金属工业相关行业"),
            IndustryModel("060000", "电子", 1, industry_desc="电子工业相关行业"),
            IndustryModel("070000", "家用电器", 1, industry_desc="家用电器制造业相关行业"),
            IndustryModel("080000", "食品饮料", 1, industry_desc="食品饮料制造业相关行业"),
            IndustryModel("090000", "纺织服装", 1, industry_desc="纺织服装制造业相关行业"),
            IndustryModel("100000", "轻工制造", 1, industry_desc="轻工制造业相关行业"),
        ]
        
        # 插入行业数据
        industry_dicts = [industry.to_dict() for industry in sample_industries]
        db_manager.insert_many("wind_industry_classification", industry_dicts)
        logger.info(f"插入 {len(sample_industries)} 条示例行业数据")
        
        # 示例股票映射数据
        sample_mappings = [
            StockIndustryModel("000001", "平安银行", "080000", "食品饮料", 1, confidence=0.95),
            StockIndustryModel("000002", "万科A", "110000", "房地产", 1, confidence=0.90),
            StockIndustryModel("000858", "五粮液", "080000", "食品饮料", 1, confidence=0.95),
            StockIndustryModel("002415", "海康威视", "060000", "电子", 1, confidence=0.90),
            StockIndustryModel("600036", "招商银行", "120000", "银行", 1, confidence=0.95),
        ]
        
        # 插入股票映射数据
        mapping_dicts = [mapping.to_dict() for mapping in sample_mappings]
        db_manager.insert_many("stock_industry_mapping", mapping_dicts)
        logger.info(f"插入 {len(sample_mappings)} 条示例股票映射数据")
        
        db_manager.disconnect()
        
    except Exception as e:
        logger.error(f"插入示例数据失败: {e}")
        raise


def check_database_status():
    """检查数据库状态"""
    try:
        from utils.database import db_manager
        
        # 连接数据库
        db_manager.connect()
        
        # 检查表是否存在
        tables = ["wind_industry_classification", "stock_industry_mapping"]
        for table in tables:
            exists = db_manager.table_exists(table)
            count = db_manager.get_table_count(table) if exists else 0
            logger.info(f"表 {table}: {'存在' if exists else '不存在'}, 记录数: {count}")
        
        # 检查索引
        for table in tables:
            indexes = db_manager.get_table_info(table)
            logger.info(f"表 {table} 的索引:")
            for index in indexes:
                if index['Key'] != '':
                    logger.info(f"  - {index['Field']} ({index['Key']})")
        
        db_manager.disconnect()
        
    except Exception as e:
        logger.error(f"检查数据库状态失败: {e}")
        raise


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库设置脚本')
    parser.add_argument('--action', choices=['create_db', 'create_tables', 'create_indexes', 'sample_data', 'check', 'all'], 
                       default='all', help='执行的操作')
    
    args = parser.parse_args()
    
    try:
        if args.action == 'create_db':
            create_database()
        elif args.action == 'create_tables':
            create_tables()
        elif args.action == 'create_indexes':
            create_indexes()
        elif args.action == 'sample_data':
            insert_sample_data()
        elif args.action == 'check':
            check_database_status()
        elif args.action == 'all':
            logger.info("开始完整的数据库设置...")
            create_database()
            create_tables()
            insert_sample_data()
            check_database_status()
            logger.info("数据库设置完成")
        
    except Exception as e:
        logger.error(f"数据库设置失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 