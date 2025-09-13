#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务状态检查脚本
快速检查各模块服务状态
"""

import requests
import time
from datetime import datetime

def check_service_status():
    """检查所有服务状态"""
    print("=" * 60)
    print("🔍 服务状态检查")
    print("=" * 60)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    services = {
        '万得行业分类': {
            'port': 5001,
            'url': 'http://localhost:5001',
            'endpoints': ['/', '/dashboard', '/api/health']
        },
        '国内热点数据': {
            'port': 5002,
            'url': 'http://localhost:5002',
            'endpoints': ['/', '/dashboard', '/api/hotspots']
        },
        '全球资金流向': {
            'port': 5003,
            'url': 'http://localhost:5003',
            'endpoints': ['/', '/dashboard', '/api/health', '/api/dashboard_data']
        }
    }
    
    all_healthy = True
    
    for service_name, config in services.items():
        print(f"📊 {service_name} (端口: {config['port']})")
        print("-" * 40)
        
        service_healthy = True
        
        for endpoint in config['endpoints']:
            try:
                url = f"{config['url']}{endpoint}"
                response = requests.get(url, timeout=3)
                
                if response.status_code == 200:
                    print(f"  ✅ {endpoint} - 正常")
                else:
                    print(f"  ⚠️  {endpoint} - 异常 (状态码: {response.status_code})")
                    service_healthy = False
                    
            except requests.exceptions.ConnectionError:
                print(f"  ❌ {endpoint} - 连接失败")
                service_healthy = False
            except requests.exceptions.Timeout:
                print(f"  ⏰ {endpoint} - 超时")
                service_healthy = False
            except Exception as e:
                print(f"  ❌ {endpoint} - 错误: {e}")
                service_healthy = False
        
        if service_healthy:
            print(f"  🟢 {service_name} 服务正常")
        else:
            print(f"  🔴 {service_name} 服务异常")
            all_healthy = False
        
        print()
    
    # 总结
    print("=" * 60)
    print("📋 服务状态总结")
    print("=" * 60)
    
    if all_healthy:
        print("🎉 所有服务运行正常！")
        print()
        print("📱 访问地址:")
        for service_name, config in services.items():
            print(f"   {service_name}: {config['url']}")
    else:
        print("⚠️ 部分服务异常，请检查服务状态")
    
    print("=" * 60)

if __name__ == "__main__":
    try:
        check_service_status()
    except KeyboardInterrupt:
        print("\n👋 检查已中断")
    except Exception as e:
        print(f"\n❌ 检查过程中发生错误: {e}") 