"""
数据库工具类
提供数据库连接和操作功能
"""

import pymysql
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger
from config import config
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        self.config = config.DATABASE
        self.connection = None
    
    def get_connection(self):
        """获取数据库连接"""
        if self.connection is None or not self.connection.open:
            try:
                self.connection = pymysql.connect(
                    host=self.config['host'],
                    port=self.config['port'],
                    user=self.config['user'],
                    password=self.config['password'],
                    database=self.config['database'],
                    charset=self.config['charset'],
                    cursorclass=pymysql.cursors.DictCursor
                )
                logger.info("数据库连接成功")
            except Exception as e:
                logger.error(f"数据库连接失败: {e}")
                raise
        return self.connection
    
    def close_connection(self):
        """关闭数据库连接"""
        if self.connection and self.connection.open:
            self.connection.close()
            logger.info("数据库连接已关闭")
    
    def create_tables(self):
        """创建数据表"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # 创建热点数据表
            table_sql = """
            CREATE TABLE IF NOT EXISTS l1_domestic_hotspot_data (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                hotspot_id VARCHAR(100) NOT NULL COMMENT '热点ID',
                title VARCHAR(500) NOT NULL COMMENT '热点标题',
                content TEXT NOT NULL COMMENT '热点内容',
                hotspot_type VARCHAR(20) NOT NULL COMMENT '热点类型',
                hotspot_level VARCHAR(20) NOT NULL DEFAULT 'medium' COMMENT '热点级别',
                status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '热点状态',
                source VARCHAR(100) COMMENT '数据来源',
                url VARCHAR(1000) COMMENT '原始链接',
                publish_time DATETIME COMMENT '发布时间',
                keywords JSON COMMENT '关键词列表',
                related_companies JSON COMMENT '相关公司列表',
                related_industries JSON COMMENT '相关行业列表',
                sentiment_score DECIMAL(3,2) COMMENT '情感得分',
                heat_score DECIMAL(5,2) COMMENT '热度得分',
                update_date DATETIME COMMENT '数据更新日期',
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                
                UNIQUE KEY uk_hotspot_id (hotspot_id),
                KEY idx_title (title(100)),
                KEY idx_hotspot_type (hotspot_type),
                KEY idx_hotspot_level (hotspot_level),
                KEY idx_status (status),
                KEY idx_source (source),
                KEY idx_publish_time (publish_time),
                KEY idx_sentiment_score (sentiment_score),
                KEY idx_heat_score (heat_score),
                KEY idx_update_date (update_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='国内热点数据表';
            """
            
            cursor.execute(table_sql)
            connection.commit()
            logger.info("热点数据表创建成功")
            
            cursor.close()
            
        except Exception as e:
            logger.error(f"创建数据表失败: {e}")
            raise
    
    def insert_hotspot(self, hotspot: HotspotModel) -> bool:
        """插入热点数据"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            sql = """
            INSERT INTO l1_domestic_hotspot_data 
            (hotspot_id, title, content, hotspot_type, hotspot_level, status, source, url, 
             publish_time, keywords, related_companies, related_industries, sentiment_score, 
             heat_score, update_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            content = VALUES(content),
            hotspot_type = VALUES(hotspot_type),
            hotspot_level = VALUES(hotspot_level),
            status = VALUES(status),
            source = VALUES(source),
            url = VALUES(url),
            publish_time = VALUES(publish_time),
            keywords = VALUES(keywords),
            related_companies = VALUES(related_companies),
            related_industries = VALUES(related_industries),
            sentiment_score = VALUES(sentiment_score),
            heat_score = VALUES(heat_score),
            update_date = VALUES(update_date)
            """
            
            cursor.execute(sql, (
                hotspot.hotspot_id,
                hotspot.title,
                hotspot.content,
                hotspot.hotspot_type.value,
                hotspot.hotspot_level.value,
                hotspot.status.value,
                hotspot.source,
                hotspot.url,
                hotspot.publish_time,
                json.dumps(hotspot.keywords, ensure_ascii=False),
                json.dumps(hotspot.related_companies, ensure_ascii=False),
                json.dumps(hotspot.related_industries, ensure_ascii=False),
                hotspot.sentiment_score,
                hotspot.heat_score,
                hotspot.update_date or datetime.now()
            ))
            
            connection.commit()
            logger.info(f"热点数据插入成功: {hotspot.hotspot_id}")
            return True
            
        except Exception as e:
            logger.error(f"插入热点数据失败: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def batch_insert_hotspots(self, hotspots: List[HotspotModel]) -> int:
        """批量插入热点数据"""
        success_count = 0
        for hotspot in hotspots:
            if self.insert_hotspot(hotspot):
                success_count += 1
        logger.info(f"批量插入完成: {success_count}/{len(hotspots)} 成功")
        return success_count
    
    def get_hotspot_by_id(self, hotspot_id: str) -> Optional[HotspotModel]:
        """根据ID获取热点数据"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            sql = "SELECT * FROM l1_domestic_hotspot_data WHERE hotspot_id = %s"
            cursor.execute(sql, (hotspot_id,))
            result = cursor.fetchone()
            
            if result:
                return self._row_to_hotspot_model(result)
            return None
            
        except Exception as e:
            logger.error(f"获取热点数据失败: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def get_hotspots(self, 
                    hotspot_type: Optional[str] = None,
                    hotspot_level: Optional[str] = None,
                    status: Optional[str] = None,
                    source: Optional[str] = None,
                    limit: int = 100,
                    offset: int = 0) -> List[HotspotModel]:
        """获取热点数据列表"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            sql = "SELECT * FROM l1_domestic_hotspot_data WHERE 1=1"
            params = []
            
            if hotspot_type:
                sql += " AND hotspot_type = %s"
                params.append(hotspot_type)
            
            if hotspot_level:
                sql += " AND hotspot_level = %s"
                params.append(hotspot_level)
            
            if status:
                sql += " AND status = %s"
                params.append(status)
            
            if source:
                sql += " AND source = %s"
                params.append(source)
            
            sql += " ORDER BY update_date DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor.execute(sql, params)
            results = cursor.fetchall()
            
            return [self._row_to_hotspot_model(row) for row in results]
            
        except Exception as e:
            logger.error(f"获取热点数据列表失败: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def get_hotspots_statistics(self) -> Dict[str, Any]:
        """获取热点数据统计信息"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            stats = {}
            
            # 总数统计
            cursor.execute("SELECT COUNT(*) as total FROM l1_domestic_hotspot_data")
            stats['total'] = cursor.fetchone()['total']
            
            # 按类型统计
            cursor.execute("SELECT hotspot_type, COUNT(*) as count FROM l1_domestic_hotspot_data GROUP BY hotspot_type")
            stats['by_type'] = {row['hotspot_type']: row['count'] for row in cursor.fetchall()}
            
            # 按级别统计
            cursor.execute("SELECT hotspot_level, COUNT(*) as count FROM l1_domestic_hotspot_data GROUP BY hotspot_level")
            stats['by_level'] = {row['hotspot_level']: row['count'] for row in cursor.fetchall()}
            
            # 按状态统计
            cursor.execute("SELECT status, COUNT(*) as count FROM l1_domestic_hotspot_data GROUP BY status")
            stats['by_status'] = {row['status']: row['count'] for row in cursor.fetchall()}
            
            # 按来源统计
            cursor.execute("SELECT source, COUNT(*) as count FROM l1_domestic_hotspot_data GROUP BY source")
            stats['by_source'] = {row['source']: row['count'] for row in cursor.fetchall()}
            
            # 平均热度得分
            cursor.execute("SELECT AVG(heat_score) as avg_heat FROM l1_domestic_hotspot_data WHERE heat_score IS NOT NULL")
            stats['avg_heat_score'] = float(cursor.fetchone()['avg_heat'] or 0)
            
            # 平均情感得分
            cursor.execute("SELECT AVG(sentiment_score) as avg_sentiment FROM l1_domestic_hotspot_data WHERE sentiment_score IS NOT NULL")
            stats['avg_sentiment_score'] = float(cursor.fetchone()['avg_sentiment'] or 0)
            
            cursor.close()
            return stats
            
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return {}
    
    def update_hotspot_status(self, hotspot_id: str, status: str) -> bool:
        """更新热点状态"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            sql = "UPDATE l1_domestic_hotspot_data SET status = %s WHERE hotspot_id = %s"
            cursor.execute(sql, (status, hotspot_id))
            connection.commit()
            
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                logger.info(f"热点状态更新成功: {hotspot_id} -> {status}")
                return True
            else:
                logger.warning(f"热点不存在: {hotspot_id}")
                return False
                
        except Exception as e:
            logger.error(f"更新热点状态失败: {e}")
            return False
    
    def delete_hotspot(self, hotspot_id: str) -> bool:
        """删除热点数据"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            sql = "DELETE FROM l1_domestic_hotspot_data WHERE hotspot_id = %s"
            cursor.execute(sql, (hotspot_id,))
            connection.commit()
            
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                logger.info(f"热点数据删除成功: {hotspot_id}")
                return True
            else:
                logger.warning(f"热点不存在: {hotspot_id}")
                return False
                
        except Exception as e:
            logger.error(f"删除热点数据失败: {e}")
            return False
    
    def _row_to_hotspot_model(self, row: Dict[str, Any]) -> HotspotModel:
        """将数据库行转换为HotspotModel对象"""
        try:
            # 处理JSON字段
            keywords = json.loads(row['keywords']) if row['keywords'] else []
            related_companies = json.loads(row['related_companies']) if row['related_companies'] else []
            related_industries = json.loads(row['related_industries']) if row['related_industries'] else []
            
            return HotspotModel(
                hotspot_id=row['hotspot_id'],
                title=row['title'],
                content=row['content'],
                hotspot_type=HotspotType(row['hotspot_type']),
                hotspot_level=HotspotLevel(row['hotspot_level']),
                status=HotspotStatus(row['status']),
                source=row['source'] or '',
                url=row['url'],
                publish_time=row['publish_time'],
                keywords=keywords,
                related_companies=related_companies,
                related_industries=related_industries,
                sentiment_score=float(row['sentiment_score']) if row['sentiment_score'] else None,
                heat_score=float(row['heat_score']) if row['heat_score'] else None,
                update_date=row['update_date'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        except Exception as e:
            logger.error(f"转换热点数据失败: {e}")
            raise


# 创建全局数据库管理器实例
db_manager = DatabaseManager() 