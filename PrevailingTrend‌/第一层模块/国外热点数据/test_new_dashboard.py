#!/usr/bin/env python3
"""
测试新的dashboard页面功能
"""

import requests
import json
from datetime import datetime

def test_api_endpoints():
    """测试API端点"""
    base_url = "http://localhost:5003"  # 假设端口是5003
    
    print("=== 测试国外热点数据API端点 ===")
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"健康检查: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"健康检查失败: {e}")
    
    # 测试统计数据API
    try:
        response = requests.get(f"{base_url}/api/statistics")
        print(f"统计数据API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"统计数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"统计数据API失败: {e}")
    
    # 测试热点数据API
    try:
        response = requests.get(f"{base_url}/api/hotspots?limit=5")
        print(f"热点数据API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"热点数据数量: {len(data.get('data', []))}")
            if data.get('data'):
                print(f"第一条数据: {json.dumps(data['data'][0], indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"热点数据API失败: {e}")

def test_dashboard_page():
    """测试dashboard页面"""
    base_url = "http://localhost:5003"
    
    print("\n=== 测试Dashboard页面 ===")
    
    try:
        response = requests.get(f"{base_url}/dashboard")
        print(f"Dashboard页面: {response.status_code}")
        if response.status_code == 200:
            print("Dashboard页面加载成功")
            # 检查页面内容
            content = response.text
            if "国外热点数据分析" in content:
                print("✓ 页面标题正确")
            if "侧边导航栏" in content or "sidebar" in content:
                print("✓ 侧边栏结构存在")
            if "统计卡片区域" in content or "stats-section" in content:
                print("✓ 统计卡片区域存在")
            if "热点数据列表" in content:
                print("✓ 数据表格区域存在")
        else:
            print("Dashboard页面加载失败")
    except Exception as e:
        print(f"Dashboard页面测试失败: {e}")

def main():
    """主函数"""
    print(f"开始测试 - {datetime.now()}")
    
    # 测试API端点
    test_api_endpoints()
    
    # 测试dashboard页面
    test_dashboard_page()
    
    print(f"\n测试完成 - {datetime.now()}")

if __name__ == "__main__":
    main() 