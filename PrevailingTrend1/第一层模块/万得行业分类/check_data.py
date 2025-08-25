import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def check_duplicates():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # 检查重复数据
        cursor.execute("""
            SELECT stock_code, stock_name, COUNT(*) as count 
            FROM stock_industry_mapping 
            GROUP BY stock_code, stock_name 
            ORDER BY count DESC 
            LIMIT 10
        """)
        
        results = cursor.fetchall()
        print("重复数据统计:")
        for r in results:
            print(f"{r['stock_code']} - {r['stock_name']}: {r['count']}条")
        
        # 检查唯一股票数量
        cursor.execute("SELECT COUNT(DISTINCT stock_code) as unique_stocks FROM stock_industry_mapping")
        unique_count = cursor.fetchone()['unique_stocks']
        print(f"\n唯一股票数量: {unique_count}")
        
        # 检查总记录数
        cursor.execute("SELECT COUNT(*) as total FROM stock_industry_mapping")
        total_count = cursor.fetchone()['total']
        print(f"总记录数: {total_count}")
        
        conn.close()
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    check_duplicates() 