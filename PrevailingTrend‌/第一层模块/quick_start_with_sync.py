#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动脚本 - 集成数据同步
一键启动所有服务和数据同步功能
"""
import os
import sys
import time
import subprocess
import threading
from pathlib import Path

class QuickStartWithSync:
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
        print("🚀 快速启动所有服务")
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
    
    def start_data_sync(self):
        """启动数据同步"""
        print("\n🔄 启动数据同步服务...")
        
        def run_sync():
            try:
                # 导入并运行数据同步
                sys.path.append(str(Path(__file__).parent))
                from sync_data import start_scheduled_sync
                start_scheduled_sync()
            except KeyboardInterrupt:
                print("\n🛑 数据同步服务已停止")
            except Exception as e:
                print(f"❌ 数据同步服务错误: {e}")
        
        sync_thread = threading.Thread(target=run_sync, daemon=True)
        sync_thread.start()
        print("✅ 数据同步服务已启动（后台运行）")
        
        return sync_thread
    
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
    
    def run(self):
        """运行主程序"""
        try:
            # 启动所有服务
            success_count = self.start_all_services()
            
            if success_count > 0:
                # 启动数据同步
                self.start_data_sync()
                
                print("\n💡 系统已启动完成！")
                print("📊 功能说明:")
                print("   - 所有服务已启动并运行在后台")
                print("   - 数据每5分钟自动同步一次")
                print("   - 可以通过浏览器访问各个模块")
                print("\n🔗 访问地址:")
                for service_name, config in self.services.items():
                    print(f"   {service_name}: http://localhost:{config['port']}")
                
                print("\n💡 操作提示:")
                print("   - 按 Ctrl+C 停止所有服务")
                print("   - 数据会自动保持同步")
                print("   - 如需手动同步，运行: python 第一层模块/sync_data.py sync")
                
                # 等待用户中断
                while True:
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n👋 正在退出...")
            self.stop_all_services()
            print("✅ 所有服务已停止")

def main():
    """主函数"""
    print("🚀 快速启动器 - 集成数据同步")
    print("=" * 60)
    
    starter = QuickStartWithSync()
    starter.run()

if __name__ == "__main__":
    main() 