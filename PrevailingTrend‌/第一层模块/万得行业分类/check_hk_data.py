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

def check_hk_data():
    """检查港股数据"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=" * 60)
        print("🇭🇰 港股数据检查")
        print("=" * 60)
        
        # 检查港股数量
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5")
        hk_count = cursor.fetchone()[0]
        print(f"港股数量: {hk_count}")
        
        # 检查港股映射情况
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5 AND industry_name != ''")
        hk_mapped = cursor.fetchone()[0]
        print(f"已映射港股: {hk_mapped}")
        print(f"映射率: {hk_mapped/hk_count*100:.1f}%")
        
        # 显示港股示例
        print(f"\n港股示例:")
        cursor.execute("SELECT stock_code, stock_name, industry_name FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5 LIMIT 10")
        hk_examples = cursor.fetchall()
        for stock_code, stock_name, industry_name in hk_examples:
            print(f"  {stock_code} {stock_name} -> {industry_name}")
        
        # 检查港股行业分布
        print(f"\n港股行业分布TOP10:")
        cursor.execute("""
            SELECT industry_name, COUNT(*) as count 
            FROM stock_industry_mapping 
            WHERE LENGTH(stock_code) = 5 AND industry_name != '' 
            GROUP BY industry_name 
            ORDER BY count DESC 
            LIMIT 10
        """)
        industries = cursor.fetchall()
        for industry, count in industries:
            print(f"  {industry}: {count}只股票")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 60)
        print("✅ 港股数据检查完成！")
        print("🌐 访问 http://127.0.0.1:5001 查看管理台")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")

if __name__ == "__main__":
    check_hk_data() 