import requests
import json

def test_api():
    """测试管理台API接口"""
    base_url = "http://127.0.0.1:5001"
    
    print("=" * 60)
    print("🔍 测试管理台API接口")
    print("=" * 60)
    
    # 1. 测试统计接口
    print("\n1. 测试统计接口:")
    try:
        response = requests.get(f"{base_url}/api/stats")
        data = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ 统计接口失败: {e}")
    
    # 2. 测试股票列表接口 - 港股通
    print("\n2. 测试港股通股票列表:")
    try:
        response = requests.get(f"{base_url}/api/stocks?filter=hk&page=1&page_size=20")
        data = response.json()
        print(f"状态码: {response.status_code}")
        if data.get('success'):
            stocks = data['data']['stocks']
            total = data['data']['total']
            print(f"港股通总数: {total}")
            print(f"当前页显示: {len(stocks)} 只股票")
            print("前5只港股:")
            for i, stock in enumerate(stocks[:5]):
                print(f"  {i+1}. {stock['stock_code']} {stock['stock_name']} -> {stock.get('industry_name', '未映射')}")
        else:
            print(f"❌ 接口返回错误: {data.get('message')}")
    except Exception as e:
        print(f"❌ 港股通接口失败: {e}")
    
    # 3. 测试股票统计接口
    print("\n3. 测试股票统计接口:")
    try:
        response = requests.get(f"{base_url}/api/stocks/stats")
        data = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ 股票统计接口失败: {e}")
    
    # 4. 测试健康检查接口
    print("\n4. 测试健康检查接口:")
    try:
        response = requests.get(f"{base_url}/api/health")
        data = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ 健康检查接口失败: {e}")

if __name__ == "__main__":
    test_api() 