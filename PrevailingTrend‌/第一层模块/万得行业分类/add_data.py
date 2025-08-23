"""
添加示例数据到数据库
"""

import pymysql
import os

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def add_sample_data():
    """添加示例数据"""
    try:
        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 示例行业数据
        industries = [
            ('010000', '农林牧渔', 1, None, 'active'),
            ('020000', '采矿业', 1, None, 'active'),
            ('030000', '制造业', 1, None, 'active'),
            ('031000', '食品饮料', 2, '030000', 'active'),
            ('032000', '纺织服装', 2, '030000', 'active'),
            ('033000', '电子', 2, '030000', 'active'),
            ('100000', '金融业', 1, None, 'active'),
            ('101000', '银行', 2, '100000', 'active'),
            ('102000', '证券', 2, '100000', 'active'),
            ('103000', '保险', 2, '100000', 'active')
        ]
        
        # 示例股票数据
        stocks = [
            ('000001.SZ', '平安银行', '101000', '银行', 'confirmed', 0.95),
            ('000858.SZ', '五粮液', '031000', '食品饮料', 'confirmed', 0.98),
            ('002415.SZ', '海康威视', '033000', '电子', 'confirmed', 0.92),
            ('600519.SH', '贵州茅台', '031000', '食品饮料', 'confirmed', 0.99),
            ('600036.SH', '招商银行', '101000', '银行', 'confirmed', 0.95),
            ('000725.SZ', '京东方A', '033000', '电子', 'confirmed', 0.88),
            ('002594.SZ', '比亚迪', '033000', '电子', 'confirmed', 0.85)
        ]
        
        # 插入行业数据
        industry_sql = """
        INSERT INTO wind_industry_classification 
        (industry_code, industry_name, level, parent_code, status) 
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        industry_name = VALUES(industry_name),
        level = VALUES(level),
        parent_code = VALUES(parent_code),
        status = VALUES(status)
        """
        
        cursor.executemany(industry_sql, industries)
        
        # 插入股票数据
        stock_sql = """
        INSERT INTO stock_industry_mapping 
        (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence) 
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        stock_name = VALUES(stock_name),
        industry_code = VALUES(industry_code),
        industry_name = VALUES(industry_name),
        mapping_status = VALUES(mapping_status),
        confidence = VALUES(confidence)
        """
        
        cursor.executemany(stock_sql, stocks)
        
        # 提交事务
        connection.commit()
        
        print(f"示例数据添加完成: {len(industries)}个行业, {len(stocks)}只股票")
        
        # 查询统计信息
        cursor.execute("SELECT COUNT(*) FROM wind_industry_classification")
        industry_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping")
        stock_count = cursor.fetchone()[0]
        
        print(f"数据库统计: {industry_count}个行业, {stock_count}只股票")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"添加示例数据失败: {e}")
        return False

if __name__ == "__main__":
    add_sample_data() 