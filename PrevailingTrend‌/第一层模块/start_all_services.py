"""
第一层模块服务启动脚本
同时启动管理台和各个模块的API服务
"""

import subprocess
import time
import sys
import os
from datetime import datetime

def start_service(name, command, port, description):
    """启动服务"""
    print(f"启动 {name} 服务...")
    print(f"  描述: {description}")
    print(f"  端口: {port}")
    print(f"  命令: {command}")
    
    try:
        # 启动服务
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待服务启动
        time.sleep(3)
        
        # 检查服务是否启动成功
        if process.poll() is None:
            print(f"✅ {name} 服务启动成功")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ {name} 服务启动失败")
            print(f"  错误: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ {name} 服务启动异常: {e}")
        return None

def main():
    """主函数"""
    print("=" * 60)
    print("第一层模块服务启动器")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 切换到第一层模块目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    services = [
        {
            'name': '管理台',
            'command': 'cd 管理台 && python app.py',
            'port': 8080,
            'description': 'Web管理界面，提供模块管理和监控功能'
        },
        {
            'name': '万得行业分类API',
            'command': 'cd 万得行业分类 && python demo_server.py',
            'port': 5000,
            'description': '行业分类数据API服务'
        }
    ]
    
    processes = []
    
    # 启动所有服务
    for service in services:
        process = start_service(
            service['name'],
            service['command'],
            service['port'],
            service['description']
        )
        if process:
            processes.append((service['name'], process))
        print()
    
    # 显示服务状态
    print("=" * 60)
    print("服务状态汇总")
    print("=" * 60)
    
    for name, process in processes:
        if process.poll() is None:
            print(f"✅ {name}: 运行中")
        else:
            print(f"❌ {name}: 已停止")
    
    print()
    print("访问地址:")
    print("  管理台: http://localhost:8080")
    print("  万得行业分类API: http://localhost:5000")
    print()
    print("按 Ctrl+C 停止所有服务")
    
    try:
        # 保持运行
        while True:
            time.sleep(1)
            
            # 检查服务状态
            for name, process in processes:
                if process.poll() is not None:
                    print(f"⚠️  {name} 服务已停止")
                    
    except KeyboardInterrupt:
        print("\n正在停止所有服务...")
        
        # 停止所有服务
        for name, process in processes:
            if process.poll() is None:
                process.terminate()
                print(f"已停止 {name}")
        
        print("所有服务已停止")

if __name__ == "__main__":
    main() 