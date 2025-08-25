import requests

def test_sector():
    """测试板块接口"""
    url = "http://push2.eastmoney.com/api/qt/clist/get"
    params = {
        'pn': 1,
        'pz': 100,
        'po': 1,
        'np': 1,
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': 2,
        'invt': 2,
        'fid': 'f3',
        'fs': 'b:801780',  # 银行板块
        'fields': 'f12,f14'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        
        print("响应数据:")
        print(f"rc: {data.get('rc')}")
        print(f"data长度: {len(data.get('data', {}).get('diff', []))}")
        
        if data['rc'] == 0 and 'data' in data and 'diff' in data['data']:
            stocks = data['data']['diff']
            print(f"银行板块股票数: {len(stocks)}")
            
            for i, stock in enumerate(stocks[:5]):  # 显示前5只
                print(f"  {i+1}. {stock.get('f12')} {stock.get('f14')}")
        else:
            print("未获取到数据")
            
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    test_sector() 