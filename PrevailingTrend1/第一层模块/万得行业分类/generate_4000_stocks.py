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

def generate_4000_a_stocks():
    """生成4000只A股数据"""
    print("开始生成4000只A股数据...")
    
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 清空现有数据
        print("清空现有股票数据...")
        cursor.execute("DELETE FROM stock_industry_mapping")
        
        # 生成4000只A股数据
        stocks = []
        for i in range(1, 4001):
            stock_code = f"{i:06d}"
            stock_name = f"A股公司{i:04d}"
            stocks.append((stock_code, stock_name, '', '', 'pending', '0.0000'))
        
        # 批量插入
        print(f"准备插入 {len(stocks)} 条股票数据...")
        sql = """
        INSERT INTO stock_industry_mapping
        (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(sql, stocks)
        conn.commit()
        
        # 验证结果
        cursor.execute("SELECT COUNT(*) as total FROM stock_industry_mapping")
        total_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) as a_stocks FROM stock_industry_mapping WHERE LENGTH(stock_code) = 6")
        a_stocks_count = cursor.fetchone()[0]
        
        print(f"✅ 成功插入 {total_count} 只股票数据")
        print(f"📊 A股数量: {a_stocks_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 生成数据失败: {e}")

if __name__ == "__main__":
    generate_4000_a_stocks() 