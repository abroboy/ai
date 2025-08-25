"""
热度排序功能测试脚本
"""

import sys
import os
import requests
import json
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_heat_sorting():
    """测试热度排序功能"""
    print("=" * 60)
    print("🔥 热度排序功能测试")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    base_url = "http://localhost:5002"
    
    # 测试不同的排序方式
    sort_tests = [
        {
            'name': '热度降序（高到低）',
            'sort_by': 'heat_score',
            'sort_order': 'desc'
        },
        {
            'name': '热度升序（低到高）',
            'sort_by': 'heat_score',
            'sort_order': 'asc'
        },
        {
            'name': '发布时间降序',
            'sort_by': 'publish_time',
            'sort_order': 'desc'
        },
        {
            'name': '情感得分降序',
            'sort_by': 'sentiment_score',
            'sort_order': 'desc'
        },
        {
            'name': '标题字母顺序',
            'sort_by': 'title',
            'sort_order': 'asc'
        }
    ]
    
    for test in sort_tests:
        print(f"🧪 测试: {test['name']}")
        print(f"   排序字段: {test['sort_by']}")
        print(f"   排序方向: {test['sort_order']}")
        
        try:
            # 构建请求URL
            url = f"{base_url}/api/hotspots"
            params = {
                'page': 1,
                'per_page': 10,
                'sort_by': test['sort_by'],
                'sort_order': test['sort_order']
            }
            
            # 发送请求
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    hotspots = data['data']['hotspots']
                    sorting_info = data['data']['sorting']
                    
                    print(f"   ✅ 请求成功")
                    print(f"   返回数据量: {len(hotspots)} 条")
                    print(f"   实际排序: {sorting_info['sort_by']} {sorting_info['sort_order']}")
                    
                    # 显示前3条数据的热度值
                    if hotspots:
                        print(f"   前3条数据热度值:")
                        for i, hotspot in enumerate(hotspots[:3]):
                            heat_score = hotspot.get('heat_score', 'N/A')
                            title = hotspot.get('title', 'N/A')[:30] + '...'
                            print(f"     {i+1}. {heat_score} - {title}")
                    
                    # 验证排序是否正确
                    if test['sort_by'] == 'heat_score' and hotspots:
                        heat_scores = [h.get('heat_score', 0) for h in hotspots if h.get('heat_score') is not None]
                        if len(heat_scores) > 1:
                            if test['sort_order'] == 'desc':
                                is_sorted = all(heat_scores[i] >= heat_scores[i+1] for i in range(len(heat_scores)-1))
                            else:
                                is_sorted = all(heat_scores[i] <= heat_scores[i+1] for i in range(len(heat_scores)-1))
                            
                            if is_sorted:
                                print(f"   ✅ 排序验证通过")
                            else:
                                print(f"   ❌ 排序验证失败")
                        else:
                            print(f"   ⚠️  数据不足，无法验证排序")
                    
                else:
                    print(f"   ❌ API返回错误: {data.get('error', '未知错误')}")
            else:
                print(f"   ❌ HTTP请求失败: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ 网络请求失败: {e}")
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
        
        print()
    
    # 测试前端排序功能
    print("🌐 前端排序功能测试")
    print("   请访问: http://localhost:5002")
    print("   点击表格头部进行排序测试")
    print("   支持排序的字段:")
    print("   - 标题 (title)")
    print("   - 类型 (hotspot_type)")
    print("   - 级别 (hotspot_level)")
    print("   - 来源 (source)")
    print("   - 热度 (heat_score) 🔥")
    print("   - 情感 (sentiment_score)")
    print("   - 状态 (status)")
    print("   - 发布时间 (publish_time)")
    print()

def test_heat_score_distribution():
    """测试热度分数分布"""
    print("📊 热度分数分布测试")
    print("-" * 40)
    
    try:
        url = "http://localhost:5002/api/hotspots"
        params = {
            'page': 1,
            'per_page': 50,
            'sort_by': 'heat_score',
            'sort_order': 'desc'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                hotspots = data['data']['hotspots']
                
                if hotspots:
                    heat_scores = [h.get('heat_score', 0) for h in hotspots if h.get('heat_score') is not None]
                    
                    if heat_scores:
                        print(f"数据量: {len(heat_scores)} 条")
                        print(f"最高热度: {max(heat_scores)}")
                        print(f"最低热度: {min(heat_scores)}")
                        print(f"平均热度: {sum(heat_scores) / len(heat_scores):.2f}")
                        
                        # 热度分布
                        ranges = [(0, 20, '低热度'), (21, 40, '中低热度'), (41, 60, '中等热度'), (61, 80, '中高热度'), (81, 100, '高热度')]
                        
                        print("\n热度分布:")
                        for min_val, max_val, label in ranges:
                            count = sum(1 for score in heat_scores if min_val <= score <= max_val)
                            percentage = (count / len(heat_scores)) * 100
                            print(f"  {label} ({min_val}-{max_val}): {count} 条 ({percentage:.1f}%)")
                        
                        # 显示前10条高热度数据
                        print("\n🔥 前10条高热度数据:")
                        for i, hotspot in enumerate(hotspots[:10]):
                            heat_score = hotspot.get('heat_score', 'N/A')
                            title = hotspot.get('title', 'N/A')[:40] + '...'
                            source = hotspot.get('source', 'N/A')
                            print(f"  {i+1:2d}. {heat_score:5.1f} - {title}")
                            print(f"      来源: {source}")
                    else:
                        print("❌ 没有找到热度数据")
                else:
                    print("❌ 没有返回数据")
            else:
                print(f"❌ API返回错误: {data.get('error', '未知错误')}")
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def main():
    """主函数"""
    print("🚀 开始热度排序功能测试")
    print()
    
    # 测试基本排序功能
    test_heat_sorting()
    
    # 测试热度分布
    test_heat_score_distribution()
    
    print("=" * 60)
    print("✅ 热度排序功能测试完成")
    print("💡 提示: 访问 http://localhost:5002 查看Web界面")
    print("💡 提示: 点击表格头部进行交互式排序")

if __name__ == "__main__":
    main() 