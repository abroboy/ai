"""
获取更多股票数据
"""

import pymysql
import requests
import json
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def fetch_more_a_stocks():
    """获取更多A股数据"""
    all_stocks = []
    
    # 分页获取更多A股数据
    for page in range(1, 21):  # 获取20页，每页5000只
        url = "http://80.push2.eastmoney.com/api/qt/clist/get"
        params = {
            'pn': page,
            'pz': 5000,
            'po': 1,
            'np': 1,
            'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
            'fltt': 2,
            'invt': 2,
            'fid': 'f3',
            'fs': 'm:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23',
            'fields': 'f12,f14,f3,f2,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
        }
        
        try:
            print(f"获取A股第{page}页数据...")
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if data['rc'] == 0 and 'data' in data and 'diff' in data['data']:
                page_stocks = []
                for item in data['data']['diff']:
                    stock_code = str(item.get('f12', ''))
                    stock_name = item.get('f14', '')
                    if stock_code and stock_name and len(stock_code) == 6:
                        page_stocks.append({
                            'stock_code': stock_code,
                            'stock_name': stock_name,
                            'industry_code': '',
                            'industry_name': '',
                            'mapping_status': 'pending',
                            'confidence': 0.0
                        })
                
                all_stocks.extend(page_stocks)
                print(f"第{page}页获取到 {len(page_stocks)} 只股票")
                
                if len(page_stocks) < 5000:  # 如果数据不足5000，说明已经到最后一页
                    break
                    
            time.sleep(0.5)  # 避免请求过快
            
        except Exception as e:
            logger.error(f"获取A股第{page}页数据失败: {e}")
            continue
    
    return all_stocks

def fetch_more_hk_stocks():
    """获取更多港股数据"""
    all_stocks = []
    
    # 分页获取更多港股数据
    for page in range(1, 11):  # 获取10页，每页2000只
        url = "http://80.push2.eastmoney.com/api/qt/clist/get"
        params = {
            'pn': page,
            'pz': 2000,
            'po': 1,
            'np': 1,
            'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
            'fltt': 2,
            'invt': 2,
            'fid': 'f3',
            'fs': 'm:128+t:3,m:128+t:4,m:128+t:1,m:128+t:2',
            'fields': 'f12,f14,f3,f2,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
        }
        
        try:
            print(f"获取港股第{page}页数据...")
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if data['rc'] == 0 and 'data' in data and 'diff' in data['data']:
                page_stocks = []
                for item in data['data']['diff']:
                    stock_code = str(item.get('f12', ''))
                    stock_name = item.get('f14', '')
                    if stock_code and stock_name and len(stock_code) == 5:
                        page_stocks.append({
                            'stock_code': stock_code,
                            'stock_name': stock_name,
                            'industry_code': '',
                            'industry_name': '',
                            'mapping_status': 'pending',
                            'confidence': 0.0
                        })
                
                all_stocks.extend(page_stocks)
                print(f"第{page}页获取到 {len(page_stocks)} 只股票")
                
                if len(page_stocks) < 2000:  # 如果数据不足2000，说明已经到最后一页
                    break
                    
            time.sleep(0.5)  # 避免请求过快
            
        except Exception as e:
            logger.error(f"获取港股第{page}页数据失败: {e}")
            continue
    
    return all_stocks

def save_to_database(stocks):
    """保存股票数据到数据库"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 清空现有数据
        logger.info("清空现有股票数据...")
        cursor.execute("DELETE FROM stock_industry_mapping")
        
        # 去重
        unique_stocks = {}
        for stock in stocks:
            key = stock['stock_code']
            if key not in unique_stocks:
                unique_stocks[key] = stock
        
        unique_stocks_list = list(unique_stocks.values())
        
        # 插入新数据
        logger.info(f"插入 {len(unique_stocks_list)} 条股票数据...")
        for stock in unique_stocks_list:
            sql = """
            INSERT INTO stock_industry_mapping 
            (stock_code, stock_name, industry_code, industry_name, mapping_status, confidence)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                stock['stock_code'],
                stock['stock_name'],
                stock['industry_code'],
                stock['industry_name'],
                stock['mapping_status'],
                stock['confidence']
            ))
        
        connection.commit()
        logger.info(f"成功保存 {len(unique_stocks_list)} 条股票数据")
        
        # 统计信息
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping")
        total = cursor.fetchone()[0]
        logger.info(f"数据库中现有股票总数: {total}")
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE LENGTH(stock_code) = 6")
        a_stocks = cursor.fetchone()[0]
        logger.info(f"A股数量: {a_stocks}")
        
        cursor.execute("SELECT COUNT(*) FROM stock_industry_mapping WHERE LENGTH(stock_code) = 5")
        hk_stocks = cursor.fetchone()[0]
        logger.info(f"港股数量: {hk_stocks}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        logger.error(f"保存数据失败: {e}")
        return False

def main():
    """主函数"""
    print("开始获取更多股票数据...")
    
    # 获取更多A股数据
    print("获取更多A股数据...")
    a_stocks = fetch_more_a_stocks()
    print(f"获取到 {len(a_stocks)} 只A股")
    
    # 获取更多港股数据
    print("获取更多港股数据...")
    hk_stocks = fetch_more_hk_stocks()
    print(f"获取到 {len(hk_stocks)} 只港股")
    
    # 合并数据
    all_stocks = a_stocks + hk_stocks
    print(f"总共获取到 {len(all_stocks)} 只股票")
    
    if all_stocks:
        # 保存到数据库
        if save_to_database(all_stocks):
            print("✅ 成功获取并保存更多股票数据！")
            print(f"📊 数据统计:")
            print(f"   - 总股票数: {len(all_stocks)}")
            print(f"   - A股数量: {len(a_stocks)}")
            print(f"   - 港股数量: {len(hk_stocks)}")
            print("🌐 访问 http://127.0.0.1:5001 查看数据")
        else:
            print("❌ 保存数据失败！")
    else:
        print("❌ 未获取到任何股票数据！")

if __name__ == "__main__":
    main() 