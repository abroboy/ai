import pymysql
import requests
import time

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def get_industry_mapping():
    """获取行业映射关系"""
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

def get_stocks_by_industry(industry_code):
    """根据行业代码获取股票列表"""
    url = "http://push2.eastmoney.com/api/qt/clist/get"
    params = {
        'pn': 1,
        'pz': 10000,
        'po': 1,
        'np': 1,
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': 2,
        'invt': 2,
        'fid': 'f3',
        'fs': f'b:{industry_code}',
        'fields': 'f12,f14'
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
                        'industry_code': industry_code
                    })
        
        return stocks
    except Exception as e:
        print(f"获取行业{industry_code}股票失败: {e}")
        return []

def update_stock_industry_mapping():
    """更新股票行业映射"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        industry_map = get_industry_mapping()
        print(f"开始更新 {len(industry_map)} 个行业的股票映射...")
        
        total_updated = 0
        
        for industry_code, industry_name in industry_map.items():
            print(f"处理行业: {industry_name} ({industry_code})")
            
            stocks = get_stocks_by_industry(industry_code)
            if stocks:
                print(f"  获取到 {len(stocks)} 只股票")
                
                for stock in stocks:
                    # 更新股票行业信息
                    sql = """
                    UPDATE stock_industry_mapping 
                    SET industry_code = %s, industry_name = %s, mapping_status = 'confirmed', confidence = 1.0
                    WHERE stock_code = %s
                    """
                    cursor.execute(sql, (industry_code, industry_name, stock['stock_code']))
                    total_updated += 1
            else:
                print(f"  未获取到股票数据")
            
            time.sleep(0.5)  # 避免请求过快
        
        connection.commit()
        print(f"✅ 成功更新 {total_updated} 只股票的行业映射")
        
        # 统计更新后的数据
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE industry_name != ''")
        mapped_count = cursor.fetchone()[0]
        print(f"📊 已映射股票数: {mapped_count}")
        
        cursor.execute("SELECT industry_name, COUNT(*) as count FROM stock_industry_mapping WHERE industry_name != '' GROUP BY industry_name ORDER BY count DESC")
        industries = cursor.fetchall()
        print("\n行业分布:")
        for industry, count in industries:
            print(f"  {industry}: {count}只股票")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"更新失败: {e}")
        return False

if __name__ == "__main__":
    print("开始修复行业映射...")
    if update_stock_industry_mapping():
        print("✅ 行业映射修复完成！")
    else:
        print("❌ 行业映射修复失败！") 