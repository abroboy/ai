#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AKShare功能
"""

import akshare as ak
import pandas as pd

def test_akshare():
    """测试AKShare基本功能"""
    print("=" * 60)
    print("🧪 测试AKShare功能")
    print("=" * 60)
    
    # 测试A股数据
    print("\n1. 测试A股数据获取...")
    try:
        # 测试平安银行
        stock_data = ak.stock_zh_a_hist(symbol="000001", period="daily", 
                                       start_date="20240801", end_date="20240824", 
                                       adjust="qfq")
        print(f"✅ 平安银行数据获取成功，共 {len(stock_data)} 条记录")
        print(f"数据列: {list(stock_data.columns)}")
        print(f"前3行数据:")
        print(stock_data.head(3))
    except Exception as e:
        print(f"❌ 平安银行数据获取失败: {e}")
    
    # 测试港股数据
    print("\n2. 测试港股数据获取...")
    try:
        # 测试腾讯控股
        hk_data = ak.stock_hk_hist(symbol="00700", period="daily", 
                                  start_date="20240801", end_date="20240824", 
                                  adjust="qfq")
        print(f"✅ 腾讯控股数据获取成功，共 {len(hk_data)} 条记录")
        print(f"数据列: {list(hk_data.columns)}")
        print(f"前3行数据:")
        print(hk_data.head(3))
    except Exception as e:
        print(f"❌ 腾讯控股数据获取失败: {e}")
    
    # 测试其他接口
    print("\n3. 测试其他数据接口...")
    try:
        # 测试股票基本信息
        stock_info = ak.stock_info_a_code_name()
        print(f"✅ A股股票列表获取成功，共 {len(stock_info)} 只股票")
    except Exception as e:
        print(f"❌ A股股票列表获取失败: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_akshare() 