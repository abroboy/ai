#!/usr/bin/env python3
"""
测试API返回的数据格式
"""

import requests
import json

def test_api_data():
    """测试API数据格式"""
    base_url = "http://localhost:5004"
    
    print("=== 测试API数据格式 ===")
    
    # 测试热点数据API
    try:
        response = requests.get(f"{base_url}/api/hotspots?limit=5")
        if response.status_code == 200:
            data = response.json()
            print("✓ 热点数据API响应成功")
            
            if data.get('success') and data.get('data'):
                hotspots = data['data']
                print(f"获取到 {len(hotspots)} 条热点数据")
                
                for i, hotspot in enumerate(hotspots, 1):
                    print(f"\n数据 {i}:")
                    print(f"  标题: {hotspot.get('title', 'N/A')}")
                    print(f"  heat_score: {hotspot.get('heat_score')} (类型: {type(hotspot.get('heat_score'))})")
                    print(f"  sentiment_score: {hotspot.get('sentiment_score')} (类型: {type(hotspot.get('sentiment_score'))})")
                    
                    # 测试JavaScript处理逻辑
                    heat_score = hotspot.get('heat_score')
                    if heat_score is not None:
                        try:
                            if hasattr(heat_score, 'toString'):
                                score = float(heat_score.toString())
                                print(f"  ✓ heat_score转换成功: {score}")
                            else:
                                score = float(heat_score)
                                print(f"  ✓ heat_score转换成功: {score}")
                        except Exception as e:
                            print(f"  ✗ heat_score转换失败: {e}")
            else:
                print("✗ API返回数据格式错误")
                print(f"响应内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"✗ API请求失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
    
    # 测试统计数据API
    try:
        response = requests.get(f"{base_url}/api/statistics")
        if response.status_code == 200:
            data = response.json()
            print("\n✓ 统计数据API响应成功")
            print(f"统计数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"\n✗ 统计数据API请求失败: {response.status_code}")
    except Exception as e:
        print(f"\n✗ 统计数据测试失败: {e}")

if __name__ == "__main__":
    test_api_data() 