"""
从真实数据源拉取股票数据
支持Tushare、AKShare等数据源
"""

import pymysql
import requests
import pandas as pd
import time
import logging
from datetime import datetime
from typing import List, Dict, Any

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

class RealStockDataFetcher:
    """真实股票数据获取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_from_tushare(self):
        """从Tushare获取股票数据"""
        try:
            import tushare as ts
            ts.set_token('your_tushare_token')  # 需要设置您的token
            pro = ts.pro_api()
            
            # 获取A股列表
            logger.info("从Tushare获取A股列表...")
            a_stocks = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,industry')
            
            # 获取港股列表
            logger.info("从Tushare获取港股列表...")
            hk_stocks = pro.stock_basic(exchange='HK', list_status='L', fields='ts_code,symbol,name,industry')
            
            return a_stocks, hk_stocks
            
        except ImportError:
            logger.warning("Tushare未安装，尝试其他数据源")
            return None, None
        except Exception as e:
            logger.error(f"Tushare数据获取失败: {e}")
            return None, None
    
    def fetch_from_akshare(self):
        """从AKShare获取股票数据"""
        try:
            import akshare as ak
            
            # 获取A股列表
            logger.info("从AKShare获取A股列表...")
            a_stocks = ak.stock_info_a_code_name()
            
            # 获取港股列表
            logger.info("从AKShare获取港股列表...")
            hk_stocks = ak.stock_hk_spot_em()
            
            return a_stocks, hk_stocks
            
        except ImportError:
            logger.warning("AKShare未安装，尝试其他数据源")
            return None, None
        except Exception as e:
            logger.error(f"AKShare数据获取失败: {e}")
            return None, None
    
    def fetch_from_eastmoney(self):
        """从东方财富获取股票数据"""
        try:
            # A股列表接口
            a_url = "http://80.push2.eastmoney.com/api/qt/clist/get"
            a_params = {
                'pn': 1,
                'pz': 5000,
                'po': 1,
                'np': 1,
                'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
                'fltt': 2,
                'invt': 2,
                'fid': 'f3',
                'fs': 'm:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23',
                'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
            }
            
            logger.info("从东方财富获取A股列表...")
            a_response = self.session.get(a_url, params=a_params, timeout=30)
            a_data = a_response.json()
            
            # 港股列表接口
            hk_url = "http://80.push2.eastmoney.com/api/qt/clist/get"
            hk_params = {
                'pn': 1,
                'pz': 2000,
                'po': 1,
                'np': 1,
                'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
                'fltt': 2,
                'invt': 2,
                'fid': 'f3',
                'fs': 'm:128+t:3,m:128+t:4,m:128+t:1,m:128+t:2',
                'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
            }
            
            logger.info("从东方财富获取港股列表...")
            hk_response = self.session.get(hk_url, params=hk_params, timeout=30)
            hk_data = hk_response.json()
            
            return a_data, hk_data
            
        except Exception as e:
            logger.error(f"东方财富数据获取失败: {e}")
            return None, None
    
    def fetch_from_sina(self):
        """从新浪财经获取股票数据"""
        try:
            # A股列表
            a_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
            a_params = {
                'page': 1,
                'num': 5000,
                'sort': 'symbol',
                'asc': 1,
                'node': 'hs_a',
                'symbol': '',
                '_s_r_a': 'page'
            }
            
            logger.info("从新浪财经获取A股列表...")
            a_response = self.session.get(a_url, params=a_params, timeout=30)
            a_data = a_response.json()
            
            return a_data, None
            
        except Exception as e:
            logger.error(f"新浪财经数据获取失败: {e}")
            return None, None
    
    def process_stock_data(self, data_source: str, a_data, hk_data):
        """处理股票数据"""
        stocks = []
        
        if data_source == "eastmoney":
            # 处理东方财富数据
            if a_data and 'data' in a_data and 'diff' in a_data['data']:
                for item in a_data['data']['diff']:
                    stock_code = str(item.get('f12', ''))
                    stock_name = item.get('f14', '')
                    if stock_code and stock_name:
                        stocks.append({
                            'stock_code': stock_code,
                            'stock_name': stock_name,
                            'market': 'A股',
                            'industry_code': '',
                            'industry_name': '',
                            'mapping_status': 'pending',
                            'confidence': 0.0
                        })
            
            if hk_data and 'data' in hk_data and 'diff' in hk_data['data']:
                for item in hk_data['data']['diff']:
                    stock_code = str(item.get('f12', ''))
                    stock_name = item.get('f14', '')
                    if stock_code and stock_name:
                        stocks.append({
                            'stock_code': stock_code,
                            'stock_name': stock_name,
                            'market': '港股',
                            'industry_code': '',
                            'industry_name': '',
                            'mapping_status': 'pending',
                            'confidence': 0.0
                        })
        
        elif data_source == "sina":
            # 处理新浪数据
            if a_data:
                for item in a_data:
                    stock_code = item.get('symbol', '').replace('sh', '').replace('sz', '')
                    stock_name = item.get('name', '')
                    if stock_code and stock_name:
                        stocks.append({
                            'stock_code': stock_code,
                            'stock_name': stock_name,
                            'market': 'A股',
                            'industry_code': '',
                            'industry_name': '',
                            'mapping_status': 'pending',
                            'confidence': 0.0
                        })
        
        return stocks
    
    def save_to_database(self, stocks: List[Dict]):
        """保存股票数据到数据库"""
        try:
            connection = pymysql.connect(**DB_CONFIG)
            cursor = connection.cursor()
            
            # 清空现有数据
            logger.info("清空现有股票数据...")
            cursor.execute("DELETE FROM stock_industry_mapping")
            
            # 插入新数据
            logger.info(f"插入 {len(stocks)} 条股票数据...")
            for stock in stocks:
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
            logger.info(f"成功保存 {len(stocks)} 条股票数据")
            
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
    
    def fetch_all_stocks(self):
        """获取所有股票数据"""
        logger.info("开始从多个数据源获取股票数据...")
        
        # 尝试不同的数据源
        data_sources = [
            ("eastmoney", self.fetch_from_eastmoney),
            ("sina", self.fetch_from_sina),
            ("tushare", self.fetch_from_tushare),
            ("akshare", self.fetch_from_akshare)
        ]
        
        for source_name, fetch_func in data_sources:
            try:
                logger.info(f"尝试从 {source_name} 获取数据...")
                a_data, hk_data = fetch_func()
                
                if a_data or hk_data:
                    stocks = self.process_stock_data(source_name, a_data, hk_data)
                    if stocks:
                        logger.info(f"从 {source_name} 获取到 {len(stocks)} 条股票数据")
                        if self.save_to_database(stocks):
                            logger.info(f"成功从 {source_name} 获取并保存股票数据")
                            return True
                
                time.sleep(1)  # 避免请求过快
                
            except Exception as e:
                logger.error(f"从 {source_name} 获取数据失败: {e}")
                continue
        
        logger.error("所有数据源都获取失败")
        return False

def main():
    """主函数"""
    fetcher = RealStockDataFetcher()
    success = fetcher.fetch_all_stocks()
    
    if success:
        print("✅ 成功从真实数据源获取股票数据！")
        print("📊 数据已保存到数据库")
        print("🌐 访问 http://127.0.0.1:5001 查看数据")
    else:
        print("❌ 获取股票数据失败！")
        print("请检查网络连接和数据源配置")

if __name__ == "__main__":
    main() 