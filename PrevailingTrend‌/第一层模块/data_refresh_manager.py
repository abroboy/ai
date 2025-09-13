#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据刷新管理器
统一管理各个模块的数据刷新和同步
"""
import os
import sys
import time
import requests
import threading
import schedule
from datetime import datetime
from pathlib import Path

class DataRefreshManager:
    def __init__(self):
        self.services = {
            '万得行业分类': {
                'port': 5001,
                'url': 'http://localhost:5001',
                'refresh_endpoints': [
                    '/api/stats',
                    '/api/industries?page=1&page_size=10'
                ],
                'description': '万得行业分类数据'
            },
            '国内热点数据': {
                'port': 5002,
                'url': 'http://localhost:5002',
                'refresh_endpoints': [
                    '/api/hotspots',
                    '/api/statistics'
                ],
                'description': '国内热点数据'
            },
            '全球资金流向': {
                'port': 5003,
                'url': 'http://localhost:5003',
                'refresh_endpoints': [
                    '/api/dashboard_data',
                    '/api/flow_analysis'
                ],
                'description': '全球资金流向数据'
            }
        }
        self.refresh_interval = 5 * 60  # 5分钟刷新一次
        self.is_running = False
        
    def check_service_status(self, service_name):
        """检查服务状态"""
        service_config = self.services[service_name]
        try:
            response = requests.get(f"{service_config['url']}/api/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def refresh_service_data(self, service_name):
        """刷新单个服务的数据"""
        service_config = self.services[service_name]
        
        if not self.check_service_status(service_name):
            print(f"⚠️  {service_name} 服务未运行，跳过刷新")
            return False
            
        print(f"🔄 开始刷新 {service_name} 数据...")
        success_count = 0
        
        for endpoint in service_config['refresh_endpoints']:
            try:
                url = f"{service_config['url']}{endpoint}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    print(f"  ✅ {endpoint} - 刷新成功")
                    success_count += 1
                else:
                    print(f"  ❌ {endpoint} - 刷新失败 (状态码: {response.status_code})")
                    
            except requests.exceptions.Timeout:
                print(f"  ⏰ {endpoint} - 请求超时")
            except requests.exceptions.ConnectionError:
                print(f"  🔌 {endpoint} - 连接失败")
            except Exception as e:
                print(f"  ❌ {endpoint} - 错误: {e}")
        
        if success_count == len(service_config['refresh_endpoints']):
            print(f"✅ {service_name} 数据刷新完成")
            return True
        else:
            print(f"⚠️  {service_name} 数据刷新部分失败 ({success_count}/{len(service_config['refresh_endpoints'])})")
            return False
    
    def refresh_all_data(self):
        """刷新所有服务的数据"""
        print("\n" + "=" * 60)
        print(f"🔄 开始数据刷新 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        results = {}
        for service_name in self.services:
            results[service_name] = self.refresh_service_data(service_name)
            time.sleep(1)  # 避免请求过于频繁
        
        print("\n" + "=" * 60)
        print("📊 数据刷新总结")
        print("=" * 60)
        
        success_count = 0
        for service_name, success in results.items():
            status = "✅ 成功" if success else "❌ 失败"
            print(f"{service_name}: {status}")
            if success:
                success_count += 1
        
        print(f"\n总体结果: {success_count}/{len(self.services)} 个服务刷新成功")
        print("=" * 60)
        
        return results
    
    def force_refresh_data(self):
        """强制刷新数据（手动触发）"""
        print("🚀 强制刷新所有数据...")
        return self.refresh_all_data()
    
    def start_scheduled_refresh(self):
        """启动定时刷新"""
        if self.is_running:
            print("⚠️  定时刷新已在运行中")
            return
        
        self.is_running = True
        print(f"🕐 启动定时数据刷新，间隔: {self.refresh_interval} 秒")
        
        # 立即执行一次刷新
        self.refresh_all_data()
        
        # 设置定时任务
        schedule.every(self.refresh_interval).seconds.do(self.refresh_all_data)
        
        # 运行定时任务
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
    
    def stop_scheduled_refresh(self):
        """停止定时刷新"""
        self.is_running = False
        print("🛑 定时数据刷新已停止")
    
    def get_service_info(self):
        """获取服务信息"""
        print("\n" + "=" * 60)
        print("📋 服务信息")
        print("=" * 60)
        
        for service_name, config in self.services.items():
            status = "🟢 运行中" if self.check_service_status(service_name) else "🔴 未运行"
            print(f"{service_name} (端口: {config['port']}): {status}")
            print(f"  访问地址: {config['url']}")
            print(f"  刷新端点: {', '.join(config['refresh_endpoints'])}")
            print()

def main():
    """主函数"""
    manager = DataRefreshManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "refresh":
            # 手动刷新
            manager.force_refresh_data()
            
        elif command == "start":
            # 启动定时刷新
            try:
                manager.start_scheduled_refresh()
            except KeyboardInterrupt:
                print("\n👋 正在停止定时刷新...")
                manager.stop_scheduled_refresh()
                
        elif command == "status":
            # 查看服务状态
            manager.get_service_info()
            
        elif command == "help":
            # 显示帮助信息
            print("""
数据刷新管理器使用说明:

用法: python data_refresh_manager.py [命令]

命令:
  refresh   - 手动刷新所有数据
  start     - 启动定时刷新（每5分钟刷新一次）
  status    - 查看服务状态
  help      - 显示此帮助信息

示例:
  python data_refresh_manager.py refresh  # 手动刷新
  python data_refresh_manager.py start    # 启动定时刷新
  python data_refresh_manager.py status   # 查看状态
            """)
        else:
            print(f"❌ 未知命令: {command}")
            print("使用 'python data_refresh_manager.py help' 查看帮助")
    else:
        # 默认执行一次刷新
        manager.force_refresh_data()

if __name__ == "__main__":
    main() 