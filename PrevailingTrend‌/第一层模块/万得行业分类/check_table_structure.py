"""
检查数据库表结构
"""

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

def check_table_structure():
    """检查数据库表结构"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=" * 60)
        print("📋 数据库表结构检查")
        print("=" * 60)
        
        # 检查stock_industry_mapping表结构
        print("\n🏗️ stock_industry_mapping表结构:")
        cursor.execute("DESCRIBE stock_industry_mapping")
        columns = cursor.fetchall()
        for column in columns:
            print(f"  {column[0]}: {column[1]} {column[2]} {column[3]} {column[4]} {column[5]}")
        
        # 检查wind_industry_classification表结构
        print("\n🏗️ wind_industry_classification表结构:")
        cursor.execute("DESCRIBE wind_industry_classification")
        columns = cursor.fetchall()
        for column in columns:
            print(f"  {column[0]}: {column[1]} {column[2]} {column[3]} {column[4]} {column[5]}")
        
        # 检查表数据量
        print("\n📊 表数据量:")
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping")
        stock_count = cursor.fetchone()[0]
        print(f"  stock_industry_mapping: {stock_count}条记录")
        
        cursor.execute("SELECT COUNT(*) FROM wind_industry_classification")
        industry_count = cursor.fetchone()[0]
        print(f"  wind_industry_classification: {industry_count}条记录")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"检查表结构失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_table_structure() 