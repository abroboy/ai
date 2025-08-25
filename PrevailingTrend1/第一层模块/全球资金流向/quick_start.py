#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球资金流向分析系统快速启动脚本
"""

import os
import sys
import subprocess
from datetime import datetime

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    return True

def install_requirements():
    """安装依赖包"""
    print("正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 依赖包安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 依赖包安装失败: {e}")
        return False

def create_directories():
    """创建必要目录"""
    directories = [
        'logs',
        'static/charts',
        'static/reports',
        'data'
    ]
    
    print("正在创建目录...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ 创建目录: {directory}")

def setup_environment():
    """设置环境"""
    print("正在设置环境...")
    
    # 检查是否存在.env文件
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            import shutil
            shutil.copy('env.example', '.env')
            print("✓ 已创建.env文件，请编辑配置信息")
        else:
            print("⚠️  未找到env.example文件")
    
    print("✓ 环境设置完成")

def run_tests():
    """运行测试"""
    print("正在运行系统测试...")
    try:
        subprocess.check_call([sys.executable, "test_system.py"])
        return True
    except subprocess.CalledProcessError:
        print("⚠️  系统测试失败，但可以继续启动")
        return False

def start_system():
    """启动系统"""
    print("正在启动系统...")
    try:
        subprocess.check_call([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n系统已停止")
    except Exception as e:
        print(f"启动失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("全球资金流向分析系统 - 快速启动")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装依赖
    if not install_requirements():
        print("请手动安装依赖包: pip install -r requirements.txt")
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    # 设置环境
    setup_environment()
    
    # 运行测试
    run_tests()
    
    print()
    print("=" * 60)
    print("快速启动完成！")
    print("=" * 60)
    print("下一步操作:")
    print("1. 编辑 .env 文件，配置数据库连接信息")
    print("2. 确保MySQL数据库已启动")
    print("3. 运行 python start.py 启动系统")
    print("4. 访问 http://localhost:5003 查看Web界面")
    print()
    
    # 询问是否立即启动
    response = input("是否立即启动系统？(y/n): ").lower().strip()
    if response in ['y', 'yes', '是']:
        start_system()

if __name__ == '__main__':
    main() 