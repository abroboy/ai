#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球资金流向API接口
提供资金流向数据的API服务
"""

import pandas as pd
import json
from datetime import datetime, timedelta
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据文件路径
MARKET_FUND_FLOW_FILE = 'akshare_test_ak_stock_market_fund_flow.csv'
INDIVIDUAL_FUND_FLOW_FILE = 'akshare_test_ak_stock_individual_fund_flow.csv'

def load_market_fund_flow_data():
    """加载市场资金流向数据"""
    try:
        if os.path.exists(MARKET_FUND_FLOW_FILE):
            df = pd.read_csv(MARKET_FUND_FLOW_FILE, encoding='utf-8-sig')
            # 转换日期格式
            df['日期'] = pd.to_datetime(df['日期'])
            # 按日期排序
            df = df.sort_values('日期')
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"加载市场资金流向数据失败: {e}")
        return pd.DataFrame()

def load_individual_fund_flow_data():
    """加载个股资金流向数据"""
    try:
        if os.path.exists(INDIVIDUAL_FUND_FLOW_FILE):
            df = pd.read_csv(INDIVIDUAL_FUND_FLOW_FILE, encoding='utf-8-sig')
            # 转换日期格式
            df['日期'] = pd.to_datetime(df['日期'])
            # 按日期排序
            df = df.sort_values('日期')
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"加载个股资金流向数据失败: {e}")
        return pd.DataFrame()

@app.route('/api/global_capital_flow/market_data', methods=['GET'])
def get_market_fund_flow():
    """获取市场资金流向数据"""
    try:
        df = load_market_fund_flow_data()
        
        if df.empty:
            return jsonify({
                'success': False,
                'message': '暂无数据',
                'data': []
            })
        
        # 获取查询参数
        days = request.args.get('days', 30, type=int)
        
        # 获取最近N天的数据
        if days > 0:
            df = df.tail(days)
        
        # 转换为JSON格式
        data = []
        for _, row in df.iterrows():
            data.append({
                'date': row['日期'].strftime('%Y-%m-%d'),
                'shanghai_close': float(row['上证-收盘价']) if pd.notna(row['上证-收盘价']) else 0,
                'shanghai_change': float(row['上证-涨跌幅']) if pd.notna(row['上证-涨跌幅']) else 0,
                'shenzhen_close': float(row['深证-收盘价']) if pd.notna(row['深证-收盘价']) else 0,
                'shenzhen_change': float(row['深证-涨跌幅']) if pd.notna(row['深证-涨跌幅']) else 0,
                'main_net_inflow': float(row['主力净流入-净额']) if pd.notna(row['主力净流入-净额']) else 0,
                'main_net_inflow_ratio': float(row['主力净流入-净占比']) if pd.notna(row['主力净流入-净占比']) else 0,
                'super_large_inflow': float(row['超大单净流入-净额']) if pd.notna(row['超大单净流入-净额']) else 0,
                'super_large_inflow_ratio': float(row['超大单净流入-净占比']) if pd.notna(row['超大单净流入-净占比']) else 0,
                'large_inflow': float(row['大单净流入-净额']) if pd.notna(row['大单净流入-净额']) else 0,
                'large_inflow_ratio': float(row['大单净流入-净占比']) if pd.notna(row['大单净流入-净占比']) else 0,
                'medium_inflow': float(row['中单净流入-净额']) if pd.notna(row['中单净流入-净额']) else 0,
                'medium_inflow_ratio': float(row['中单净流入-净占比']) if pd.notna(row['中单净流入-净占比']) else 0,
                'small_inflow': float(row['小单净流入-净额']) if pd.notna(row['小单净流入-净额']) else 0,
                'small_inflow_ratio': float(row['小单净流入-净占比']) if pd.notna(row['小单净流入-净占比']) else 0
            })
        
        return jsonify({
            'success': True,
            'message': '数据获取成功',
            'data': data,
            'total': len(data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'数据获取失败: {str(e)}',
            'data': []
        })

@app.route('/api/global_capital_flow/individual_data', methods=['GET'])
def get_individual_fund_flow():
    """获取个股资金流向数据"""
    try:
        df = load_individual_fund_flow_data()
        
        if df.empty:
            return jsonify({
                'success': False,
                'message': '暂无数据',
                'data': []
            })
        
        # 获取查询参数
        days = request.args.get('days', 30, type=int)
        
        # 获取最近N天的数据
        if days > 0:
            df = df.tail(days)
        
        # 转换为JSON格式
        data = []
        for _, row in df.iterrows():
            data.append({
                'date': row['日期'].strftime('%Y-%m-%d'),
                'close_price': float(row['收盘价']) if pd.notna(row['收盘价']) else 0,
                'change_ratio': float(row['涨跌幅']) if pd.notna(row['涨跌幅']) else 0,
                'main_net_inflow': float(row['主力净流入-净额']) if pd.notna(row['主力净流入-净额']) else 0,
                'main_net_inflow_ratio': float(row['主力净流入-净占比']) if pd.notna(row['主力净流入-净占比']) else 0,
                'super_large_inflow': float(row['超大单净流入-净额']) if pd.notna(row['超大单净流入-净额']) else 0,
                'super_large_inflow_ratio': float(row['超大单净流入-净占比']) if pd.notna(row['超大单净流入-净占比']) else 0,
                'large_inflow': float(row['大单净流入-净额']) if pd.notna(row['大单净流入-净额']) else 0,
                'large_inflow_ratio': float(row['大单净流入-净占比']) if pd.notna(row['大单净流入-净占比']) else 0,
                'medium_inflow': float(row['中单净流入-净额']) if pd.notna(row['中单净流入-净额']) else 0,
                'medium_inflow_ratio': float(row['中单净流入-净占比']) if pd.notna(row['中单净流入-净占比']) else 0,
                'small_inflow': float(row['小单净流入-净额']) if pd.notna(row['小单净流入-净额']) else 0,
                'small_inflow_ratio': float(row['小单净流入-净占比']) if pd.notna(row['小单净流入-净占比']) else 0
            })
        
        return jsonify({
            'success': True,
            'message': '数据获取成功',
            'data': data,
            'total': len(data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'数据获取失败: {str(e)}',
            'data': []
        })

@app.route('/api/global_capital_flow/summary', methods=['GET'])
def get_capital_flow_summary():
    """获取资金流向汇总数据"""
    try:
        df = load_market_fund_flow_data()
        
        if df.empty:
            return jsonify({
                'success': False,
                'message': '暂无数据',
                'data': {}
            })
        
        # 获取最新数据
        latest_data = df.iloc[-1]
        
        # 计算最近7天的数据
        recent_7_days = df.tail(7)
        
        # 计算统计数据
        summary = {
            'latest_date': latest_data['日期'].strftime('%Y-%m-%d'),
            'shanghai_index': {
                'close': float(latest_data['上证-收盘价']) if pd.notna(latest_data['上证-收盘价']) else 0,
                'change': float(latest_data['上证-涨跌幅']) if pd.notna(latest_data['上证-涨跌幅']) else 0
            },
            'shenzhen_index': {
                'close': float(latest_data['深证-收盘价']) if pd.notna(latest_data['深证-收盘价']) else 0,
                'change': float(latest_data['深证-涨跌幅']) if pd.notna(latest_data['深证-涨跌幅']) else 0
            },
            'today_flow': {
                'main_net_inflow': float(latest_data['主力净流入-净额']) if pd.notna(latest_data['主力净流入-净额']) else 0,
                'super_large_inflow': float(latest_data['超大单净流入-净额']) if pd.notna(latest_data['超大单净流入-净额']) else 0,
                'large_inflow': float(latest_data['大单净流入-净额']) if pd.notna(latest_data['大单净流入-净额']) else 0,
                'medium_inflow': float(latest_data['中单净流入-净额']) if pd.notna(latest_data['中单净流入-净额']) else 0,
                'small_inflow': float(latest_data['小单净流入-净额']) if pd.notna(latest_data['小单净流入-净额']) else 0
            },
            'week_summary': {
                'total_main_inflow': float(recent_7_days['主力净流入-净额'].sum()) if not recent_7_days.empty else 0,
                'positive_days': int((recent_7_days['主力净流入-净额'] > 0).sum()) if not recent_7_days.empty else 0,
                'negative_days': int((recent_7_days['主力净流入-净额'] < 0).sum()) if not recent_7_days.empty else 0,
                'avg_daily_flow': float(recent_7_days['主力净流入-净额'].mean()) if not recent_7_days.empty else 0
            }
        }
        
        return jsonify({
            'success': True,
            'message': '汇总数据获取成功',
            'data': summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'汇总数据获取失败: {str(e)}',
            'data': {}
        })

@app.route('/api/global_capital_flow/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'success': True,
        'message': '全球资金流向API服务正常',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # 切换到API目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("启动全球资金流向API服务...")
    print("API接口:")
    print("- GET /api/global_capital_flow/market_data - 获取市场资金流向数据")
    print("- GET /api/global_capital_flow/individual_data - 获取个股资金流向数据")
    print("- GET /api/global_capital_flow/summary - 获取资金流向汇总数据")
    print("- GET /api/global_capital_flow/health - 健康检查")
    
    app.run(host='0.0.0.0', port=5001, debug=True)