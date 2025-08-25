"""
数据库初始化脚本
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

def create_tables():
    """创建数据库表"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 创建行业分类表
        industry_table_sql = """
        CREATE TABLE IF NOT EXISTS wind_industry_classification (
            id INT AUTO_INCREMENT PRIMARY KEY,
            industry_code VARCHAR(20) UNIQUE NOT NULL,
            industry_name VARCHAR(100) NOT NULL,
            level INT NOT NULL,
            parent_code VARCHAR(20),
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        
        # 创建股票行业映射表
        stock_table_sql = """
        CREATE TABLE IF NOT EXISTS stock_industry_mapping (
            id INT AUTO_INCREMENT PRIMARY KEY,
            stock_code VARCHAR(20) NOT NULL,
            stock_name VARCHAR(100),
            industry_code VARCHAR(20) NOT NULL,
            industry_name VARCHAR(100),
            mapping_status VARCHAR(20) DEFAULT 'confirmed',
            confidence DECIMAL(5,4) DEFAULT 1.0000,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        
        cursor.execute(industry_table_sql)
        cursor.execute(stock_table_sql)
        
        connection.commit()
        print("数据库表创建成功")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"创建数据库表失败: {e}")
        return False

def add_sample_data():
    """添加示例数据"""
    try:
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
        
        connection.commit()
        print(f"示例数据添加完成: {len(industries)}个行业, {len(stocks)}只股票")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"添加示例数据失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 数据库初始化 ===")
    
    # 创建表
    if create_tables():
        # 添加示例数据
        add_sample_data()
        print("数据库初始化完成！")
    else:
        print("数据库初始化失败！")

if __name__ == "__main__":
    main() 