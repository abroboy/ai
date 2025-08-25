import requests
import json

def debug_api():
    print("🔍 调试API响应")
    print("=" * 50)
    
    try:
        response = requests.get('http://localhost:5002/api/statistics', timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n原始响应数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if data.get('success'):
                stats = data['data']
                print(f"\n解析后的统计数据:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
        else:
            print(f"错误响应: {response.text}")
            
    except Exception as e:
        print(f"❌ 调试失败: {e}")

if __name__ == "__main__":
    debug_api() 