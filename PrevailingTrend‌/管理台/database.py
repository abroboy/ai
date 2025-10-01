#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库模块
用于存储和管理国内上市公司的数据
"""

import os
import sqlite3
import json
import time
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'database.log'))
    ]
)
logger = logging.getLogger('market_database')

# 全局数据库实例
_db_instance = None

def get_db_instance():
    """
    获取数据库实例（单例模式）
    
    Returns:
        MarketDatabase: 数据库实例
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = MarketDatabase()
    return _db_instance

def init_db():
    """
    初始化数据库
    
    Returns:
        bool: 是否成功
    """
    try:
        db = get_db_instance()
        logger.info("数据库初始化成功")
        return True
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        return False

def update_stock_data(stocks_data):
    """
    更新股票数据
    
    Args:
        stocks_data (list): 股票数据列表
    
    Returns:
        bool: 是否成功
    """
    try:
        db = get_db_instance()
        result = db.batch_insert_stocks(stocks_data)
        
        # 更新行业数据
        industries = {}
        for stock in stocks_data:
            industry_name = stock.get('industry')
            if not industry_name:
                continue
                
            if industry_name not in industries:
                industries[industry_name] = {
                    'name': industry_name,
                    'company_count': 0,
                    'total_market_cap': 0,
                    'total_change': 0,
                    'positive_count': 0,
                    'negative_count': 0
                }
            
            industries[industry_name]['company_count'] += 1
            industries[industry_name]['total_market_cap'] += stock.get('market_cap', 0)
            
            change = stock.get('change_percent', 0)
            industries[industry_name]['total_change'] += change
            
            if change >= 0:
                industries[industry_name]['positive_count'] += 1
            else:
                industries[industry_name]['negative_count'] += 1
        
        # 计算行业平均变化和情绪
        industry_data_list = []
        for name, data in industries.items():
            avg_change = data['total_change'] / data['company_count'] if data['company_count'] > 0 else 0
            
            # 根据涨跌家数确定行业情绪
            if data['positive_count'] > data['negative_count']:
                sentiment = '积极'
            elif data['positive_count'] < data['negative_count']:
                sentiment = '消极'
            else:
                sentiment = '中性'
            
            # 计算行业热度分数（简单算法：市值 * 公司数量 / 1000）
            heat_score = (data['total_market_cap'] * data['company_count']) / 1000
            
            industry_data_list.append({
                'name': name,
                'avg_change': avg_change,
                'company_count': data['company_count'],
                'total_market_cap': data['total_market_cap'],
                'heat_score': heat_score,
                'sentiment': sentiment
            })
        
        # 批量更新行业数据
        if industry_data_list:
            db.batch_insert_industries(industry_data_list)
        
        logger.info(f"更新股票数据成功，共{len(stocks_data)}条记录")
        return result
    except Exception as e:
        logger.error(f"更新股票数据失败: {str(e)}")
        return False

def get_stocks(limit=None, offset=None, order_by='heat_score', order_dir='DESC'):
    """
    获取股票列表
    
    Args:
        limit (int, optional): 限制数量
        offset (int, optional): 偏移量
        order_by (str, optional): 排序字段
        order_dir (str, optional): 排序方向，ASC或DESC
    
    Returns:
        list: 股票数据列表
    """
    try:
        db = get_db_instance()
        stocks = db.get_stocks(limit, offset, order_by, order_dir)
        
        # 添加last_update字段，与前端保持一致
        for stock in stocks:
            stock['last_update'] = stock.get('update_time')
            
        return stocks
    except Exception as e:
        logger.error(f"获取股票列表失败: {str(e)}")
        return []

def get_industries(limit=None, offset=None, order_by='heat_score', order_dir='DESC'):
    """
    获取行业列表
    
    Args:
        limit (int, optional): 限制数量
        offset (int, optional): 偏移量
        order_by (str, optional): 排序字段
        order_dir (str, optional): 排序方向，ASC或DESC
    
    Returns:
        list: 行业数据列表
    """
    try:
        db = get_db_instance()
        return db.get_industries(limit, offset, order_by, order_dir)
    except Exception as e:
        logger.error(f"获取行业列表失败: {str(e)}")
        return []

def get_db_tables():
    """
    获取数据库表信息
    
    Returns:
        list: 表信息列表
    """
    try:
        db = get_db_instance()
        
        # 获取所有表名
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in db.cursor.fetchall()]
        
        # 获取每个表的信息
        result = []
        for table_name in tables:
            table_info = db.get_table_info(table_name)
            if table_info:
                result.append(table_info)
        
        return result
    except Exception as e:
        logger.error(f"获取数据库表信息失败: {str(e)}")
        return []

def execute_db_query(query):
    """
    执行数据库查询
    
    Args:
        query (str): SQL查询语句
    
    Returns:
        dict: 查询结果
    """
    try:
        db = get_db_instance()
        
        # 检查是否是SELECT查询
        if not query.strip().upper().startswith('SELECT'):
            return {
                "success": False,
                "message": "只允许执行SELECT查询",
                "data": None
            }
        
        # 执行查询
        result = db.execute_query(query)
        
        if result is not None:
            return {
                "success": True,
                "message": "查询执行成功",
                "data": result
            }
        else:
            return {
                "success": False,
                "message": "查询执行失败",
                "data": None
            }
    except Exception as e:
        logger.error(f"执行数据库查询失败: {str(e)}")
        return {
            "success": False,
            "message": f"查询执行失败: {str(e)}",
            "data": None
        }

class MarketDatabase:
    """市场数据库类，用于管理股票和行业数据"""
    
    def __init__(self):
        """初始化数据库连接"""
        self.db_path = os.path.join(os.path.dirname(__file__), 'market_data.db')
        self.conn = sqlite3.connect(self.db_path)
        # 启用外键约束
        self.conn.execute("PRAGMA foreign_keys = ON")
        # 设置行工厂，返回字典而不是元组
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._init_tables()
    
    def _init_tables(self):
        """初始化数据表"""
        # 创建股票表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            industry TEXT,
            price REAL,
            change_percent REAL,
            volume INTEGER,
            market_cap REAL,
            heat_score REAL,
            sentiment TEXT,
            update_time TEXT
        )
        ''')
        
        # 创建行业表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS industries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            avg_change REAL,
            company_count INTEGER,
            total_market_cap REAL,
            heat_score REAL,
            sentiment TEXT,
            update_time TEXT
        )
        ''')
        
        # 创建历史数据表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code TEXT NOT NULL,
            date TEXT NOT NULL,
            open_price REAL,
            close_price REAL,
            high_price REAL,
            low_price REAL,
            volume INTEGER,
            change_percent REAL,
            UNIQUE(stock_code, date),
            FOREIGN KEY(stock_code) REFERENCES stocks(code) ON DELETE CASCADE
        )
        ''')
        
        # 创建预测数据表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code TEXT NOT NULL,
            prediction_date TEXT NOT NULL,
            predicted_price REAL,
            predicted_change REAL,
            confidence REAL,
            model_version TEXT,
            update_time TEXT,
            UNIQUE(stock_code, prediction_date),
            FOREIGN KEY(stock_code) REFERENCES stocks(code) ON DELETE CASCADE
        )
        ''')
        
        # 提交事务
        self.conn.commit()
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
    
    # 股票数据操作方法
    
    def insert_stock(self, stock_data):
        """
        插入股票数据
        
        Args:
            stock_data (dict): 股票数据字典
        
        Returns:
            bool: 是否成功
        """
        try:
            # 准备SQL语句
            sql = '''
            INSERT OR REPLACE INTO stocks 
            (code, name, industry, price, change_percent, volume, market_cap, heat_score, sentiment, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            # 准备参数
            params = (
                stock_data.get('code'),
                stock_data.get('name'),
                stock_data.get('industry'),
                stock_data.get('price'),
                stock_data.get('change_percent'),
                stock_data.get('volume'),
                stock_data.get('market_cap'),
                stock_data.get('heat_score'),
                stock_data.get('sentiment'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            # 执行SQL
            self.cursor.execute(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"插入股票数据失败: {str(e)}")
            self.conn.rollback()
            return False
    
    def batch_insert_stocks(self, stocks_data):
        """
        批量插入股票数据
        
        Args:
            stocks_data (list): 股票数据列表
        
        Returns:
            bool: 是否成功
        """
        try:
            # 准备SQL语句
            sql = '''
            INSERT OR REPLACE INTO stocks 
            (code, name, industry, price, change_percent, volume, market_cap, heat_score, sentiment, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            # 准备参数
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = []
            for stock in stocks_data:
                params.append((
                    stock.get('code'),
                    stock.get('name'),
                    stock.get('industry'),
                    stock.get('price'),
                    stock.get('change_percent'),
                    stock.get('volume'),
                    stock.get('market_cap'),
                    stock.get('heat_score'),
                    stock.get('sentiment'),
                    current_time
                ))
            
            # 执行SQL
            self.cursor.executemany(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"批量插入股票数据失败: {str(e)}")
            self.conn.rollback()
            return False
    
    def get_stock(self, code):
        """
        获取单个股票数据
        
        Args:
            code (str): 股票代码
        
        Returns:
            dict: 股票数据
        """
        try:
            # 执行查询
            self.cursor.execute('SELECT * FROM stocks WHERE code = ?', (code,))
            row = self.cursor.fetchone()
            
            # 转换为字典
            if row:
                return dict(row)
            else:
                return None
        except Exception as e:
            logging.error(f"获取股票数据失败: {str(e)}")
            return None

    def get_stocks(self, limit=None, offset=None, order_by=None, order_dir='DESC'):
        """
        获取股票列表
        
        Args:
            limit (int, optional): 限制数量
            offset (int, optional): 偏移量
            order_by (str, optional): 排序字段
            order_dir (str, optional): 排序方向，ASC或DESC
        
        Returns:
            list: 股票数据列表
        """
        try:
            # 构建SQL
            sql = 'SELECT * FROM stocks'
            
            # 添加排序
            if order_by:
                sql += f' ORDER BY {order_by} {order_dir}'
            
            # 添加分页
            if limit is not None:
                sql += f' LIMIT {limit}'
                if offset is not None:
                    sql += f' OFFSET {offset}'
            
            # 执行查询
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            
            # 转换为字典列表
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"获取股票列表失败: {str(e)}")
            return []
    
    def count_stocks(self):
        """
        获取股票总数
        
        Returns:
            int: 股票总数
        """
        try:
            self.cursor.execute('SELECT COUNT(*) FROM stocks')
            return self.cursor.fetchone()[0]
        except Exception as e:
            logging.error(f"获取股票总数失败: {str(e)}")
            return 0
    
    def search_stocks(self, keyword, limit=None, offset=None):
        """
        搜索股票
        
        Args:
            keyword (str): 关键词
            limit (int, optional): 限制数量
            offset (int, optional): 偏移量
        
        Returns:
            list: 股票数据列表
        """
        try:
            # 构建SQL
            sql = '''
            SELECT * FROM stocks 
            WHERE code LIKE ? OR name LIKE ? OR industry LIKE ?
            '''
            
            # 添加分页
            if limit is not None:
                sql += f' LIMIT {limit}'
                if offset is not None:
                    sql += f' OFFSET {offset}'
            
            # 执行查询
            keyword_param = f'%{keyword}%'
            self.cursor.execute(sql, (keyword_param, keyword_param, keyword_param))
            rows = self.cursor.fetchall()
            
            # 转换为字典列表
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"搜索股票失败: {str(e)}")
            return []
    
    # 行业数据操作方法
    
    def insert_industry(self, industry_data):
        """
        插入行业数据
        
        Args:
            industry_data (dict): 行业数据字典
        
        Returns:
            bool: 是否成功
        """
        try:
            # 准备SQL语句
            sql = '''
            INSERT OR REPLACE INTO industries 
            (name, avg_change, company_count, total_market_cap, heat_score, sentiment, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            
            # 准备参数
            params = (
                industry_data.get('name'),
                industry_data.get('avg_change'),
                industry_data.get('company_count'),
                industry_data.get('total_market_cap'),
                industry_data.get('heat_score'),
                industry_data.get('sentiment'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            # 执行SQL
            self.cursor.execute(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"插入行业数据失败: {str(e)}")
            self.conn.rollback()
            return False
    
    def batch_insert_industries(self, industries_data):
        """
        批量插入行业数据
        
        Args:
            industries_data (list): 行业数据列表
        
        Returns:
            bool: 是否成功
        """
        try:
            # 准备SQL语句
            sql = '''
            INSERT OR REPLACE INTO industries 
            (name, avg_change, company_count, total_market_cap, heat_score, sentiment, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            
            # 准备参数
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = []
            for industry in industries_data:
                params.append((
                    industry.get('name'),
                    industry.get('avg_change'),
                    industry.get('company_count'),
                    industry.get('total_market_cap'),
                    industry.get('heat_score'),
                    industry.get('sentiment'),
                    current_time
                ))
            
            # 执行SQL
            self.cursor.executemany(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"批量插入行业数据失败: {str(e)}")
            self.conn.rollback()
            return False
    
    def get_industries(self, limit=None, offset=None, order_by=None, order_dir='DESC'):
        """
        获取行业列表
        
        Args:
            limit (int, optional): 限制数量
            offset (int, optional): 偏移量
            order_by (str, optional): 排序字段
            order_dir (str, optional): 排序方向，ASC或DESC
        
        Returns:
            list: 行业数据列表
        """
        try:
            # 构建SQL
            sql = 'SELECT * FROM industries'
            
            # 添加排序
            if order_by:
                sql += f' ORDER BY {order_by} {order_dir}'
            
            # 添加分页
            if limit is not None:
                sql += f' LIMIT {limit}'
                if offset is not None:
                    sql += f' OFFSET {offset}'
            
            # 执行查询
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            
            # 转换为字典列表
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"获取行业列表失败: {str(e)}")
            return []
    
    # 历史数据操作方法
    
    def insert_stock_history(self, history_data):
        """
        插入股票历史数据
        
        Args:
            history_data (dict): 历史数据字典
        
        Returns:
            bool: 是否成功
        """
        try:
            # 准备SQL语句
            sql = '''
            INSERT OR REPLACE INTO stock_history 
            (stock_code, date, open_price, close_price, high_price, low_price, volume, change_percent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            # 准备参数
            params = (
                history_data.get('stock_code'),
                history_data.get('date'),
                history_data.get('open_price'),
                history_data.get('close_price'),
                history_data.get('high_price'),
                history_data.get('low_price'),
                history_data.get('volume'),
                history_data.get('change_percent')
            )
            
            # 执行SQL
            self.cursor.execute(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"插入股票历史数据失败: {str(e)}")
            self.conn.rollback()
            return False
    
    def batch_insert_stock_history(self, history_data_list):
        """
        批量插入股票历史数据
        
        Args:
            history_data_list (list): 历史数据列表
        
        Returns:
            bool: 是否成功
        """
        try:
            # 准备SQL语句
            sql = '''
            INSERT OR REPLACE INTO stock_history 
            (stock_code, date, open_price, close_price, high_price, low_price, volume, change_percent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            # 准备参数
            params = []
            for history in history_data_list:
                params.append((
                    history.get('stock_code'),
                    history.get('date'),
                    history.get('open_price'),
                    history.get('close_price'),
                    history.get('high_price'),
                    history.get('low_price'),
                    history.get('volume'),
                    history.get('change_percent')
                ))
            
            # 执行SQL
            self.cursor.executemany(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"批量插入股票历史数据失败: {str(e)}")
            self.conn.rollback()
            return False
    
    def get_stock_history(self, stock_code, start_date=None, end_date=None, limit=None):
        """
        获取股票历史数据
        
        Args:
            stock_code (str): 股票代码
            start_date (str, optional): 开始日期
            end_date (str, optional): 结束日期
            limit (int, optional): 限制数量
        
        Returns:
            list: 历史数据列表
        """
        try:
            # 构建SQL
            sql = 'SELECT * FROM stock_history WHERE stock_code = ?'
            params = [stock_code]
            
            # 添加日期过滤
            if start_date:
                sql += ' AND date >= ?'
                params.append(start_date)
            if end_date:
                sql += ' AND date <= ?'
                params.append(end_date)
            
            # 添加排序
            sql += ' ORDER BY date DESC'
            
            # 添加限制
            if limit:
                sql += f' LIMIT {limit}'
            
            # 执行查询
            self.cursor.execute(sql, params)
            rows = self.cursor.fetchall()
            
            # 转换为字典列表
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"获取股票历史数据失败: {str(e)}")
            return []
    
    # 预测数据操作方法
    
    def insert_stock_prediction(self, prediction_data):
        """
        插入股票预测数据
        
        Args:
            prediction_data (dict): 预测数据字典
        
        Returns:
            bool: 是否成功
        """
        try:
            # 准备SQL语句
            sql = '''
            INSERT OR REPLACE INTO stock_predictions 
            (stock_code, prediction_date, predicted_price, predicted_change, confidence, model_version, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            
            # 准备参数
            params = (
                prediction_data.get('stock_code'),
                prediction_data.get('prediction_date'),
                prediction_data.get('predicted_price'),
                prediction_data.get('predicted_change'),
                prediction_data.get('confidence'),
                prediction_data.get('model_version'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            # 执行SQL
            self.cursor.execute(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"插入股票预测数据失败: {str(e)}")
            self.conn.rollback()
            return False
    
    def batch_insert_stock_predictions(self, predictions_data):
        """
        批量插入股票预测数据
        
        Args:
            predictions_data (list): 预测数据列表
        
        Returns:
            bool: 是否成功
        """
        try:
            # 准备SQL语句
            sql = '''
            INSERT OR REPLACE INTO stock_predictions 
            (stock_code, prediction_date, predicted_price, predicted_change, confidence, model_version, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            
            # 准备参数
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = []
            for prediction in predictions_data:
                params.append((
                    prediction.get('stock_code'),
                    prediction.get('prediction_date'),
                    prediction.get('predicted_price'),
                    prediction.get('predicted_change'),
                    prediction.get('confidence'),
                    prediction.get('model_version'),
                    current_time
                ))
            
            # 执行SQL
            self.cursor.executemany(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"批量插入股票预测数据失败: {str(e)}")
            self.conn.rollback()
            return False
    
    def get_stock_predictions(self, stock_code=None, prediction_date=None):
        """
        获取股票预测数据
        
        Args:
            stock_code (str, optional): 股票代码
            prediction_date (str, optional): 预测日期
        
        Returns:
            list: 预测数据列表
        """
        try:
            # 构建SQL
            sql = 'SELECT * FROM stock_predictions'
            params = []
            
            # 添加过滤条件
            conditions = []
            if stock_code:
                conditions.append('stock_code = ?')
                params.append(stock_code)
            if prediction_date:
                conditions.append('prediction_date = ?')
                params.append(prediction_date)
            
            # 组合条件
            if conditions:
                sql += ' WHERE ' + ' AND '.join(conditions)
            
            # 添加排序
            sql += ' ORDER BY prediction_date ASC'
            
            # 执行查询
            self.cursor.execute(sql, params)
            rows = self.cursor.fetchall()
            
            # 转换为字典列表
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"获取股票预测数据失败: {str(e)}")
            return []
    
    # 数据库管理方法
    
    def get_table_info(self, table_name):
        """
        获取表信息
        
        Args:
            table_name (str): 表名
        
        Returns:
            dict: 表信息
        """
        try:
            # 获取表结构
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [dict(row) for row in self.cursor.fetchall()]
            
            # 获取表行数
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = self.cursor.fetchone()[0]
            
            return {
                'name': table_name,
                'columns': columns,
                'row_count': row_count
            }
        except Exception as e:
            logging.error(f"获取表信息失败: {str(e)}")
            return None
    
    def get_table_data(self, table_name, page=1, page_size=20):
        """
        获取表数据
        
        Args:
            table_name (str): 表名
            page (int, optional): 页码
            page_size (int, optional): 每页大小
        
        Returns:
            dict: 表数据
        """
        try:
            # 获取表结构
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row['name'] for row in self.cursor.fetchall()]
            
            # 获取总行数
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            total = self.cursor.fetchone()[0]
            
            # 计算偏移量
            offset = (page - 1) * page_size
            
            # 获取数据
            self.cursor.execute(f"SELECT * FROM {table_name} LIMIT {page_size} OFFSET {offset}")
            rows = self.cursor.fetchall()
            data = [dict(row) for row in rows]
            
            return {
                'columns': columns,
                'data': data,
                'total': total,
                'page': page,
                'page_size': page_size
            }
        except Exception as e:
            logging.error(f"获取表数据失败: {str(e)}")
            return None
    
    def execute_query(self, query, params=None):
        """
        执行自定义查询
        
        Args:
            query (str): SQL查询语句
            params (tuple, optional): 查询参数
        
        Returns:
            list: 查询结果
        """
        try:
            # 检查是否是SELECT查询
            if not query.strip().upper().startswith('SELECT'):
                raise ValueError("只允许执行SELECT查询")
            
            # 执行查询
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            # 获取结果
            rows = self.cursor.fetchall()
            
            # 转换为字典列表
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"执行查询失败: {str(e)}")
            return None

# 兼容旧的函数名
def execute_db_query(query, params=None):
    """
    执行数据库查询并返回格式化的响应
    
    Args:
        query (str): SQL查询语句
        params (tuple, optional): 查询参数
    
    Returns:
        dict: 查询结果，包含success、message和data字段
    """
    try:
        db = MarketDatabase()
        results = db.execute_query(query, params)
        if results is not None:
            return {
                "success": True,
                "message": "查询成功",
                "data": results
            }
        else:
            return {
                "success": False,
                "message": "查询执行失败",
                "data": None
            }
    except Exception as e:
        logging.error(f"数据库查询错误: {str(e)}")
        return {
            "success": False,
            "message": f"查询执行失败: {str(e)}",
            "data": None
        }