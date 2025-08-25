import pymysql

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def check_database():
    """检查数据库状态"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=" * 60)
        print("📊 数据库状态检查")
        print("=" * 60)
        
        # 检查股票表
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping")
        stock_count = cursor.fetchone()[0]
        print(f"📈 股票表记录数: {stock_count}")
        
        # 检查行业分类表
        cursor.execute("SELECT COUNT(*) FROM wind_industry_classification")
        industry_count = cursor.fetchone()[0]
        print(f"🏭 行业分类表记录数: {industry_count}")
        
        # 检查已映射的股票
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE industry_name != ''")
        mapped_count = cursor.fetchone()[0]
        print(f"✅ 已映射股票数: {mapped_count}")
        
        # 检查未映射的股票
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE industry_name = '' OR industry_name IS NULL")
        unmapped_count = cursor.fetchone()[0]
        print(f"⏳ 未映射股票数: {unmapped_count}")
        
        # 显示行业分类示例
        print(f"\n🏭 行业分类示例:")
        cursor.execute("SELECT * FROM wind_industry_classification LIMIT 5")
        industries = cursor.fetchall()
        for industry in industries:
            print(f"  {industry}")
        
        # 显示股票示例
        print(f"\n📈 股票示例:")
        cursor.execute("SELECT stock_code, stock_name, industry_name FROM stock_industry_mapping LIMIT 5")
        stocks = cursor.fetchall()
        for stock in stocks:
            print(f"  {stock[0]} {stock[1]} -> {stock[2]}")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 60)
        print("✅ 数据库检查完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")

if __name__ == "__main__":
    check_database() 