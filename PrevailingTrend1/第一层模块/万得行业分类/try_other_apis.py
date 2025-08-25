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

def try_sina_api():
    """尝试新浪财经接口"""
    print("尝试新浪财经接口...")
    
    url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
    params = {
        'page': 1,
        'num': 5000,
        'sort': 'symbol',
        'asc': 1,
        'node': 'hs_a',
        'symbol': '',
        '_s_r_a': 'page'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        
        stocks = []
        for item in data:
            stock_code = item.get('symbol', '').replace('sh', '').replace('sz', '')
            stock_name = item.get('name', '')
            if stock_code and stock_name and len(stock_code) == 6:
                stocks.append({
                    'stock_code': stock_code,
                    'stock_name': stock_name,
                    'industry_code': '',
                    'industry_name': '',
                    'mapping_status': 'pending',
                    'confidence': 0.0
                })
        
        print(f"新浪接口获取到 {len(stocks)} 只股票")
        return stocks
        
    except Exception as e:
        print(f"新浪接口失败: {e}")
        return []

def try_tencent_api():
    """尝试腾讯财经接口"""
    print("尝试腾讯财经接口...")
    
    url = "http://qt.gtimg.cn/q=sh000001"
    
    try:
        response = requests.get(url, timeout=30)
        print(f"腾讯接口响应: {response.text[:100]}")
        return []
        
    except Exception as e:
        print(f"腾讯接口失败: {e}")
        return []

def try_akshare_api():
    """尝试AKShare接口"""
    print("尝试AKShare接口...")
    
    try:
        import akshare as ak
        
        # 获取A股列表
        a_stocks = ak.stock_info_a_code_name()
        print(f"AKShare获取到 {len(a_stocks)} 只A股")
        
        stocks = []
        for _, row in a_stocks.iterrows():
            stock_code = str(row['code'])
            stock_name = row['name']
            if stock_code and stock_name and len(stock_code) == 6:
                stocks.append({
                    'stock_code': stock_code,
                    'stock_name': stock_name,
                    'industry_code': '',
                    'industry_name': '',
                    'mapping_status': 'pending',
                    'confidence': 0.0
                })
        
        return stocks
        
    except ImportError:
        print("AKShare未安装")
        return []
    except Exception as e:
        print(f"AKShare接口失败: {e}")
        return []

def try_tushare_api():
    """尝试Tushare接口"""
    print("尝试Tushare接口...")
    
    try:
        import tushare as ts
        ts.set_token('your_token')  # 需要设置token
        pro = ts.pro_api()
        
        # 获取A股列表
        data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,industry')
        
        stocks = []
        for _, row in data.iterrows():
            stock_code = row['symbol']
            stock_name = row['name']
            industry = row['industry']
            if stock_code and stock_name and len(stock_code) == 6:
                stocks.append({
                    'stock_code': stock_code,
                    'stock_name': stock_name,
                    'industry_code': '',
                    'industry_name': industry if industry else '',
                    'mapping_status': 'confirmed' if industry else 'pending',
                    'confidence': 1.0 if industry else 0.0
                })
        
        print(f"Tushare获取到 {len(stocks)} 只股票")
        return stocks
        
    except ImportError:
        print("Tushare未安装")
        return []
    except Exception as e:
        print(f"Tushare接口失败: {e}")
        return []

def try_eastmoney_v2():
    """尝试东方财富接口V2"""
    print("尝试东方财富接口V2...")
    
    # 尝试不同的参数组合
    urls = [
        "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14",
        "http://80.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14",
        "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0&fields=f12,f14"
    ]
    
    for i, url in enumerate(urls):
        try:
            print(f"  尝试URL {i+1}...")
            response = requests.get(url, timeout=30)
            data = response.json()
            
            if data['rc'] == 0 and 'data' in data and 'diff' in data['data']:
                stocks = []
                for item in data['data']['diff']:
                    stock_code = str(item.get('f12', ''))
                    stock_name = item.get('f14', '')
                    if stock_code and stock_name and len(stock_code) == 6:
                        stocks.append({
                            'stock_code': stock_code,
                            'stock_name': stock_name,
                            'industry_code': '',
                            'industry_name': '',
                            'mapping_status': 'pending',
                            'confidence': 0.0
                        })
                
                print(f"  获取到 {len(stocks)} 只股票")
                return stocks
                
        except Exception as e:
            print(f"  URL {i+1}失败: {e}")
            continue
    
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
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE industry_name != ''")
        mapped = cursor.fetchone()[0]
        print(f"已映射股票数: {mapped}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"保存失败: {e}")
        return False

def main():
    """主函数"""
    print("开始尝试其他接口...")
    
    # 尝试不同的接口
    apis = [
        try_eastmoney_v2,
        try_sina_api,
        try_akshare_api,
        try_tushare_api,
        try_tencent_api
    ]
    
    all_stocks = []
    
    for api_func in apis:
        try:
            stocks = api_func()
            if stocks and len(stocks) > len(all_stocks):
                all_stocks = stocks
                print(f"✅ 使用 {api_func.__name__} 接口获取到 {len(stocks)} 只股票")
                break
        except Exception as e:
            print(f"❌ {api_func.__name__} 接口失败: {e}")
            continue
    
    if all_stocks:
        if save_to_db(all_stocks):
            print("✅ 成功获取并保存股票数据！")
        else:
            print("❌ 保存失败！")
    else:
        print("❌ 所有接口都失败了！")

if __name__ == "__main__":
    main() 