# -*- coding: utf-8 -*-
"""
AKShare 数据获取与持久化模块
- 先从 AKShare 获取数据并保存到文件
- 后续从文件读取数据
"""

from __future__ import annotations
from typing import List, Dict, Any
import json
import os
from datetime import datetime

def save_akshare_data_to_file() -> bool:
    """从AKShare获取数据并保存到文件"""
    try:
        import akshare as ak
        import pandas as pd
        print("正在从AKShare获取股票数据...")
        df = ak.stock_zh_a_spot_em()
        
        if df is None or df.empty:
            print("AKShare返回空数据")
            return False
            
        print(f"成功获取{len(df)}条股票数据")
        
        # 保存原始数据结构到txt文件
        with open("akshare_stock_structure.txt", "w", encoding="utf-8") as f:
            f.write(f"数据获取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"数据形状: {df.shape}\n")
            f.write(f"列名: {list(df.columns)}\n")
            f.write(f"前5行数据:\n{df.head(5).to_string()}\n")
        
        # 转换为JSON格式并保存
        def safe_float(x, default=0.0):
            try:
                return float(x) if pd.notna(x) else default
            except Exception:
                return default
        
        stock_data = []
        for _, row in df.iterrows():
            try:
                stock_info = {
                    "code": str(row.get("代码", "")),
                    "name": str(row.get("名称", "")),
                    "latest_price": safe_float(row.get("最新价")),
                    "change_percent": safe_float(row.get("涨跌幅")),
                    "change_amount": safe_float(row.get("涨跌额")),
                    "volume": safe_float(row.get("成交量")),
                    "turnover": safe_float(row.get("成交额")),
                    "amplitude": safe_float(row.get("振幅")),
                    "highest": safe_float(row.get("最高")),
                    "lowest": safe_float(row.get("最低")),
                    "open_price": safe_float(row.get("今开")),
                    "prev_close": safe_float(row.get("昨收")),
                    "volume_ratio": safe_float(row.get("量比"), 1.0),
                    "turnover_rate": safe_float(row.get("换手率")),
                    "pe_ratio": safe_float(row.get("市盈率-动态")),
                    "pb_ratio": safe_float(row.get("市净率")),
                    "total_market_value": safe_float(row.get("总市值")),
                    "circulating_market_value": safe_float(row.get("流通市值")),
                    "industry": "未知",
                    "heat_score": min(safe_float(row.get("量比"), 1.0) * 100, 100),
                    "sentiment": "积极" if safe_float(row.get("涨跌幅")) >= 0 else "消极",
                    "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                stock_data.append(stock_info)
            except Exception as e:
                print(f"处理行数据失败: {e}")
                continue
        
        # 保存到JSON文件
        with open("akshare_stock_data.json", "w", encoding="utf-8") as f:
            json.dump(stock_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已保存到akshare_stock_data.json，共{len(stock_data)}条记录")
        return True
        
    except Exception as e:
        print(f"AKShare数据获取失败: {e}")
        return False

def load_stock_data_from_file() -> List[Dict[str, Any]]:
    """从文件加载股票数据"""
    try:
        if not os.path.exists("akshare_stock_data.json"):
            print("数据文件不存在，尝试重新获取...")
            if save_akshare_data_to_file():
                return load_stock_data_from_file()
            else:
                return []
        
        with open("akshare_stock_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"从文件加载了{len(data)}条股票数据")
            return data
            
    except Exception as e:
        print(f"从文件加载数据失败: {e}")
        return []

def fetch_from_akshare() -> List[Dict[str, Any]]:
    """获取股票数据（优先从文件读取）"""
    data = load_stock_data_from_file()
    
    # 转换为原有格式以保持兼容性
    results = []
    for item in data:
        results.append({
            'code': item.get('code', ''),
            'name': item.get('name', ''),
            'price': item.get('latest_price', 0),
            'change_percent': item.get('change_percent', 0),
            'volume': item.get('volume', 0),
            'market_cap': item.get('total_market_value', 0),
            'industry': item.get('industry', '未知'),
            'heat_score': item.get('heat_score', 0),
            'sentiment': item.get('sentiment', '中性'),
            'pe_ratio': item.get('pe_ratio', 0),
            'pb_ratio': item.get('pb_ratio', 0)
        })
    
    return results