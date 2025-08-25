# -*- coding: utf-8 -*-
"""
数据库管理工具
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
import logging
from datetime import datetime
import json

from config import DATABASE_CONFIG
from models import Base

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, config=None):
        """初始化数据库管理器"""
        self.config = config or DATABASE_CONFIG
        self.engine = None
        self.Session = None
        self.logger = logging.getLogger(__name__)
        
    def connect(self):
        """连接数据库"""
        try:
            # 构建数据库连接字符串
            connection_string = (
                f"mysql+pymysql://{self.config['user']}:{self.config['password']}"
                f"@{self.config['host']}:{self.config['port']}/{self.config['database']}"
                f"?charset={self.config['charset']}"
            )
            
            # 创建数据库引擎
            self.engine = create_engine(
                connection_string,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False
            )
            
            # 创建会话工厂
            session_factory = sessionmaker(bind=self.engine)
            self.Session = scoped_session(session_factory)
            
            self.logger.info("数据库连接成功")
            return True
            
        except Exception as e:
            self.logger.error(f"数据库连接失败: {e}")
            return False
    
    def create_tables(self):
        """创建数据库表"""
        try:
            Base.metadata.create_all(self.engine)
            self.logger.info("数据库表创建成功")
            return True
        except Exception as e:
            self.logger.error(f"数据库表创建失败: {e}")
            return False
    
    def get_session(self):
        """获取数据库会话"""
        if not self.Session:
            self.connect()
        return self.Session()
    
    def close_session(self, session):
        """关闭数据库会话"""
        if session:
            session.close()
    
    def execute_query(self, query, params=None):
        """执行查询"""
        session = self.get_session()
        try:
            result = session.execute(text(query), params or {})
            return result.fetchall()
        except Exception as e:
            self.logger.error(f"查询执行失败: {e}")
            return []
        finally:
            self.close_session(session)
    
    def execute_update(self, query, params=None):
        """执行更新"""
        session = self.get_session()
        try:
            result = session.execute(text(query), params or {})
            session.commit()
            return result.rowcount
        except Exception as e:
            session.rollback()
            self.logger.error(f"更新执行失败: {e}")
            return 0
        finally:
            self.close_session(session)
    
    def check_table_exists(self, table_name):
        """检查表是否存在"""
        try:
            query = """
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = :database 
                AND table_name = :table_name
            """
            result = self.execute_query(query, {
                'database': self.config['database'],
                'table_name': table_name
            })
            return result[0][0] > 0
        except Exception as e:
            self.logger.error(f"检查表存在性失败: {e}")
            return False
    
    def get_table_info(self, table_name):
        """获取表信息"""
        try:
            query = """
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                FROM information_schema.columns 
                WHERE table_schema = :database 
                AND table_name = :table_name
                ORDER BY ORDINAL_POSITION
            """
            return self.execute_query(query, {
                'database': self.config['database'],
                'table_name': table_name
            })
        except Exception as e:
            self.logger.error(f"获取表信息失败: {e}")
            return []
    
    def backup_table(self, table_name, backup_suffix=None):
        """备份表"""
        try:
            if not backup_suffix:
                backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            backup_table_name = f"{table_name}_backup_{backup_suffix}"
            
            # 创建备份表
            create_backup_query = f"CREATE TABLE {backup_table_name} LIKE {table_name}"
            self.execute_update(create_backup_query)
            
            # 复制数据
            copy_data_query = f"INSERT INTO {backup_table_name} SELECT * FROM {table_name}"
            rows_copied = self.execute_update(copy_data_query)
            
            self.logger.info(f"表 {table_name} 备份成功，备份表: {backup_table_name}，复制行数: {rows_copied}")
            return backup_table_name
            
        except Exception as e:
            self.logger.error(f"表备份失败: {e}")
            return None
    
    def get_database_stats(self):
        """获取数据库统计信息"""
        try:
            stats = {}
            
            # 获取表列表
            tables_query = """
                SELECT table_name, table_rows, data_length, index_length
                FROM information_schema.tables 
                WHERE table_schema = :database
            """
            tables = self.execute_query(tables_query, {'database': self.config['database']})
            
            for table in tables:
                table_name = table[0]
                stats[table_name] = {
                    'rows': table[1] or 0,
                    'data_size_mb': round((table[2] or 0) / 1024 / 1024, 2),
                    'index_size_mb': round((table[3] or 0) / 1024 / 1024, 2)
                }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"获取数据库统计信息失败: {e}")
            return {}
    
    def optimize_tables(self):
        """优化数据库表"""
        try:
            tables_query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = :database
            """
            tables = self.execute_query(tables_query, {'database': self.config['database']})
            
            optimized_count = 0
            for table in tables:
                table_name = table[0]
                try:
                    optimize_query = f"OPTIMIZE TABLE {table_name}"
                    self.execute_update(optimize_query)
                    optimized_count += 1
                except Exception as e:
                    self.logger.warning(f"优化表 {table_name} 失败: {e}")
            
            self.logger.info(f"数据库表优化完成，优化表数量: {optimized_count}")
            return optimized_count
            
        except Exception as e:
            self.logger.error(f"数据库表优化失败: {e}")
            return 0
    
    def close(self):
        """关闭数据库连接"""
        if self.engine:
            self.engine.dispose()
            self.logger.info("数据库连接已关闭") 