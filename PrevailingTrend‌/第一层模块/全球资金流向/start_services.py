#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球资金流向系统服务启动脚本
管理数据收集和展示两个独立服务
"""

import os
import sys
import time
import subprocess
import threading
from datetime import datetime

def start_data_collector():
    """启动数据收集服务"""
    print("正在启动数据收集服务...")
    try:
        # 启动数据收集服务 (端口5004)
        subprocess.run([
            sys.executable, 
            "data_collector_service.py"
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
    except Exception as e:
        print(f"数据收集服务启动失败: {e}")

def start_display_service():
    """启动数据展示服务"""
    print("正在启动数据展示服务...")
    try:
        # 启动数据展示服务 (端口5003)
        subprocess.run([
            sys.executable, 
            "display_service.py"
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
    except Exception as e:
        print(f"数据展示服务启动失败: {e}")

def main():
    """主函数"""
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
                start_data_collector()
                break
                
            elif choice == '2':
                print("\n启动数据展示服务...")
                start_display_service()
                break
                
            elif choice == '3':
                print("\n启动两个服务...")
                print("注意: 两个服务将在不同的终端窗口中运行")
                
                # 使用线程启动两个服务
                collector_thread = threading.Thread(target=start_data_collector)
                display_thread = threading.Thread(target=start_display_service)
                
                collector_thread.start()
                time.sleep(2)  # 等待2秒
                display_thread.start()
                
                print("\n服务启动完成!")
                print("- 数据收集服务: http://localhost:5004")
                print("- 数据展示服务: http://localhost:5003")
                print("\n按 Ctrl+C 停止服务")
                
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n正在停止服务...")
                    break
                    
            elif choice == '4':
                print("退出程序")
                break
                
            else:
                print("无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n程序已停止")
            break
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == '__main__':
    main() 