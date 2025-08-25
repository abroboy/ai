import requests
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

def get_all_stocks():
    """获取所有股票数据"""
    all_stocks = []
    
    # 尝试不同的市场类型
    markets = [
        'm:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23',  # A股
        'm:128+t:3,m:128+t:4,m:128+t:1,m:128+t:2',     # 港股
        'm:105+t:31,m:105+t:32,m:105+t:33,m:105+t:34'  # 美股
    ]
    
    for i, market in enumerate(markets):
        market_name = ['A股', '港股', '美股'][i]
        print(f"获取{market_name}数据...")
        
        # 分页获取
        for page in range(1, 101):  # 最多100页
            print(f"  获取{market_name}第{page}页数据...")
            
            url = "http://push2.eastmoney.com/api/qt/clist/get"
            params = {
                'pn': page,
                'pz': 10000,
                'po': 1,
                'np': 1,
                'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
                'fltt': 2,
                'invt': 2,
                'fid': 'f3',
                'fs': market,
                'fields': 'f12,f14'
            }
            
            try:
                response = requests.get(url, params=params, timeout=30)
                data = response.json()
                
                if data['rc'] == 0 and 'data' in data and 'diff' in data['data']:
                    page_stocks = []
                    for item in data['data']['diff']:
                        stock_code = str(item.get('f12', ''))
                        stock_name = item.get('f14', '')
                        if stock_code and stock_name:
                            page_stocks.append({
                                'stock_code': stock_code,
                                'stock_name': stock_name,
                                'industry_code': '',
                                'industry_name': '',
                                'mapping_status': 'pending',
                                'confidence': 0.0
                            })
                    
                    all_stocks.extend(page_stocks)
                    print(f"    第{page}页获取到 {len(page_stocks)} 只股票")
                    
                    if len(page_stocks) < 10000:
                        print(f"    已到最后一页，停止获取")
                        break
                        
            except Exception as e:
                print(f"    获取失败: {e}")
                continue
    
    return all_stocks

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
        for stock in unique_list:
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
        
        connection.commit()
        
        # 统计
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping")
        total = cursor.fetchone()[0]
        print(f"总股票数: {total}")
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE LENGTH(stock_code) = 6")
        a_stocks = cursor.fetchone()[0]
        print(f"A股数量: {a_stocks}")
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5")
        hk_stocks = cursor.fetchone()[0]
        print(f"港股数量: {hk_stocks}")
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE LENGTH(stock_code) > 6")
        us_stocks = cursor.fetchone()[0]
        print(f"美股数量: {us_stocks}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"保存失败: {e}")
        return False

if __name__ == "__main__":
    print("开始获取所有股票数据...")
    stocks = get_all_stocks()
    print(f"总共获取到 {len(stocks)} 只股票")
    
    if stocks:
        if save_to_db(stocks):
            print("✅ 成功获取并保存股票数据！")
        else:
            print("❌ 保存失败！")
    else:
        print("❌ 未获取到数据！") 