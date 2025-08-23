"""
数据库管理器
提供数据库连接和操作功能
"""

import pymysql
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
from datetime import datetime

from .logger import logger


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, host='localhost', port=3306, user='root', password='', database='prevailing_trend'):
        """初始化数据库管理器"""
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.logger = logger
    
    def connect(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.logger.info(f"成功连接到数据库: {self.host}:{self.port}/{self.database}")
            return True
        except Exception as e:
            self.logger.error(f"数据库连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.logger.info("数据库连接已断开")
    
    @contextmanager
    def get_cursor(self):
        """获取数据库游标的上下文管理器"""
        if not self.connection:
            if not self.connect():
                raise Exception("无法连接到数据库")
        
        cursor = self.connection.cursor()
        try:
            yield cursor
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            cursor.close()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """执行查询语句"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"查询执行失败: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """执行更新语句"""
        try:
            with self.get_cursor() as cursor:
                result = cursor.execute(query, params)
                return result > 0
        except Exception as e:
            self.logger.error(f"更新执行失败: {e}")
            return False
    
    def execute_many(self, query: str, params_list: List[tuple]) -> bool:
        """批量执行语句"""
        try:
            with self.get_cursor() as cursor:
                result = cursor.executemany(query, params_list)
                return result > 0
        except Exception as e:
            self.logger.error(f"批量执行失败: {e}")
            return False
    
    def create_table(self, table_name: str, table_sql: str) -> bool:
        """创建数据表"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(table_sql)
                self.logger.info(f"成功创建表: {table_name}")
                return True
        except Exception as e:
            self.logger.error(f"创建表失败: {e}")
            return False
    
    def insert_data(self, table_name: str, data: Dict[str, Any]) -> bool:
        """插入单条数据"""
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, tuple(data.values()))
                return True
        except Exception as e:
            self.logger.error(f"插入数据失败: {e}")
            return False
    
    def insert_many(self, table_name: str, data_list: List[Dict[str, Any]]) -> bool:
        """批量插入数据"""
        if not data_list:
            return True
        
        try:
            columns = list(data_list[0].keys())
            placeholders = ', '.join(['%s'] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            values_list = [tuple(data.values()) for data in data_list]
            
            with self.get_cursor() as cursor:
                cursor.executemany(query, values_list)
                self.logger.info(f"成功插入 {len(data_list)} 条数据到表 {table_name}")
                return True
        except Exception as e:
            self.logger.error(f"批量插入数据失败: {e}")
            return False
    
    def update_data(self, table_name: str, data: Dict[str, Any], condition: str, params: tuple) -> bool:
        """更新数据"""
        try:
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            
            all_params = tuple(data.values()) + params
            
            with self.get_cursor() as cursor:
                result = cursor.execute(query, all_params)
                return result > 0
        except Exception as e:
            self.logger.error(f"更新数据失败: {e}")
            return False
    
    def delete_data(self, table_name: str, condition: str, params: tuple) -> bool:
        """删除数据"""
        try:
            query = f"DELETE FROM {table_name} WHERE {condition}"
            
            with self.get_cursor() as cursor:
                result = cursor.execute(query, params)
                return result > 0
        except Exception as e:
            self.logger.error(f"删除数据失败: {e}")
            return False
    
    def query_to_dataframe(self, query: str, params: tuple = None) -> Optional['pd.DataFrame']:
        """查询结果转换为DataFrame"""
        try:
            import pandas as pd
            result = self.execute_query(query, params)
            if result:
                return pd.DataFrame(result)
            return None
        except ImportError:
            self.logger.error("pandas未安装，无法转换为DataFrame")
            return None
        except Exception as e:
            self.logger.error(f"转换为DataFrame失败: {e}")
            return None
    
    def table_exists(self, table_name: str) -> bool:
        """检查表是否存在"""
        try:
            query = "SHOW TABLES LIKE %s"
            result = self.execute_query(query, (table_name,))
            return len(result) > 0
        except Exception as e:
            self.logger.error(f"检查表是否存在失败: {e}")
            return False
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """获取表结构信息"""
        try:
            query = f"DESCRIBE {table_name}"
            return self.execute_query(query)
        except Exception as e:
            self.logger.error(f"获取表结构失败: {e}")
            return []
    
    def get_table_count(self, table_name: str) -> int:
        """获取表记录数"""
        try:
            query = f"SELECT COUNT(*) as count FROM {table_name}"
            result = self.execute_query(query)
            return result[0]['count'] if result else 0
        except Exception as e:
            self.logger.error(f"获取表记录数失败: {e}")
            return 0
    
    def backup_table(self, table_name: str, backup_name: str = None) -> bool:
        """备份表"""
        try:
            if not backup_name:
                backup_name = f"{table_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            query = f"CREATE TABLE {backup_name} AS SELECT * FROM {table_name}"
            
            with self.get_cursor() as cursor:
                cursor.execute(query)
                self.logger.info(f"成功备份表 {table_name} 到 {backup_name}")
                return True
        except Exception as e:
            self.logger.error(f"备份表失败: {e}")
            return False
    
    def truncate_table(self, table_name: str) -> bool:
        """清空表"""
        try:
            query = f"TRUNCATE TABLE {table_name}"
            
            with self.get_cursor() as cursor:
                cursor.execute(query)
                self.logger.info(f"成功清空表: {table_name}")
                return True
        except Exception as e:
            self.logger.error(f"清空表失败: {e}")
            return False


# 创建全局数据库管理器实例
db_manager = DatabaseManager() 