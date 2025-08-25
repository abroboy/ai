import requests
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

def get_sector_stocks():
    """获取板块股票数据"""
    all_stocks = []
    
    # 申万一级行业板块
    sectors = [
        '801010', '801020', '801030', '801040', '801050', '801080', '801110', '801120',
        '801130', '801140', '801150', '801160', '801170', '801180', '801200', '801210',
        '801230', '801710', '801720', '801730', '801740', '801750', '801760', '801770',
        '801780', '801790', '801880', '801890'
    ]
    
    sector_names = {
        '801010': '农林牧渔', '801020': '采掘', '801030': '化工', '801040': '钢铁',
        '801050': '有色金属', '801080': '电子', '801110': '家用电器', '801120': '食品饮料',
        '801130': '纺织服装', '801140': '轻工制造', '801150': '医药生物', '801160': '公用事业',
        '801170': '交通运输', '801180': '房地产', '801200': '商业贸易', '801210': '休闲服务',
        '801230': '综合', '801710': '建筑材料', '801720': '建筑装饰', '801730': '电气设备',
        '801740': '国防军工', '801750': '计算机', '801760': '传媒', '801770': '通信',
        '801780': '银行', '801790': '非银金融', '801880': '汽车', '801890': '机械设备'
    }
    
    for sector_code in sectors:
        print(f"获取板块 {sector_code} ({sector_names.get(sector_code, '')}) 的股票...")
        
        url = "http://80.push2.eastmoney.com/api/qt/clist/get"
        params = {
            'pn': 1,
            'pz': 10000,
            'po': 1,
            'np': 1,
            'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
            'fltt': 2,
            'invt': 2,
            'fid': 'f3',
            'fs': f'b:{sector_code}',
            'fields': 'f12,f14'
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if data['rc'] == 0 and 'data' in data and 'diff' in data['data']:
                sector_stocks = []
                for item in data['data']['diff']:
                    stock_code = str(item.get('f12', ''))
                    stock_name = item.get('f14', '')
                    if stock_code and stock_name and len(stock_code) == 6:
                        sector_stocks.append({
                            'stock_code': stock_code,
                            'stock_name': stock_name,
                            'industry_code': sector_code,
                            'industry_name': sector_names.get(sector_code, '')
                        })
                
                all_stocks.extend(sector_stocks)
                print(f"  获取到 {len(sector_stocks)} 只股票")
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  获取失败: {e}")
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
                'confirmed',
                1.0
            ))
        
        connection.commit()
        
        # 统计
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping")
        total = cursor.fetchone()[0]
        print(f"总股票数: {total}")
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE industry_name != ''")
        mapped = cursor.fetchone()[0]
        print(f"已映射股票数: {mapped}")
        
        # 按行业统计
        cursor.execute("""
            SELECT industry_name, COUNT(*) as count 
            FROM stock_industry_mapping 
            WHERE industry_name != '' 
            GROUP BY industry_name 
            ORDER BY count DESC
        """)
        industries = cursor.fetchall()
        print("\n行业分布:")
        for industry, count in industries:
            print(f"  {industry}: {count}只股票")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"保存失败: {e}")
        return False

if __name__ == "__main__":
    print("开始拉取板块股票数据...")
    stocks = get_sector_stocks()
    print(f"总共获取到 {len(stocks)} 只股票")
    
    if stocks:
        if save_to_db(stocks):
            print("✅ 成功获取并保存板块股票数据！")
        else:
            print("❌ 保存失败！")
    else:
        print("❌ 未获取到数据！") 