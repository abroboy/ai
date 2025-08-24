import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def count_stocks():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    # 统计A股数量 (6位数字代码，以0、3、6开头)
    cursor.execute("SELECT COUNT(*) as a_stocks FROM stock_industry_mapping WHERE LENGTH(stock_code) = 6 AND (stock_code LIKE '0%' OR stock_code LIKE '3%' OR stock_code LIKE '6%')")
    a_stocks = cursor.fetchone()['a_stocks']
    
    # 统计港股通数量 (5位数字代码)
    cursor.execute("SELECT COUNT(*) as hk_stocks FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5")
    hk_stocks = cursor.fetchone()['hk_stocks']
    
    # 统计总数
    cursor.execute("SELECT COUNT(*) as total FROM stock_industry_mapping")
    total = cursor.fetchone()['total']
    
    print(f"A股数量: {a_stocks}")
    print(f"港股通数量: {hk_stocks}")
    print(f"总股票数: {total}")
    
    # 显示一些A股示例
    cursor.execute("SELECT stock_code, stock_name FROM stock_industry_mapping WHERE LENGTH(stock_code) = 6 AND (stock_code LIKE '0%' OR stock_code LIKE '3%' OR stock_code LIKE '6%') LIMIT 10")
    a_stock_examples = cursor.fetchall()
    print("\nA股示例:")
    for stock in a_stock_examples:
        print(f"  {stock['stock_code']} - {stock['stock_name']}")
    
    # 显示一些港股通示例
    cursor.execute("SELECT stock_code, stock_name FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5 LIMIT 10")
    hk_stock_examples = cursor.fetchall()
    print("\n港股通示例:")
    for stock in hk_stock_examples:
        print(f"  {stock['stock_code']} - {stock['stock_name']}")
    
    conn.close()

if __name__ == "__main__":
    count_stocks() 