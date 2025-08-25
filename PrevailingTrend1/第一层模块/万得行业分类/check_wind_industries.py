import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def check_wind_industries():
    """查看万得行业分类数据"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # 查看万得行业分类表结构
        cursor.execute("DESCRIBE wind_industry_classification")
        columns = cursor.fetchall()
        print("万得行业分类表结构:")
        for col in columns:
            print(f"  {col['Field']} - {col['Type']}")
        
        print("\n" + "="*50)
        
        # 查看前10条行业数据
        cursor.execute("SELECT * FROM wind_industry_classification LIMIT 10")
        industries = cursor.fetchall()
        print("万得行业分类示例:")
        for industry in industries:
            print(f"  {industry['industry_code']} - {industry['industry_name']}")
        
        print("\n" + "="*50)
        
        # 统计行业数量
        cursor.execute("SELECT COUNT(*) as total FROM wind_industry_classification")
        total = cursor.fetchone()['total']
        print(f"万得行业分类总数: {total}")
        
        # 按层级统计
        cursor.execute("SELECT level, COUNT(*) as count FROM wind_industry_classification GROUP BY level ORDER BY level")
        levels = cursor.fetchall()
        print("\n按层级统计:")
        for level in levels:
            print(f"  层级{level['level']}: {level['count']}个行业")
        
        conn.close()
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    check_wind_industries() 