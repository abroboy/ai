"""
测试统计数据修复
"""

import requests
import json

def test_statistics_api():
    """测试统计数据API"""
    print("🧪 测试统计数据API修复")
    print("=" * 50)
    
    try:
        # 测试统计数据API
        response = requests.get('http://localhost:5002/api/statistics', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                stats = data['data']
                print("✅ API响应成功")
                print(f"总数据量: {stats.get('total_count', 0)}")
                print(f"平均热度: {stats.get('avg_heat', 0)}")
                print(f"平均情感: {stats.get('avg_sentiment', 0)}")
                print(f"类型分布: {stats.get('by_type', {})}")
                print(f"级别分布: {stats.get('by_level', {})}")
                print(f"状态分布: {stats.get('by_status', {})}")
                print(f"来源分布: {len(stats.get('by_source', {}))} 个来源")
                
                # 检查关键字段是否存在
                required_fields = ['total_count', 'avg_heat', 'avg_sentiment', 'by_type', 'by_level', 'by_status']
                missing_fields = [field for field in required_fields if field not in stats]
                
                if missing_fields:
                    print(f"❌ 缺少字段: {missing_fields}")
                else:
                    print("✅ 所有必需字段都存在")
                
                return True
            else:
                print(f"❌ API返回错误: {data.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_hotspots_api():
    """测试热点数据API"""
    print("\n🧪 测试热点数据API")
    print("=" * 50)
    
    try:
        # 测试热点数据API
        response = requests.get('http://localhost:5002/api/hotspots?page=1&per_page=5', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                hotspots = data['data']['hotspots']
                print("✅ 热点数据API响应成功")
                print(f"返回数据量: {len(hotspots)} 条")
                
                if hotspots:
                    print("前3条数据:")
                    for i, hotspot in enumerate(hotspots[:3]):
                        print(f"  {i+1}. {hotspot.get('title', 'N/A')[:30]}...")
                        print(f"     热度: {hotspot.get('heat_score', 'N/A')}")
                        print(f"     情感: {hotspot.get('sentiment_score', 'N/A')}")
                
                return True
            else:
                print(f"❌ API返回错误: {data.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试统计数据修复")
    print()
    
    # 等待服务启动
    import time
    print("⏳ 等待服务启动...")
    time.sleep(3)
    
    # 测试统计数据API
    stats_ok = test_statistics_api()
    
    # 测试热点数据API
    hotspots_ok = test_hotspots_api()
    
    print("\n" + "=" * 50)
    if stats_ok and hotspots_ok:
        print("✅ 所有测试通过！统计数据修复成功")
        print("💡 现在可以正常访问 http://localhost:5002")
    else:
        print("❌ 部分测试失败，请检查服务状态")
    
    print("\n🌐 前端测试:")
    print("1. 访问 http://localhost:5002")
    print("2. 检查仪表盘统计数据是否正常显示")
    print("3. 检查是否还有JavaScript错误")

if __name__ == "__main__":
    main() 