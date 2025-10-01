#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
import os
from typing import List, Dict, Any

def read_stock_data_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    读取股票数据CSV文件（修复：跳过第一行列名，正确处理数据）
    """
    stocks = []
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            # 直接使用reader读取CSV
            reader = csv.reader(f)
            # 跳过第一行（列名行）
            header_skipped = False
            for row in reader:
                # 跳过第一行（列名行）
                if not header_skipped:
                    header_skipped = True
                    continue
                
                # 确保行有足够的数据列
                if len(row) >= 10:
                    # 数据清洗和类型转换 - 直接根据列的位置映射到字段
                    stock = {
                        'symbol': row[0],  # 第一列是symbol
                        'code': row[1],    # 第二列是code
                        'name': row[2],    # 第三列是name
                        'open': safe_float(row[3]),     # 第四列是open
                        'high': safe_float(row[4]),     # 第五列是high
                        'low': safe_float(row[5]),      # 第六列是low
                        'volume': safe_int(row[6]),     # 第七列是volume
                        'amount': safe_float(row[7]),   # 第八列是amount
                        'mktcap': safe_float(row[8]),   # 第九列是mktcap
                        'turnoverratio': safe_float(row[9])  # 第十列是turnoverratio
                    }
                    stocks.append(stock)
    except Exception as e:
        print(f"读取股票数据文件失败: {e}")
        return []
    
    return stocks

def read_company_names_csv(file_path: str) -> List[Dict[str, str]]:
    """
    读取公司名称CSV文件
    """
    companies = []
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                company = {
                    'code': row.get('code', '').strip(),
                    'name': row.get('name', '').strip()
                }
                companies.append(company)
    except Exception as e:
        print(f"读取公司名称文件失败: {e}")
        return []
    
    return companies

def merge_stock_and_company_data(stock_data: List[Dict], company_data: List[Dict]) -> List[Dict]:
    """
    合并股票数据和公司名称数据
    """
    # 创建公司名称映射
    company_map = {comp['code']: comp['name'] for comp in company_data}
    
    merged_data = []
    for stock in stock_data:
        # 使用公司名称文件中的名称，如果没有则使用股票数据中的名称
        code = stock['code']
        if code in company_map:
            stock['name'] = company_map[code]
        
        # 添加行业分类（基于股票代码前缀简单分类）
        stock['industry'] = classify_industry_by_code(code)
        
        # 计算一些衍生指标
        stock['market_cap_billion'] = safe_float(stock['mktcap']) / 100000000 if stock['mktcap'] else 0
        stock['price_change'] = calculate_price_change(stock)
        
        merged_data.append(stock)
    
    return merged_data

def classify_industry_by_code(code: str) -> str:
    """
    根据股票代码简单分类行业
    """
    if not code:
        return '未知行业'
    
    # 基于股票代码前缀的简单行业分类
    code_prefix = code[:3]
    
    industry_mapping = {
        '000': '深圳主板',
        '001': '深圳主板',
        '002': '深圳中小板',
        '003': '深圳主板',
        '300': '创业板',
        '600': '上海主板',
        '601': '上海主板',
        '603': '上海主板',
        '605': '上海主板',
        '688': '科创板',
        '920': '北交所',
        '430': '新三板',
        '831': '新三板',
        '833': '新三板',
        '835': '新三板',
        '836': '新三板',
        '837': '新三板',
        '838': '新三板',
        '839': '新三板'
    }
    
    return industry_mapping.get(code_prefix, '其他板块')

def calculate_price_change(stock: Dict) -> float:
    """
    计算价格变化百分比（简单估算）
    """
    try:
        open_price = stock.get('open', 0)
        high_price = stock.get('high', 0)
        low_price = stock.get('low', 0)
        
        if open_price and high_price and low_price:
            # 简单估算当前价格为高低价平均值
            current_price = (high_price + low_price) / 2
            change_percent = ((current_price - open_price) / open_price) * 100
            return round(change_percent, 2)
    except:
        pass
    
    return 0.0

def safe_float(value) -> float:
    """
    安全转换为浮点数
    """
    try:
        return float(value) if value else 0.0
    except (ValueError, TypeError):
        return 0.0

def safe_int(value) -> int:
    """
    安全转换为整数
    """
    try:
        return int(float(value)) if value else 0
    except (ValueError, TypeError):
        return 0

def get_industry_statistics(merged_data: List[Dict]) -> Dict[str, Any]:
    """
    计算行业统计数据
    """
    industry_stats = {}
    
    for stock in merged_data:
        industry = stock.get('industry', '未知行业')
        
        if industry not in industry_stats:
            industry_stats[industry] = {
                'industry_name': industry,
                'company_count': 0,
                'total_market_cap': 0,
                'total_volume': 0,
                'total_amount': 0,
                'companies': []
            }
        
        stats = industry_stats[industry]
        stats['company_count'] += 1
        stats['total_market_cap'] += stock.get('market_cap_billion', 0)
        stats['total_volume'] += stock.get('volume', 0)
        stats['total_amount'] += stock.get('amount', 0)
        stats['companies'].append(stock)
    
    # 计算平均值
    for industry, stats in industry_stats.items():
        if stats['company_count'] > 0:
            stats['avg_market_cap'] = stats['total_market_cap'] / stats['company_count']
            stats['avg_volume'] = stats['total_volume'] / stats['company_count']
            stats['avg_amount'] = stats['total_amount'] / stats['company_count']
    
    return industry_stats

def build_csv_based_response(page: int = 0, size: int = 50, industry: str = None) -> Dict[str, Any]:
    """
    构建基于CSV数据的响应
    """
    try:
        # 获取文件路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        stock_file = os.path.join(base_dir, 'api', 'akshare_test_enhanced_ak_stock_zh_a_new.csv')
        company_file = os.path.join(base_dir, 'api', 'akshare_test_ak_stock_info_a_code_name.csv')
        
        # 读取数据
        stock_data = read_stock_data_csv(stock_file)
        company_data = read_company_names_csv(company_file)
        
        # 合并数据
        merged_data = merge_stock_and_company_data(stock_data, company_data)
        
        # 按行业过滤
        if industry:
            merged_data = [stock for stock in merged_data if stock.get('industry') == industry]
        
        # 分页处理
        total_count = len(merged_data)
        start_idx = page * size
        end_idx = start_idx + size
        page_data = merged_data[start_idx:end_idx]
        
        return {
            'success': True,
            'data': {
                'content': page_data,
                'totalElements': total_count,
                'totalPages': (total_count + size - 1) // size,
                'currentPage': page,
                'pageSize': size
            },
            'message': f'成功获取 {len(page_data)} 条数据'
        }
        
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'message': f'获取数据失败: {str(e)}'
        }

def build_industry_statistics_response() -> Dict[str, Any]:
    """
    构建行业统计响应
    """
    try:
        # 获取文件路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        stock_file = os.path.join(base_dir, 'api', 'akshare_test_enhanced_ak_stock_zh_a_new.csv')
        company_file = os.path.join(base_dir, 'api', 'akshare_test_ak_stock_info_a_code_name.csv')
        
        # 读取数据
        stock_data = read_stock_data_csv(stock_file)
        company_data = read_company_names_csv(company_file)
        
        # 合并数据
        merged_data = merge_stock_and_company_data(stock_data, company_data)
        
        # 获取行业统计
        industry_stats = get_industry_statistics(merged_data)
        
        # 转换为列表格式
        industries_list = []
        industry_code = 100000
        
        for industry_name, stats in industry_stats.items():
            industries_list.append({
                'industryCode': str(industry_code),
                'industryName': industry_name,
                'industryLevel': 1,
                'parentIndustryCode': None,
                'companyCount': stats['company_count'],
                'totalMarketCap': round(stats['total_market_cap'], 2),
                'avgMarketCap': round(stats['avg_market_cap'], 2),
                'totalVolume': stats['total_volume'],
                'totalAmount': round(stats['total_amount'], 2),
                'companies': stats['companies']
            })
            industry_code += 1
        
        # 按公司数量排序
        industries_list.sort(key=lambda x: x['companyCount'], reverse=True)
        
        return {
            'success': True,
            'data': {
                'industries': industries_list,
                'totalIndustries': len(industries_list),
                'totalCompanies': len(merged_data),
                'totalMarketCap': sum(industry['totalMarketCap'] for industry in industries_list)
            },
            'message': f'成功获取 {len(industries_list)} 个行业统计数据'
        }
        
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'message': f'获取行业统计失败: {str(e)}'
        }

if __name__ == '__main__':
    # 测试代码
    response = build_csv_based_response(0, 10)
    print(json.dumps(response, ensure_ascii=False, indent=2))
    
    stats_response = build_industry_statistics_response()
    print(json.dumps(stats_response, ensure_ascii=False, indent=2))