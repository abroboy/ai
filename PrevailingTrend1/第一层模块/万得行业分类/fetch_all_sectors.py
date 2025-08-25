"""
拉取A股所有板块的股票数据
"""

import requests
import pymysql
import time
import json

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def get_all_sectors():
    """获取所有板块信息"""
    url = "http://80.push2.eastmoney.com/api/qt/clist/get"
    params = {
        'pn': 1,
        'pz': 1000,
        'po': 1,
        'np': 1,
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': 2,
        'invt': 2,
        'fid': 'f3',
        'fs': 'b:BK0707',  # 申万一级行业
        'fields': 'f12,f14,f3,f2,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        
        sectors = []
        if data['rc'] == 0 and 'data' in data and 'diff' in data['data']:
            for item in data['data']['diff']:
                sector_code = str(item.get('f12', ''))
                sector_name = item.get('f14', '')
                if sector_code and sector_name:
                    sectors.append({
                        'code': sector_code,
                        'name': sector_name
                    })
        
        return sectors
    except Exception as e:
        print(f"获取板块信息失败: {e}")
        return []

def get_stocks_by_sector(sector_code):
    """根据板块代码获取股票列表"""
    url = "http://80.push2.eastmoney.com/api/qt/clist/get"
    params = {
        'pn': 1,
        'pz': 10000,
        'po': 1,
        'np': 1,
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': 2,
        'invt': 2,
        'fid': 'f3',
        'fs': f'b:{sector_code}',
        'fields': 'f12,f14,f3,f2,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        
        stocks = []
        if data['rc'] == 0 and 'data' in data and 'diff' in data['data']:
            for item in data['data']['diff']:
                stock_code = str(item.get('f12', ''))
                stock_name = item.get('f14', '')
                if stock_code and stock_name and len(stock_code) == 6:
                    stocks.append({
                        'stock_code': stock_code,
                        'stock_name': stock_name,
                        'sector_code': sector_code
                    })
        
        return stocks
    except Exception as e:
        print(f"获取板块{sector_code}股票失败: {e}")
        return []

def get_industry_mapping():
    """获取行业分类映射"""
    # 申万一级行业分类
    industry_map = {
        '801010': '农林牧渔',
        '801020': '采掘',
        '801030': '化工',
        '801040': '钢铁',
        '801050': '有色金属',
        '801080': '电子',
        '801110': '家用电器',
        '801120': '食品饮料',
        '801130': '纺织服装',
        '801140': '轻工制造',
        '801150': '医药生物',
        '801160': '公用事业',
        '801170': '交通运输',
        '801180': '房地产',
        '801200': '商业贸易',
        '801210': '休闲服务',
        '801230': '综合',
        '801710': '建筑材料',
        '801720': '建筑装饰',
        '801730': '电气设备',
        '801740': '国防军工',
        '801750': '计算机',
        '801760': '传媒',
        '801770': '通信',
        '801780': '银行',
        '801790': '非银金融',
        '801880': '汽车',
        '801890': '机械设备'
    }
    return industry_map

def save_to_database(all_stocks, industry_map):
    """保存股票数据到数据库"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 清空现有数据
        print("清空现有股票数据...")
        cursor.execute("DELETE FROM stock_industry_mapping")
        
        # 插入数据
        print(f"插入 {len(all_stocks)} 条股票数据...")
        for stock in all_stocks:
            sector_code = stock['sector_code']
            industry_name = industry_map.get(sector_code, '')
            
            sql = """
            INSERT INTO stock_industry_mapping 
            (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                stock['stock_code'],
                stock['stock_name'],
                sector_code,
                industry_name,
                'confirmed',
                1.0
            ))
        
        connection.commit()
        
        # 统计信息
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping")
        total = cursor.fetchone()[0]
        print(f"总股票数: {total}")
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE industry_name != ''")
        mapped = cursor.fetchone()[0]
        print(f"已映射股票数: {mapped}")
        
        # 按行业统计
        cursor.execute("""
            SELECT industry_name, COUNT(*) as count 
            FROM stock_industry_mapping 
            WHERE industry_name != '' 
            GROUP BY industry_name 
            ORDER BY count DESC
        """)
        industries = cursor.fetchall()
        print("\n行业分布:")
        for industry, count in industries:
            print(f"  {industry}: {count}只股票")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"保存数据失败: {e}")
        return False

def main():
    """主函数"""
    print("开始拉取A股所有板块数据...")
    
    # 获取行业映射
    industry_map = get_industry_mapping()
    print(f"获取到 {len(industry_map)} 个行业分类")
    
    # 获取所有板块
    sectors = get_all_sectors()
    print(f"获取到 {len(sectors)} 个板块")
    
    all_stocks = []
    
    # 遍历每个板块获取股票
    for i, sector in enumerate(sectors):
        print(f"处理板块 {i+1}/{len(sectors)}: {sector['name']} ({sector['code']})")
        
        stocks = get_stocks_by_sector(sector['code'])
        print(f"  获取到 {len(stocks)} 只股票")
        
        all_stocks.extend(stocks)
        time.sleep(0.5)  # 避免请求过快
    
    print(f"\n总共获取到 {len(all_stocks)} 只股票")
    
    # 去重
    unique_stocks = {}
    for stock in all_stocks:
        key = stock['stock_code']
        if key not in unique_stocks:
            unique_stocks[key] = stock
    
    unique_list = list(unique_stocks.values())
    print(f"去重后: {len(unique_list)} 只股票")
    
    # 保存到数据库
    if unique_list:
        if save_to_database(unique_list, industry_map):
            print("✅ 成功获取并保存所有板块股票数据！")
        else:
            print("❌ 保存数据失败！")
    else:
        print("❌ 未获取到任何股票数据！")

if __name__ == "__main__":
    main() 