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

def get_akshare_stocks():
    """使用AKShare获取A股数据"""
    print("开始使用AKShare获取A股数据...")
    
    try:
        # 获取A股列表
        stocks = ak.stock_info_a_code_name()
        print(f"✅ AKShare获取到 {len(stocks)} 只A股")
        
        # 转换为列表格式
        stock_list = []
        for _, row in stocks.iterrows():
            stock_code = str(row['code'])
            stock_name = row['name']
            if stock_code and stock_name and len(stock_code) == 6:
                stock_list.append({
                    'stock_code': stock_code,
                    'stock_name': stock_name,
                    'industry_code': '',
                    'industry_name': '',
                    'mapping_status': 'pending',
                    'confidence': 0.0
                })
        
        print(f"✅ 有效股票数量: {len(stock_list)}")
        return stock_list
        
    except Exception as e:
        print(f"❌ AKShare获取失败: {e}")
        return []

def save_to_db(stocks):
    """保存到数据库"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 清空现有数据
        print("清空现有数据...")
        cursor.execute("DELETE FROM stock_industry_mapping")
        
        # 去重
        unique_stocks = {}
        for stock in stocks:
            key = stock['stock_code']
            if key not in unique_stocks:
                unique_stocks[key] = stock
        
        unique_list = list(unique_stocks.values())
        
        # 插入数据
        print(f"插入 {len(unique_list)} 条数据...")
        for i, stock in enumerate(unique_list):
            sql = """
            INSERT INTO stock_industry_mapping 
            (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                stock['stock_code'],
                stock['stock_name'],
                stock['industry_code'],
                stock['industry_name'],
                stock['mapping_status'],
                stock['confidence']
            ))
            
            if (i + 1) % 1000 == 0:
                print(f"  已插入 {i + 1} 条数据...")
        
        connection.commit()
        
        # 统计
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping")
        total = cursor.fetchone()[0]
        print(f"✅ 总股票数: {total}")
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE industry_name != ''")
        mapped = cursor.fetchone()[0]
        print(f"✅ 已映射股票数: {mapped}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 开始使用AKShare获取完整股票数据")
    print("=" * 60)
    
    # 获取股票数据
    stocks = get_akshare_stocks()
    
    if stocks:
        if save_to_db(stocks):
            print("\n" + "=" * 60)
            print("✅ 成功获取并保存股票数据！")
            print(f"📊 数据统计:")
            print(f"   - 总股票数: {len(stocks)}")
            print(f"   - 数据来源: AKShare")
            print("🌐 访问 http://127.0.0.1:5001 查看数据")
            print("=" * 60)
        else:
            print("❌ 保存失败！")
    else:
        print("❌ 未获取到数据！")

if __name__ == "__main__":
    main() 