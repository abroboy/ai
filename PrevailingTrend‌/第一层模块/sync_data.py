#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据同步脚本
定期同步各个模块的数据，确保数据一致性
"""
import requests
import time
import schedule
from datetime import datetime

def sync_wind_data():
    """同步万得行业分类数据"""
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 同步万得行业分类数据...")
        
        # 刷新统计数据
        response = requests.get('http://localhost:5001/api/stats', timeout=5)
        if response.status_code == 200:
            print("  ✅ 统计数据已同步")
        else:
            print(f"  ❌ 统计数据同步失败: {response.status_code}")
        
        # 刷新行业列表
        response = requests.get('http://localhost:5001/api/industries?page=1&page_size=10', timeout=5)
        if response.status_code == 200:
            print("  ✅ 行业列表已同步")
        else:
            print(f"  ❌ 行业列表同步失败: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ 万得数据同步错误: {e}")

def sync_hotspot_data():
    """同步国内热点数据"""
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 同步国内热点数据...")
        
        # 刷新热点数据
        response = requests.get('http://localhost:5002/api/hotspots', timeout=5)
        if response.status_code == 200:
            print("  ✅ 热点数据已同步")
        else:
            print(f"  ❌ 热点数据同步失败: {response.status_code}")
        
        # 刷新统计数据
        response = requests.get('http://localhost:5002/api/statistics', timeout=5)
        if response.status_code == 200:
            print("  ✅ 统计数据已同步")
        else:
            print(f"  ❌ 统计数据同步失败: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ 热点数据同步错误: {e}")

def sync_flow_data():
    """同步全球资金流向数据"""
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 同步全球资金流向数据...")
        
        # 刷新仪表盘数据
        response = requests.get('http://localhost:5003/api/dashboard_data', timeout=5)
        if response.status_code == 200:
            print("  ✅ 仪表盘数据已同步")
        else:
            print(f"  ❌ 仪表盘数据同步失败: {response.status_code}")
        
        # 刷新流向分析数据
        response = requests.get('http://localhost:5003/api/flow_analysis', timeout=5)
        if response.status_code == 200:
            print("  ✅ 流向分析数据已同步")
        else:
            print(f"  ❌ 流向分析数据同步失败: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ 资金流向数据同步错误: {e}")

def sync_all_data():
    """同步所有模块数据"""
    print("\n" + "=" * 50)
    print(f"🔄 开始数据同步 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    sync_wind_data()
    time.sleep(1)
    
    sync_hotspot_data()
    time.sleep(1)
    
    sync_flow_data()
    
    print("=" * 50)
    print("✅ 数据同步完成")
    print("=" * 50)

def start_scheduled_sync():
    """启动定时同步"""
    print("🕐 启动定时数据同步...")
    print("📅 同步计划:")
    print("   - 每5分钟同步一次")
    print("   - 按 Ctrl+C 停止")
    
    # 立即执行一次同步
    sync_all_data()
    
    # 设置定时任务
    schedule.every(5).minutes.do(sync_all_data)
    
    # 运行定时任务
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 定时同步已停止")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "sync":
            # 执行一次同步
            sync_all_data()
        elif command == "start":
            # 启动定时同步
            start_scheduled_sync()
        elif command == "help":
            print("""
数据同步脚本使用说明:

用法: python sync_data.py [命令]

命令:
  sync   - 执行一次数据同步
  start  - 启动定时同步（每5分钟）
  help   - 显示此帮助信息

示例:
  python sync_data.py sync   # 执行一次同步
  python sync_data.py start  # 启动定时同步
            """)
        else:
            print(f"❌ 未知命令: {command}")
            print("使用 'python sync_data.py help' 查看帮助")
    else:
        # 默认执行一次同步
        sync_all_data() 