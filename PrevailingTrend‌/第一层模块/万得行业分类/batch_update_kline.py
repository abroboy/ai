#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新K线数据脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from get_kline_data import KlineDataCollector
import logging

def main():
    """主函数"""
    print("=" * 60)
    print("🔄 批量更新K线数据")
    print("=" * 60)
    
    collector = KlineDataCollector()
    
    # 获取用户输入
    try:
        limit = input("请输入要更新的股票数量 (默认50): ").strip()
        limit = int(limit) if limit else 50
        
        confirm = input(f"确认要更新 {limit} 只股票的K线数据吗? (y/N): ").strip().lower()
        if confirm != 'y':
            print("操作已取消")
            return
            
    except KeyboardInterrupt:
        print("\n操作已取消")
        return
    except ValueError:
        print("输入无效，使用默认值50")
        limit = 50
    
    print(f"\n开始批量更新 {limit} 只股票的K线数据...")
    
    # 执行批量更新
    result = collector.batch_update_kline_data(limit)
    
    # 显示结果
    print("\n" + "=" * 60)
    print("📊 更新结果统计")
    print("=" * 60)
    print(f"总数量: {result['total']}")
    print(f"成功: {result['success_count']}")
    print(f"失败: {result['failed_count']}")
    print(f"成功率: {result['success_count']/result['total']*100:.1f}%")
    
    if result['failed_stocks']:
        print(f"\n❌ 失败的股票:")
        for stock in result['failed_stocks'][:10]:  # 只显示前10个
            print(f"  - {stock}")
        if len(result['failed_stocks']) > 10:
            print(f"  ... 还有 {len(result['failed_stocks']) - 10} 只")
    
    print("\n✅ 批量更新完成!")

if __name__ == "__main__":
    main() 