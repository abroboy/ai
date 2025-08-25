#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取股票K线数据脚本
支持A股和港股通的K线数据获取
"""

import akshare as ak
import pymysql
import json
import time
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Optional
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kline_data.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

class KlineDataCollector:
    """K线数据收集器"""
    
    def __init__(self):
        self.db_config = DB_CONFIG
        self.connection = None
        
    def get_db_connection(self):
        """获取数据库连接"""
        try:
            if self.connection is None or not self.connection.open:
                self.connection = pymysql.connect(**self.db_config)
            return self.connection
        except Exception as e:
            logging.error(f"数据库连接失败: {e}")
            return None
    
    def get_stock_list(self) -> List[Dict]:
        """获取股票列表"""
        try:
            connection = self.get_db_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT stock_code, stock_name, industry_name 
                FROM stock_industry_mapping 
                ORDER BY stock_code
            """)
            
            stocks = cursor.fetchall()
            cursor.close()
            
            logging.info(f"获取到 {len(stocks)} 只股票")
            return stocks
            
        except Exception as e:
            logging.error(f"获取股票列表失败: {e}")
            return []
    
    def get_akshare_kline_data(self, stock_code: str, period: str = "daily", 
                              start_date: str = None, end_date: str = None) -> Optional[pd.DataFrame]:
        """使用AKShare获取K线数据"""
        try:
            # 根据股票代码长度判断市场类型
            if len(stock_code) == 6:
                # A股 - 使用更稳定的接口
                try:
                    # 方法1: 使用东方财富接口
                    kline_data = ak.stock_zh_a_hist(symbol=stock_code, period=period, 
                                                   start_date=start_date, end_date=end_date, 
                                                   adjust="qfq")
                except:
                    try:
                        # 方法2: 使用新浪接口
                        kline_data = ak.stock_zh_a_daily(symbol=stock_code, start_date=start_date, end_date=end_date)
                    except:
                        # 方法3: 使用腾讯接口
                        kline_data = ak.stock_zh_a_hist_163(symbol=stock_code, start_date=start_date, end_date=end_date)
                
            elif len(stock_code) == 5:
                # 港股
                try:
                    kline_data = ak.stock_hk_hist(symbol=stock_code, period=period, 
                                                 start_date=start_date, end_date=end_date, 
                                                 adjust="qfq")
                except:
                    # 备用方法
                    kline_data = ak.stock_hk_daily(symbol=stock_code, start_date=start_date, end_date=end_date)
            else:
                logging.warning(f"不支持的股票代码格式: {stock_code}")
                return None
            
            if kline_data is None or kline_data.empty:
                logging.warning(f"未获取到 {stock_code} 的K线数据")
                return None
            
            logging.info(f"成功获取 {stock_code} 的K线数据，共 {len(kline_data)} 条记录")
            return kline_data
            
        except Exception as e:
            logging.error(f"获取 {stock_code} K线数据失败: {e}")
            return None
    
    def save_kline_data_to_db(self, stock_code: str, kline_data: pd.DataFrame) -> bool:
        """保存K线数据到数据库"""
        try:
            connection = self.get_db_connection()
            if not connection:
                return False
            
            cursor = connection.cursor()
            
            # 创建K线数据表（如果不存在）
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS stock_kline_data (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                stock_code VARCHAR(10) NOT NULL,
                trade_date DATE NOT NULL,
                open_price DECIMAL(10,4),
                high_price DECIMAL(10,4),
                low_price DECIMAL(10,4),
                close_price DECIMAL(10,4),
                volume BIGINT,
                amount DECIMAL(20,4),
                amplitude DECIMAL(10,4),
                change_percent DECIMAL(10,4),
                change_amount DECIMAL(10,4),
                turnover_rate DECIMAL(10,4),
                period VARCHAR(10) DEFAULT 'daily',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY uk_stock_date_period (stock_code, trade_date, period),
                INDEX idx_stock_code (stock_code),
                INDEX idx_trade_date (trade_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            cursor.execute(create_table_sql)
            
            # 准备插入数据
            insert_sql = """
            INSERT INTO stock_kline_data 
            (stock_code, trade_date, open_price, high_price, low_price, close_price, 
             volume, amount, amplitude, change_percent, change_amount, turnover_rate, period)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            open_price = VALUES(open_price),
            high_price = VALUES(high_price),
            low_price = VALUES(low_price),
            close_price = VALUES(close_price),
            volume = VALUES(volume),
            amount = VALUES(amount),
            amplitude = VALUES(amplitude),
            change_percent = VALUES(change_percent),
            change_amount = VALUES(change_amount),
            turnover_rate = VALUES(turnover_rate),
            updated_at = CURRENT_TIMESTAMP
            """
            
            # 处理数据并插入
            success_count = 0
            for _, row in kline_data.iterrows():
                try:
                    # 根据AKShare返回的实际列名进行适配
                    trade_date = row.get('日期', row.get('date', row.get('Date')))
                    open_price = row.get('开盘', row.get('open', row.get('Open')))
                    high_price = row.get('最高', row.get('high', row.get('High')))
                    low_price = row.get('最低', row.get('low', row.get('Low')))
                    close_price = row.get('收盘', row.get('close', row.get('Close')))
                    volume = row.get('成交量', row.get('volume', row.get('Volume')))
                    amount = row.get('成交额', row.get('amount', row.get('Amount')))
                    amplitude = row.get('振幅', row.get('amplitude', 0))
                    change_percent = row.get('涨跌幅', row.get('change_percent', 0))
                    change_amount = row.get('涨跌额', row.get('change_amount', 0))
                    turnover_rate = row.get('换手率', row.get('turnover_rate', 0))
                    
                    # 数据类型转换
                    if isinstance(trade_date, str):
                        trade_date = datetime.strptime(trade_date, '%Y-%m-%d').date()
                    elif hasattr(trade_date, 'date'):
                        trade_date = trade_date.date()
                    
                    # 处理数值类型
                    def safe_float(value):
                        if pd.isna(value) or value is None:
                            return None
                        try:
                            return float(value)
                        except:
                            return None
                    
                    def safe_int(value):
                        if pd.isna(value) or value is None:
                            return None
                        try:
                            return int(float(value))
                        except:
                            return None
                    
                    values = (
                        stock_code,
                        trade_date,
                        safe_float(open_price),
                        safe_float(high_price),
                        safe_float(low_price),
                        safe_float(close_price),
                        safe_int(volume),
                        safe_float(amount),
                        safe_float(amplitude),
                        safe_float(change_percent),
                        safe_float(change_amount),
                        safe_float(turnover_rate),
                        'daily'
                    )
                    
                    cursor.execute(insert_sql, values)
                    success_count += 1
                    
                except Exception as e:
                    logging.error(f"插入 {stock_code} 数据失败: {e}")
                    continue
            
            connection.commit()
            cursor.close()
            
            logging.info(f"成功保存 {stock_code} 的 {success_count} 条K线数据")
            return True
            
        except Exception as e:
            logging.error(f"保存 {stock_code} K线数据失败: {e}")
            return False
    
    def update_single_stock_kline(self, stock_code: str) -> bool:
        """更新单个股票的K线数据"""
        logging.info(f"开始更新 {stock_code} 的K线数据...")
        
        # 获取最近30天的数据
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
        
        # 获取K线数据
        kline_data = self.get_akshare_kline_data(stock_code, start_date=start_date, end_date=end_date)
        
        if kline_data is None:
            return False
        
        # 保存到数据库
        return self.save_kline_data_to_db(stock_code, kline_data)
    
    def batch_update_kline_data(self, limit: int = 50) -> Dict:
        """批量更新K线数据"""
        logging.info("开始批量更新K线数据...")
        
        stocks = self.get_stock_list()
        if not stocks:
            return {'success': False, 'message': '未获取到股票列表'}
        
        # 限制处理数量
        stocks = stocks[:limit]
        
        success_count = 0
        failed_count = 0
        failed_stocks = []
        
        for i, stock in enumerate(stocks, 1):
            stock_code = stock['stock_code']
            logging.info(f"处理进度: {i}/{len(stocks)} - {stock_code}")
            
            try:
                if self.update_single_stock_kline(stock_code):
                    success_count += 1
                else:
                    failed_count += 1
                    failed_stocks.append(stock_code)
                
                # 避免请求过于频繁
                time.sleep(0.5)
                
            except Exception as e:
                logging.error(f"处理 {stock_code} 失败: {e}")
                failed_count += 1
                failed_stocks.append(stock_code)
        
        result = {
            'success': True,
            'total': len(stocks),
            'success_count': success_count,
            'failed_count': failed_count,
            'failed_stocks': failed_stocks
        }
        
        logging.info(f"批量更新完成: {result}")
        return result
    
    def get_kline_data_from_db(self, stock_code: str, limit: int = 100) -> List[Dict]:
        """从数据库获取K线数据"""
        try:
            connection = self.get_db_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT trade_date, open_price, high_price, low_price, close_price, 
                       volume, amount, change_percent, change_amount
                FROM stock_kline_data 
                WHERE stock_code = %s 
                ORDER BY trade_date DESC 
                LIMIT %s
            """, (stock_code, limit))
            
            data = cursor.fetchall()
            cursor.close()
            
            return data
            
        except Exception as e:
            logging.error(f"从数据库获取 {stock_code} K线数据失败: {e}")
            return []

def main():
    """主函数"""
    collector = KlineDataCollector()
    
    # 测试单个股票更新
    test_stock = "000001"  # 平安银行
    logging.info(f"测试更新 {test_stock} 的K线数据")
    
    if collector.update_single_stock_kline(test_stock):
        logging.info(f"{test_stock} 更新成功")
        
        # 获取并显示数据
        data = collector.get_kline_data_from_db(test_stock, 10)
        logging.info(f"获取到 {len(data)} 条数据")
        for item in data[:3]:  # 显示前3条
            logging.info(f"数据: {item}")
    else:
        logging.error(f"{test_stock} 更新失败")

if __name__ == "__main__":
    main() 