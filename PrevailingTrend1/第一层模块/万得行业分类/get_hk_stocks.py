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

def get_hk_stocks():
    """获取港股通数据"""
    print("尝试获取港股通数据...")
    
    methods = [
        ("港股通成分股", lambda: ak.stock_hk_ggt_components_em()),
        ("港股主板", lambda: ak.stock_hk_main_board_spot_em()),
        ("港股现货", lambda: ak.stock_hk_spot_em()),
        ("港股现货列表", lambda: ak.stock_hk_spot())
    ]
    
    all_hk_stocks = []
    
    for method_name, method_func in methods:
        try:
            print(f"\n尝试 {method_name}...")
            hk_data = method_func()
            print(f"✅ {method_name} 获取到 {len(hk_data)} 只股票")
            print("前5只股票:")
            print(hk_data.head())
            
            # 转换为标准格式
            stocks = []
            for _, row in hk_data.iterrows():
                # 尝试不同的列名
                stock_code = None
                stock_name = None
                
                # 常见的港股代码列名
                for code_col in ['代码', 'symbol', 'code', '股票代码', '港股代码']:
                    if code_col in row.index and row[code_col]:
                        stock_code = str(row[code_col])
                        break
                
                # 常见的股票名称列名
                for name_col in ['名称', 'name', '股票名称', '公司名称']:
                    if name_col in row.index and row[name_col]:
                        stock_name = str(row[name_col])
                        break
                
                if stock_code and stock_name:
                    stocks.append({
                        'stock_code': stock_code,
                        'stock_name': stock_name,
                        'industry_code': '',
                        'industry_name': '',
                        'mapping_status': 'pending',
                        'confidence': 0.0,
                        'market_type': 'HK'
                    })
            
            all_hk_stocks.extend(stocks)
            print(f"✅ 转换后有效股票: {len(stocks)}")
            
            if len(stocks) > 0:
                return all_hk_stocks
                
        except Exception as e:
            print(f"❌ {method_name} 失败: {e}")
            continue
    
    return all_hk_stocks

def save_hk_stocks_to_db(hk_stocks):
    """保存港股通数据到数据库"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print(f"准备插入 {len(hk_stocks)} 只港股...")
        
        inserted_count = 0
        for stock in hk_stocks:
            # 检查是否已存在
            cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE stock_code = %s", (stock['stock_code'],))
            if cursor.fetchone()[0] > 0:
                continue
                
            # 插入新记录
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
            inserted_count += 1
        
        connection.commit()
        
        # 统计
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE LENGTH(stock_code) = 6")
        a_stocks = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5")
        hk_stocks_count = cursor.fetchone()[0]
        
        print(f"✅ 成功插入 {inserted_count} 只港股")
        print(f"📊 数据统计:")
        print(f"   - 总股票数: {total}")
        print(f"   - A股数量: {a_stocks}")
        print(f"   - 港股数量: {hk_stocks_count}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🇭🇰 开始获取港股通数据")
    print("=" * 60)
    
    # 获取港股通数据
    hk_stocks = get_hk_stocks()
    
    if hk_stocks:
        print(f"\n总共获取到 {len(hk_stocks)} 只港股")
        
        if save_hk_stocks_to_db(hk_stocks):
            print("\n" + "=" * 60)
            print("✅ 港股通数据获取完成！")
            print("🌐 访问 http://127.0.0.1:5001 查看数据")
            print("=" * 60)
        else:
            print("❌ 保存失败！")
    else:
        print("❌ 未获取到港股通数据！")

if __name__ == "__main__":
    main() 