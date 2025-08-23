"""
数据库管理工具
提供数据库连接和操作功能
"""

import pymysql
import pandas as pd
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
from ..utils.logger import logger
from ..config import config


class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self):
        """初始化数据库管理器"""
        self.config = config.database
        self.connection = None
    
    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(
                host=self.config.host,
                port=self.config.port,
                user=self.config.username,
                password=self.config.password,
                database=self.config.database,
                charset=self.config.charset,
                autocommit=True
            )
            logger.info(f"数据库连接成功: {self.config.host}:{self.config.port}/{self.config.database}")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise
    
    def disconnect(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("数据库连接已关闭")
    
    @contextmanager
    def get_cursor(self):
        """获取数据库游标的上下文管理器"""
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            yield cursor
        except Exception as e:
            logger.error(f"数据库操作失败: {e}")
            self.connection.rollback()
            raise
        finally:
            cursor.close()
    
    def execute_query(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """执行查询语句"""
        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    def execute_update(self, sql: str, params: Optional[tuple] = None) -> int:
        """执行更新语句"""
        with self.get_cursor() as cursor:
            rows_affected = cursor.execute(sql, params)
            return rows_affected
    
    def execute_many(self, sql: str, params_list: List[tuple]) -> int:
        """批量执行语句"""
        with self.get_cursor() as cursor:
            rows_affected = cursor.executemany(sql, params_list)
            return rows_affected
    
    def create_table(self, table_sql: str):
        """创建数据表"""
        try:
            self.execute_update(table_sql)
            logger.info("数据表创建成功")
        except Exception as e:
            logger.error(f"数据表创建失败: {e}")
            raise
    
    def insert_data(self, table: str, data: Dict[str, Any]) -> int:
        """插入单条数据"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        return self.execute_update(sql, tuple(data.values()))
    
    def insert_many(self, table: str, data_list: List[Dict[str, Any]]) -> int:
        """批量插入数据"""
        if not data_list:
            return 0
        
        columns = list(data_list[0].keys())
        placeholders = ', '.join(['%s'] * len(columns))
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        
        values_list = [tuple(data[col] for col in columns) for data in data_list]
        return self.execute_many(sql, values_list)
    
    def update_data(self, table: str, data: Dict[str, Any], condition: str, params: tuple) -> int:
        """更新数据"""
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        
        all_params = tuple(data.values()) + params
        return self.execute_update(sql, all_params)
    
    def delete_data(self, table: str, condition: str, params: tuple) -> int:
        """删除数据"""
        sql = f"DELETE FROM {table} WHERE {condition}"
        return self.execute_update(sql, params)
    
    def query_to_dataframe(self, sql: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """查询结果转换为DataFrame"""
        results = self.execute_query(sql, params)
        return pd.DataFrame(results)
    
    def table_exists(self, table_name: str) -> bool:
        """检查表是否存在"""
        sql = """
        SELECT COUNT(*) as count 
        FROM information_schema.tables 
        WHERE table_schema = %s AND table_name = %s
        """
        result = self.execute_query(sql, (self.config.database, table_name))
        return result[0]['count'] > 0
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """获取表结构信息"""
        sql = f"DESCRIBE {table_name}"
        return self.execute_query(sql)
    
    def get_table_count(self, table_name: str) -> int:
        """获取表记录数"""
        sql = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.execute_query(sql)
        return result[0]['count']
    
    def backup_table(self, table_name: str, backup_suffix: str = "_backup"):
        """备份数据表"""
        backup_table = f"{table_name}{backup_suffix}"
        sql = f"CREATE TABLE {backup_table} AS SELECT * FROM {table_name}"
        self.execute_update(sql)
        logger.info(f"数据表备份成功: {table_name} -> {backup_table}")
    
    def truncate_table(self, table_name: str):
        """清空数据表"""
        sql = f"TRUNCATE TABLE {table_name}"
        self.execute_update(sql)
        logger.info(f"数据表清空成功: {table_name}")


# 全局数据库管理器实例
db_manager = DatabaseManager() 