#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动脚本 - 多模块服务管理器
支持各模块通过不同端口访问：
- 5001: 万得行业分类模块
- 5002: 国内热点数据模块  
- 5003: 全球资金流向模块
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path

class QuickStartManager:
    def __init__(self):
        self.services = {
            '万得行业分类': {
                'port': 5001,
                'path': '第一层模块/万得行业分类',
                'script': 'run_dashboard.py',
                'description': '万得行业分类管理系统'
            },
            '国内热点数据': {
                'port': 5002,
                'path': '第一层模块/国内热点数据',
                'script': 'app.py',
                'description': '国内热点数据监控系统'
            },
            '全球资金流向': {
                'port': 5003,
                'path': '第一层模块/全球资金流向',
                'script': 'display_service.py',
                'description': '全球资金流向分析系统'
            }
        }
        self.processes = {}
        
    def start_service(self, service_name):
        """启动单个服务"""
        if service_name not in self.services:
            print(f"❌ 未知服务: {service_name}")
            return False
            
        service_config = self.services[service_name]
        port = service_config['port']
        path = service_config['path']
        script = service_config['script']
        
        # 构建完整路径
        full_path = Path(__file__).parent / path
        script_path = full_path / script
        
        if not script_path.exists():
            print(f"❌ 脚本文件不存在: {script_path}")
            return False
            
        try:
            print(f"🚀 启动 {service_name} (端口: {port})...")
            process = subprocess.Popen(
                [sys.executable, str(script_path)],
                cwd=str(full_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.processes[service_name] = process
            time.sleep(2)  # 等待服务启动
            
            if process.poll() is None:
                print(f"✅ {service_name} 启动成功")
                print(f"   访问地址: http://localhost:{port}")
                return True
            else:
                print(f"❌ {service_name} 启动失败")
                return False
                
        except Exception as e:
            print(f"❌ 启动 {service_name} 时发生错误: {e}")
            return False
    
    def start_all_services(self):
        """启动所有服务"""
        print("=" * 60)
        print("🚀 快速启动多模块服务")
        print("=" * 60)
        
        success_count = 0
        for service_name in self.services:
            if self.start_service(service_name):
                success_count += 1
            print()
        
        print("=" * 60)
        print("📋 服务访问地址:")
        for service_name, config in self.services.items():
            print(f"   {service_name}: http://localhost:{config['port']}")
        print("=" * 60)
        
        if success_count == len(self.services):
            print("✅ 所有服务启动成功！")
        else:
            print(f"⚠️  {success_count}/{len(self.services)} 个服务启动成功")
        
        return success_count
    
    def stop_all_services(self):
        """停止所有服务"""
        print("\n🛑 停止所有服务...")
        for service_name, process in self.processes.items():
            try:
                process.terminate()
                print(f"🛑 {service_name} 已停止")
            except:
                pass
        self.processes.clear()

def main():
    manager = QuickStartManager()
    
    try:
        manager.start_all_services()
        
        print("\n💡 提示:")
        print("   - 按 Ctrl+C 停止所有服务")
        print("   - 服务会自动在后台运行")
        print("   - 可以通过浏览器访问各个模块")
        
        # 保持程序运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 正在退出...")
        manager.stop_all_services()
        print("✅ 所有服务已停止")

if __name__ == "__main__":
    main() 