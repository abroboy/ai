#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球资金流向模块测试脚本
"""

import requests
import json
import pandas as pd
import os
from pathlib import Path

def test_csv_data():
    """测试CSV数据文件"""
    print("=" * 50)
    print("测试CSV数据文件")
    print("=" * 50)
    
    api_dir = Path('api')
    market_file = api_dir / 'akshare_test_ak_stock_market_fund_flow.csv'
    individual_file = api_dir / 'akshare_test_ak_stock_individual_fund_flow.csv'
    
    # 测试市场数据文件
    if market_file.exists():
        try:
            df = pd.read_csv(market_file, encoding='utf-8-sig')
            print(f"✓ 市场数据文件加载成功")
            print(f"  - 文件路径: {market_file}")
            print(f"  - 数据行数: {len(df)}")
            print(f"  - 数据列数: {len(df.columns)}")
            print(f"  - 日期范围: {df['日期'].iloc[0]} 到 {df['日期'].iloc[-1]}")
        except Exception as e:
            print(f"✗ 市场数据文件加载失败: {e}")
    else:
        print(f"✗ 市场数据文件不存在: {market_file}")
    
    # 测试个股数据文件
    if individual_file.exists():
        try:
            df = pd.read_csv(individual_file, encoding='utf-8-sig')
            print(f"✓ 个股数据文件加载成功")
            print(f"  - 文件路径: {individual_file}")
            print(f"  - 数据行数: {len(df)}")
            print(f"  - 数据列数: {len(df.columns)}")
            print(f"  - 日期范围: {df['日期'].iloc[0]} 到 {df['日期'].iloc[-1]}")
        except Exception as e:
            print(f"✗ 个股数据文件加载失败: {e}")
    else:
        print(f"✗ 个股数据文件不存在: {individual_file}")

def test_api_server():
    """测试API服务器"""
    print("\n" + "=" * 50)
    print("测试API服务器")
    print("=" * 50)
    
    base_url = "http://localhost:5001"
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/api/global_capital_flow/health", timeout=5)
        if response.status_code == 200:
            print("✓ API服务器运行正常")
            data = response.json()
            print(f"  - 响应: {data['message']}")
        else:
            print(f"✗ API服务器响应异常: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到API服务器")
        print("  请先运行: python start_api_server.py")
        return False
    except Exception as e:
        print(f"✗ API测试失败: {e}")
        return False
    
    # 测试市场数据接口
    try:
        response = requests.get(f"{base_url}/api/global_capital_flow/market_data?days=5", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✓ 市场数据接口正常")
                print(f"  - 返回数据条数: {len(data['data'])}")
                if data['data']:
                    latest = data['data'][-1]
                    print(f"  - 最新日期: {latest['date']}")
                    print(f"  - 主力净流入: {latest['main_net_inflow']:,.0f}")
            else:
                print(f"✗ 市场数据接口返回错误: {data['message']}")
        else:
            print(f"✗ 市场数据接口响应异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 市场数据接口测试失败: {e}")
    
    # 测试汇总数据接口
    try:
        response = requests.get(f"{base_url}/api/global_capital_flow/summary", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✓ 汇总数据接口正常")
                summary = data['data']
                print(f"  - 最新日期: {summary['latest_date']}")
                print(f"  - 上证指数: {summary['shanghai_index']['close']:.2f}")
                print(f"  - 深证指数: {summary['shenzhen_index']['close']:.2f}")
            else:
                print(f"✗ 汇总数据接口返回错误: {data['message']}")
        else:
            print(f"✗ 汇总数据接口响应异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 汇总数据接口测试失败: {e}")
    
    return True

def test_frontend_files():
    """测试前端文件"""
    print("\n" + "=" * 50)
    print("测试前端文件")
    print("=" * 50)
    
    files_to_check = [
        ('管理台/index.html', '主页面'),
        ('static/js/global_capital_flow.js', 'JavaScript模块'),
        ('static/css/style.css', '基础样式'),
        ('static/css/global_capital_flow.css', '模块样式')
    ]
    
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✓ {description}存在")
            print(f"  - 文件路径: {file_path}")
            print(f"  - 文件大小: {file_size:,} 字节")
        else:
            print(f"✗ {description}不存在: {file_path}")

def generate_test_report():
    """生成测试报告"""
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    print("全球资金流向模块测试完成！")
    print("\n如果所有测试都通过，您可以:")
    print("1. 启动API服务器: python start_api_server.py")
    print("2. 打开浏览器访问: 管理台/index.html")
    print("3. 点击'全球资金流向'模块开始使用")
    
    print("\n如果遇到问题，请检查:")
    print("- Python依赖包是否安装: pip install flask flask-cors pandas requests")
    print("- CSV数据文件是否存在且格式正确")
    print("- 端口5001是否被占用")
    print("- 浏览器控制台是否有错误信息")

def main():
    """主函数"""
    print("全球资金流向模块测试")
    print("测试时间:", pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # 测试CSV数据
    test_csv_data()
    
    # 测试前端文件
    test_frontend_files()
    
    # 测试API服务器
    test_api_server()
    
    # 生成测试报告
    generate_test_report()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()