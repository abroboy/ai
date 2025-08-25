"""
第一层模块快速访问脚本
提供快速访问各个模块功能的入口
"""

import webbrowser
import time
import sys
import os

def open_management_console():
    """打开管理台"""
    print("正在打开管理台...")
    webbrowser.open('http://localhost:8080')
    print("✅ 管理台已打开")

def open_api_docs():
    """打开API文档"""
    print("正在打开API文档...")
    webbrowser.open('http://localhost:5000')
    print("✅ API文档已打开")

def show_status():
    """显示服务状态"""
    print("\n第一层模块服务状态:")
    print("=" * 40)
    print("管理台: http://localhost:8080")
    print("万得行业分类API: http://localhost:5000")
    print("=" * 40)

def main():
    """主函数"""
    print("第一层模块快速访问")
    print("=" * 30)
    print("1. 打开管理台")
    print("2. 打开API文档")
    print("3. 显示服务状态")
    print("4. 退出")
    print("=" * 30)
    
    while True:
        try:
            choice = input("请选择操作 (1-4): ").strip()
            
            if choice == '1':
                open_management_console()
            elif choice == '2':
                open_api_docs()
            elif choice == '3':
                show_status()
            elif choice == '4':
                print("再见！")
                break
            else:
                print("无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"操作失败: {e}")

if __name__ == "__main__":
    main() 