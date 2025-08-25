#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球资金流向系统服务管理器
管理数据收集和展示两个独立服务
"""

import os
import sys
import time
import subprocess
import threading
import requests
import signal
from datetime import datetime

class ServiceManager:
    def __init__(self):
        self.collector_process = None
        self.display_process = None
        self.services_running = False
        
    def check_service_health(self, url, service_name):
        """检查服务健康状态"""
        try:
            response = requests.get(f"{url}/api/health", timeout=5)
            if response.status_code == 200:
                return True, "运行正常"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "连接失败"
        except requests.exceptions.Timeout:
            return False, "请求超时"
        except Exception as e:
            return False, f"错误: {str(e)}"
    
    def start_data_collector(self):
        """启动数据收集服务"""
        print("正在启动数据收集服务...")
        try:
            # 启动数据收集服务 (端口5004)
            self.collector_process = subprocess.Popen([
                sys.executable, 
                "simple_data_collector.py"
            ], cwd=os.path.dirname(os.path.abspath(__file__)))
            
            # 等待服务启动
            time.sleep(3)
            
            # 检查服务状态
            is_healthy, status = self.check_service_health("http://localhost:5004", "数据收集服务")
            if is_healthy:
                print("✅ 数据收集服务启动成功")
                return True
            else:
                print(f"❌ 数据收集服务启动失败: {status}")
                return False
                
        except Exception as e:
            print(f"❌ 数据收集服务启动失败: {e}")
            return False

    def start_display_service(self):
        """启动数据展示服务"""
        print("正在启动数据展示服务...")
        try:
            # 启动数据展示服务 (端口5003)
            self.display_process = subprocess.Popen([
                sys.executable, 
                "display_service.py"
            ], cwd=os.path.dirname(os.path.abspath(__file__)))
            
            # 等待服务启动
            time.sleep(3)
            
            # 检查服务状态
            is_healthy, status = self.check_service_health("http://localhost:5003", "数据展示服务")
            if is_healthy:
                print("✅ 数据展示服务启动成功")
                return True
            else:
                print(f"❌ 数据展示服务启动失败: {status}")
                return False
                
        except Exception as e:
            print(f"❌ 数据展示服务启动失败: {e}")
            return False
    
    def stop_services(self):
        """停止所有服务"""
        print("\n正在停止服务...")
        
        if self.collector_process:
            try:
                self.collector_process.terminate()
                self.collector_process.wait(timeout=5)
                print("✅ 数据收集服务已停止")
            except subprocess.TimeoutExpired:
                self.collector_process.kill()
                print("⚠️  强制停止数据收集服务")
            except Exception as e:
                print(f"❌ 停止数据收集服务时出错: {e}")
        
        if self.display_process:
            try:
                self.display_process.terminate()
                self.display_process.wait(timeout=5)
                print("✅ 数据展示服务已停止")
            except subprocess.TimeoutExpired:
                self.display_process.kill()
                print("⚠️  强制停止数据展示服务")
            except Exception as e:
                print(f"❌ 停止数据展示服务时出错: {e}")
        
        self.services_running = False
    
    def monitor_services(self):
        """监控服务状态"""
        while self.services_running:
            try:
                print("\n" + "="*60)
                print("服务状态监控")
                print("="*60)
                
                # 检查数据收集服务
                collector_healthy, collector_status = self.check_service_health("http://localhost:5004", "数据收集服务")
                print(f"数据收集服务: {'✅' if collector_healthy else '❌'} {collector_status}")
                
                # 检查数据展示服务
                display_healthy, display_status = self.check_service_health("http://localhost:5003", "数据展示服务")
                print(f"数据展示服务: {'✅' if display_healthy else '❌'} {display_status}")
                
                print(f"\n访问地址:")
                print(f"- 数据展示服务: http://localhost:5003")
                print(f"- 数据收集服务API: http://localhost:5004/api/status")
                print(f"\n按 Ctrl+C 停止所有服务")
                
                time.sleep(30)  # 每30秒检查一次
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"监控过程中出错: {e}")
                time.sleep(10)
    
    def signal_handler(self, signum, frame):
        """信号处理器"""
        print(f"\n收到信号 {signum}，正在停止服务...")
        self.stop_services()
        sys.exit(0)

def main():
    """主函数"""
    manager = ServiceManager()
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, manager.signal_handler)
    signal.signal(signal.SIGTERM, manager.signal_handler)
    
    print("=" * 60)
    print("全球资金流向系统 - 服务管理器")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("服务配置:")
    print("- 数据收集服务: http://localhost:5004")
    print("- 数据展示服务: http://localhost:5003")
    print()
    print("选择启动模式:")
    print("1. 启动数据收集服务")
    print("2. 启动数据展示服务")
    print("3. 启动两个服务")
    print("4. 退出")
    print("=" * 60)
    
    while True:
        try:
            choice = input("请选择 (1-4): ").strip()
            
            if choice == '1':
                print("\n启动数据收集服务...")
                if manager.start_data_collector():
                    print("\n数据收集服务已启动!")
                    print("访问地址: http://localhost:5004/api/status")
                    print("\n按 Ctrl+C 停止服务")
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        manager.stop_services()
                break
                
            elif choice == '2':
                print("\n启动数据展示服务...")
                if manager.start_display_service():
                    print("\n数据展示服务已启动!")
                    print("访问地址: http://localhost:5003")
                    print("\n按 Ctrl+C 停止服务")
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        manager.stop_services()
                break
                
            elif choice == '3':
                print("\n启动两个服务...")
                print("注意: 两个服务将在不同的进程中运行")
                
                # 启动数据收集服务
                if not manager.start_data_collector():
                    print("❌ 数据收集服务启动失败，退出")
                    break
                
                # 启动数据展示服务
                if not manager.start_display_service():
                    print("❌ 数据展示服务启动失败，停止数据收集服务")
                    manager.stop_services()
                    break
                
                print("\n✅ 所有服务启动完成!")
                manager.services_running = True
                
                # 开始监控服务
                manager.monitor_services()
                break
                    
            elif choice == '4':
                print("退出程序")
                break
                
            else:
                print("无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n程序已停止")
            manager.stop_services()
            break
        except Exception as e:
            print(f"发生错误: {e}")
            manager.stop_services()

if __name__ == '__main__':
    main() 