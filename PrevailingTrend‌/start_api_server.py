#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动全球资金流向API服务器
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """检查依赖包"""
    required_packages = ['flask', 'flask-cors', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("缺少以下依赖包:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n请运行以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def start_api_server():
    """启动API服务器"""
    if not check_dependencies():
        return False
    
    # 获取当前脚本目录
    current_dir = Path(__file__).parent
    api_dir = current_dir / 'api'
    api_script = api_dir / 'global_capital_flow_api.py'
    
    if not api_script.exists():
        print(f"API脚本不存在: {api_script}")
        return False
    
    print("正在启动全球资金流向API服务器...")
    print(f"API脚本路径: {api_script}")
    print("服务地址: http://localhost:5001")
    print("按 Ctrl+C 停止服务")
    print("-" * 50)
    
    try:
        # 切换到API目录并启动服务
        os.chdir(api_dir)
        subprocess.run([sys.executable, 'global_capital_flow_api.py'], check=True)
    except KeyboardInterrupt:
        print("\n服务已停止")
        return True
    except subprocess.CalledProcessError as e:
        print(f"启动API服务失败: {e}")
        return False
    except Exception as e:
        print(f"启动服务时发生错误: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("全球资金流向API服务器启动器")
    print("=" * 60)
    
    success = start_api_server()
    
    if not success:
        print("\n启动失败，请检查错误信息")
        sys.exit(1)