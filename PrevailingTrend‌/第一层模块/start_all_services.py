#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版服务启动脚本
启动所有模块服务并集成数据刷新功能
"""
import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from data_refresh_manager import DataRefreshManager

class EnhancedServiceManager:
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
        self.refresh_manager = DataRefreshManager()
        
    def start_service(self, service_name):
        """启动单个服务"""
        if service_name not in self.services:
            print(f"❌ 未知服务: {service_name}")
            return False
            
        service_config = self.services[service_name]
        port = service_config['port']
        path = service_config['path']
        script = service_config['script']
        
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
            time.sleep(3)  # 等待服务启动
            
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
        print("🚀 增强版服务启动器")
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
    
    def start_data_refresh(self):
        """启动数据刷新服务"""
        print("\n🔄 启动数据刷新服务...")
        
        def run_refresh():
            try:
                self.refresh_manager.start_scheduled_refresh()
            except KeyboardInterrupt:
                print("\n🛑 数据刷新服务已停止")
        
        refresh_thread = threading.Thread(target=run_refresh, daemon=True)
        refresh_thread.start()
        print("✅ 数据刷新服务已启动（后台运行）")
        
        return refresh_thread
    
    def stop_all_services(self):
        """停止所有服务"""
        print("\n🛑 停止所有服务...")
        
        # 停止数据刷新
        self.refresh_manager.stop_scheduled_refresh()
        
        # 停止服务进程
        for service_name, process in self.processes.items():
            try:
                process.terminate()
                print(f"🛑 {service_name} 已停止")
            except:
                pass
        self.processes.clear()
    
    def check_services_status(self):
        """检查所有服务状态"""
        print("\n🔍 检查服务状态...")
        self.refresh_manager.get_service_info()
    
    def manual_refresh(self):
        """手动刷新数据"""
        print("\n🔄 手动刷新数据...")
        self.refresh_manager.force_refresh_data()

def main():
    """主函数"""
    manager = EnhancedServiceManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            # 启动所有服务
            success_count = manager.start_all_services()
            
            if success_count > 0:
                # 启动数据刷新
                manager.start_data_refresh()
                
                print("\n💡 提示:")
                print("   - 按 Ctrl+C 停止所有服务")
                print("   - 服务会自动在后台运行")
                print("   - 数据每5分钟自动刷新一次")
                print("   - 可以通过浏览器访问各个模块")
                
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n👋 正在退出...")
                    manager.stop_all_services()
                    print("✅ 所有服务已停止")
                    
        elif command == "refresh":
            # 手动刷新数据
            manager.manual_refresh()
            
        elif command == "status":
            # 检查服务状态
            manager.check_services_status()
            
        elif command == "stop":
            # 停止所有服务
            manager.stop_all_services()
            
        elif command == "help":
            # 显示帮助信息
            print("""
增强版服务启动器使用说明:

用法: python start_all_services.py [命令]

命令:
  start    - 启动所有服务并开始数据刷新
  refresh  - 手动刷新所有数据
  status   - 检查服务状态
  stop     - 停止所有服务
  help     - 显示此帮助信息

示例:
  python start_all_services.py start    # 启动所有服务
  python start_all_services.py refresh  # 手动刷新数据
  python start_all_services.py status   # 检查状态
            """)
        else:
            print(f"❌ 未知命令: {command}")
            print("使用 'python start_all_services.py help' 查看帮助")
    else:
        # 默认启动所有服务
        success_count = manager.start_all_services()
        
        if success_count > 0:
            manager.start_data_refresh()
            
            print("\n💡 提示:")
            print("   - 按 Ctrl+C 停止所有服务")
            print("   - 服务会自动在后台运行")
            print("   - 数据每5分钟自动刷新一次")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 正在退出...")
                manager.stop_all_services()
                print("✅ 所有服务已停止")

if __name__ == "__main__":
    main() 