"""
万得行业分类模块演示程序
展示模块的基本功能和使用方法
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.industry_model import IndustryModel, IndustryStatus
from models.stock_industry_model import StockIndustryModel, MappingStatus
from utils.logger import logger


def demo_industry_model():
    """演示行业模型功能"""
    print("=== 行业模型演示 ===")
    
    # 创建行业模型
    industry = IndustryModel(
        industry_code="010000",
        industry_name="农林牧渔",
        industry_level=1,
        industry_desc="农业、林业、畜牧业、渔业相关行业"
    )
    
    print(f"行业代码: {industry.industry_code}")
    print(f"行业名称: {industry.industry_name}")
    print(f"行业层级: {industry.industry_level}")
    print(f"行业描述: {industry.industry_desc}")
    print(f"行业状态: {industry.status.value}")
    
    # 转换为字典
    industry_dict = industry.to_dict()
    print(f"转换为字典: {industry_dict}")
    
    # 从字典创建
    new_industry = IndustryModel.from_dict(industry_dict)
    print(f"从字典创建: {new_industry}")
    
    print()


def demo_stock_industry_model():
    """演示股票行业映射模型功能"""
    print("=== 股票行业映射模型演示 ===")
    
    # 创建股票行业映射
    mapping = StockIndustryModel(
        stock_code="000001",
        stock_name="平安银行",
        industry_code="080000",
        industry_name="食品饮料",
        industry_level=1,
        confidence=0.95
    )
    
    print(f"股票代码: {mapping.stock_code}")
    print(f"股票名称: {mapping.stock_name}")
    print(f"行业代码: {mapping.industry_code}")
    print(f"行业名称: {mapping.industry_name}")
    print(f"置信度: {mapping.confidence}")
    print(f"是否高置信度: {mapping.is_high_confidence()}")
    
    # 转换为字典
    mapping_dict = mapping.to_dict()
    print(f"转换为字典: {mapping_dict}")
    
    print()


def demo_data_validation():
    """演示数据验证功能"""
    print("=== 数据验证演示 ===")
    
    # 创建测试数据
    industries = [
        IndustryModel("010000", "农林牧渔", 1),
        IndustryModel("020000", "采掘", 1),
        IndustryModel("010100", "农业", 2, parent_code="010000"),
    ]
    
    mappings = [
        StockIndustryModel("000001", "平安银行", "080000", "食品饮料", 1),
        StockIndustryModel("000002", "万科A", "110000", "房地产", 1),
    ]
    
    print(f"创建了 {len(industries)} 个行业模型")
    print(f"创建了 {len(mappings)} 个股票映射模型")
    
    # 验证数据格式
    print("\n验证数据格式:")
    for i, industry in enumerate(industries):
        print(f"  行业 {i+1}: {industry.industry_code} - {industry.industry_name}")
    
    for i, mapping in enumerate(mappings):
        print(f"  映射 {i+1}: {mapping.stock_code} -> {mapping.industry_code}")
    
    print()


def demo_configuration():
    """演示配置功能"""
    print("=== 配置演示 ===")
    
    try:
        from config import config
        
        print("数据库配置:")
        print(f"  主机: {config.database.host}")
        print(f"  端口: {config.database.port}")
        print(f"  数据库: {config.database.database}")
        print(f"  用户名: {config.database.username}")
        
        print("\n万得Wind配置:")
        print(f"  服务器: {config.wind.wind_server}")
        print(f"  端口: {config.wind.wind_port}")
        print(f"  更新频率: {config.wind.update_frequency_hours}小时")
        
        print("\nTushare配置:")
        print(f"  基础URL: {config.tushare.base_url}")
        print(f"  超时时间: {config.tushare.timeout}秒")
        
        print("\n日志配置:")
        print(f"  级别: {config.log.level}")
        print(f"  文件路径: {config.log.file_path}")
        
    except ImportError:
        print("配置模块导入失败，请检查config.py文件")
    
    print()


def demo_logging():
    """演示日志功能"""
    print("=== 日志功能演示 ===")
    
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")
    
    print("日志已记录到文件中")
    print()


def main():
    """主函数"""
    print("万得行业分类模块演示程序")
    print("=" * 50)
    
    try:
        # 运行各种演示
        demo_industry_model()
        demo_stock_industry_model()
        demo_data_validation()
        demo_configuration()
        demo_logging()
        
        print("演示程序执行完成！")
        print("\n下一步:")
        print("1. 配置数据库连接信息")
        print("2. 运行 python main.py --action init 初始化数据库")
        print("3. 运行 python main.py --action update 更新数据")
        print("4. 运行 python main.py --action query --level 1 查询数据")
        
    except Exception as e:
        logger.error(f"演示程序执行失败: {e}")
        print(f"执行失败: {e}")


if __name__ == "__main__":
    main() 