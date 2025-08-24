import akshare as ak
import pymysql
import time

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def get_industry_classification():
    """获取行业分类信息"""
    print("尝试获取行业分类信息...")
    
    try:
        # 尝试获取东方财富行业分类
        industry = ak.stock_board_industry_name_em()
        print(f"✅ 东方财富行业分类数量: {len(industry)}")
        print("前5个行业:")
        print(industry.head())
        return industry
    except Exception as e:
        print(f"❌ 东方财富行业分类获取失败: {e}")
        return None

def get_stock_industry_mapping():
    """获取股票行业映射"""
    print("尝试获取股票行业映射...")
    
    try:
        # 尝试获取申万行业分类
        sw_industry = ak.stock_board_industry_cons_sw(symbol="801010")
        print(f"✅ 申万农林牧渔行业股票数量: {len(sw_industry)}")
        print("前5只股票:")
        print(sw_industry.head())
        return sw_industry
    except Exception as e:
        print(f"❌ 申万行业映射获取失败: {e}")
        return None

def try_different_industry_sources():
    """尝试不同的行业数据源"""
    print("=" * 60)
    print("🔍 尝试不同的行业数据源")
    print("=" * 60)
    
    # 1. 东方财富行业分类
    print("\n1. 东方财富行业分类:")
    industry = get_industry_classification()
    
    # 2. 申万行业映射
    print("\n2. 申万行业映射:")
    stock_industry = get_stock_industry_mapping()
    
    # 3. 尝试获取具体行业的股票
    print("\n3. 尝试获取具体行业股票:")
    try:
        # 银行行业
        bank_stocks = ak.stock_board_industry_cons_sw(symbol="801780")
        print(f"✅ 申万银行行业股票数量: {len(bank_stocks)}")
        print("银行股票示例:")
        print(bank_stocks.head())
    except Exception as e:
        print(f"❌ 银行行业获取失败: {e}")
    
    # 4. 尝试获取所有申万一级行业
    print("\n4. 申万一级行业列表:")
    try:
        sw_industries = ak.stock_board_industry_name_sw()
        print(f"✅ 申万一级行业数量: {len(sw_industries)}")
        print("申万一级行业:")
        print(sw_industries)
    except Exception as e:
        print(f"❌ 申万一级行业获取失败: {e}")

def main():
    """主函数"""
    try_different_industry_sources()

if __name__ == "__main__":
    main() 