#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多端口服务测试脚本
测试各模块是否在正确的端口运行
"""

import requests
import time
import sys
from datetime import datetime

def test_service(service_name, port, endpoints):
    """测试单个服务"""
    print(f"\n🔍 测试 {service_name} (端口: {port})")
    print("-" * 50)
    
    success_count = 0
    total_count = len(endpoints)
    
    for endpoint, description in endpoints.items():
        try:
            url = f"http://localhost:{port}{endpoint}"
            print(f"  测试 {description}: {url}")
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"  ✅ 成功 (状态码: {response.status_code})")
                success_count += 1
            else:
                print(f"  ❌ 失败 (状态码: {response.status_code})")
                
        except requests.exceptions.ConnectionError:
            print(f"  ❌ 连接失败 (服务可能未启动)")
        except requests.exceptions.Timeout:
            print(f"  ❌ 请求超时")
        except Exception as e:
            print(f"  ❌ 错误: {e}")
    
    print(f"\n📊 {service_name} 测试结果: {success_count}/{total_count} 成功")
    return success_count == total_count

def main():
    """主测试函数"""
    print("=" * 60)
    print("🚀 多端口服务测试")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 定义各服务的测试端点
    services = {
        '万得行业分类': {
            'port': 5001,
            'endpoints': {
                '/': '首页',
                '/dashboard': '仪表盘',
                '/api/health': '健康检查'
            }
        },
        '国内热点数据': {
            'port': 5002,
            'endpoints': {
                '/': '首页',
                '/dashboard': '仪表盘',
                '/api/hotspots': '热点数据API'
            }
        },
        '全球资金流向': {
            'port': 5003,
            'endpoints': {
                '/': '首页',
                '/dashboard': '仪表盘',
                '/api/health': '健康检查',
                '/api/dashboard_data': '仪表盘数据API'
            }
        }
    }
    
    # 测试所有服务
    results = {}
    total_success = 0
    
    for service_name, config in services.items():
        success = test_service(
            service_name, 
            config['port'], 
            config['endpoints']
        )
        results[service_name] = success
        if success:
            total_success += 1
    
    # 显示测试总结
    print("\n" + "=" * 60)
    print("📋 测试总结")
    print("=" * 60)
    
    for service_name, success in results.items():
        status = "✅ 正常" if success else "❌ 异常"
        port = services[service_name]['port']
        print(f"{service_name} (端口: {port}): {status}")
    
    print(f"\n总体结果: {total_success}/{len(services)} 个服务正常")
    
    if total_success == len(services):
        print("\n🎉 所有服务运行正常！")
        print("\n📱 访问地址:")
        for service_name, config in services.items():
            print(f"   {service_name}: http://localhost:{config['port']}")
    else:
        print("\n⚠️ 部分服务异常，请检查服务状态")
        
        # 提供启动建议
        print("\n💡 启动建议:")
        print("   1. 运行 python quick_start.py 启动所有服务")
        print("   2. 或手动启动各模块:")
        for service_name, config in services.items():
            if not results[service_name]:
                print(f"      - {service_name}: cd {service_name} && python app.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 测试已中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}") 