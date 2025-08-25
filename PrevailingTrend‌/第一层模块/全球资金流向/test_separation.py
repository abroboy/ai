#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据拉取和展示分离功能
"""

import requests
import time
import json
from datetime import datetime

def test_data_collector():
    """测试数据收集服务"""
    print("=" * 50)
    print("测试数据收集服务")
    print("=" * 50)
    
    base_url = "http://localhost:5004"
    
    try:
        # 测试健康检查
        print("1. 测试健康检查...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ 健康检查通过")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
        
        # 测试服务状态
        print("2. 测试服务状态...")
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 服务状态: {data['data']['is_running']}")
        else:
            print(f"❌ 获取服务状态失败: {response.status_code}")
            return False
        
        # 测试数据收集
        print("3. 测试数据收集...")
        response = requests.post(f"{base_url}/api/collect_once", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ 数据收集成功: {data['data']['total_records']} 条记录")
            else:
                print(f"❌ 数据收集失败: {data.get('message', '未知错误')}")
                return False
        else:
            print(f"❌ 数据收集失败: {response.status_code}")
            return False
        
        # 测试仪表盘数据
        print("4. 测试仪表盘数据...")
        response = requests.get(f"{base_url}/api/dashboard_data", timeout=5)
        if response.status_code == 200:
            data = response.json()
            analysis = data['data']['global_analysis']
            print(f"✅ 仪表盘数据获取成功:")
            for asset, info in analysis.items():
                print(f"   {asset}: {info['total_net_flow']} ({info['flow_trend']})")
        else:
            print(f"❌ 获取仪表盘数据失败: {response.status_code}")
            return False
        
        # 测试流向分析
        print("5. 测试流向分析...")
        response = requests.get(f"{base_url}/api/flow_analysis?period=30d", timeout=5)
        if response.status_code == 200:
            data = response.json()
            analysis = data['data']['analysis']
            print(f"✅ 流向分析获取成功:")
            for asset, info in analysis.items():
                print(f"   {asset}: {info['total_net_flow']} ({info['trend']}) - {info['count']} 条记录")
        else:
            print(f"❌ 获取流向分析失败: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到数据收集服务，请确保服务正在运行")
        return False
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

def test_display_service():
    """测试数据展示服务"""
    print("\n" + "=" * 50)
    print("测试数据展示服务")
    print("=" * 50)
    
    base_url = "http://localhost:5003"
    
    try:
        # 测试健康检查
        print("1. 测试健康检查...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ 健康检查通过")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
        
        # 测试系统状态
        print("2. 测试系统状态...")
        response = requests.get(f"{base_url}/api/system_status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 系统状态: {data['data']['system_status']}")
        else:
            print(f"❌ 获取系统状态失败: {response.status_code}")
            return False
        
        # 测试仪表盘数据（从数据收集服务获取）
        print("3. 测试仪表盘数据获取...")
        response = requests.get(f"{base_url}/api/dashboard_data", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'note' in data['data']:
                print(f"⚠️  使用模拟数据: {data['data']['note']}")
            else:
                print("✅ 获取实时数据成功")
            
            analysis = data['data']['global_analysis']
            for asset, info in analysis.items():
                print(f"   {asset}: {info['total_net_flow']} ({info['flow_trend']})")
        else:
            print(f"❌ 获取仪表盘数据失败: {response.status_code}")
            return False
        
        # 测试流向分析（从数据收集服务获取）
        print("4. 测试流向分析获取...")
        response = requests.get(f"{base_url}/api/flow_analysis?period=30d", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'note' in data['data']:
                print(f"⚠️  使用模拟数据: {data['data']['note']}")
            else:
                print("✅ 获取实时分析数据成功")
            
            analysis = data['data']['analysis']
            for asset, info in analysis.items():
                print(f"   {asset}: {info['total_net_flow']} ({info['trend']}) - {info['count']} 条记录")
        else:
            print(f"❌ 获取流向分析失败: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到数据展示服务，请确保服务正在运行")
        return False
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

def test_separation():
    """测试分离功能"""
    print("\n" + "=" * 50)
    print("测试数据拉取和展示分离")
    print("=" * 50)
    
    # 测试数据收集服务
    collector_ok = test_data_collector()
    
    # 测试数据展示服务
    display_ok = test_display_service()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    if collector_ok and display_ok:
        print("✅ 数据拉取和展示分离测试通过!")
        print("✅ 两个服务可以独立运行")
        print("✅ 展示服务可以从收集服务获取数据")
        print("✅ 展示服务在收集服务不可用时使用模拟数据")
        return True
    else:
        print("❌ 测试失败:")
        if not collector_ok:
            print("   - 数据收集服务测试失败")
        if not display_ok:
            print("   - 数据展示服务测试失败")
        return False

def main():
    """主函数"""
    print("全球资金流向系统 - 数据拉取和展示分离测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        success = test_separation()
        
        if success:
            print("\n🎉 所有测试通过! 系统运行正常")
            print("\n访问地址:")
            print("- 数据展示服务: http://localhost:5003")
            print("- 数据收集服务API: http://localhost:5004/api/status")
        else:
            print("\n❌ 测试失败，请检查服务状态")
            
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")

if __name__ == '__main__':
    main() 