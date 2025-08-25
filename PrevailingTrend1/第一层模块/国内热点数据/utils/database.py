import pymysql
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from loguru import logger
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus
from config import config


class DatabaseManager:
    def __init__(self):
        self.config = config
        self.connection = None

    def get_connection(self):
        """获取数据库连接"""
        try:
            if self.connection is None or not self.connection.open:
                self.connection = pymysql.connect(
                    host=self.config.DATABASE['host'],
                    port=self.config.DATABASE['port'],
                    user=self.config.DATABASE['user'],
                    password=self.config.DATABASE['password'],
                    database=self.config.DATABASE['database'],
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                logger.info("数据库连接成功")
            return self.connection
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise

    def create_tables(self):
        """创建数据表"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # 创建热点数据表
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS l1_domestic_hotspot_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hotspot_id VARCHAR(100) UNIQUE NOT NULL,
                title VARCHAR(500) NOT NULL,
                content TEXT,
                hotspot_type VARCHAR(20) NOT NULL,
                hotspot_level VARCHAR(20) NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'active',
                source VARCHAR(100),
                url VARCHAR(500),
                publish_time DATETIME,
                keywords JSON,
                related_companies JSON,
                related_industries JSON,
                sentiment_score DECIMAL(3,2),
                heat_score DECIMAL(5,2),
                update_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_hotspot_type (hotspot_type),
                INDEX idx_hotspot_level (hotspot_level),
                INDEX idx_status (status),
                INDEX idx_source (source),
                INDEX idx_publish_time (publish_time),
                INDEX idx_heat_score (heat_score),
                INDEX idx_sentiment_score (sentiment_score)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            cursor.execute(create_table_sql)
            connection.commit()
            cursor.close()
            logger.info("热点数据表创建成功")
            
        except Exception as e:
            logger.error(f"创建数据表失败: {e}")
            raise

    def insert_hotspot(self, hotspot: HotspotModel) -> bool:
        """插入单个热点数据"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            sql = """
            INSERT INTO l1_domestic_hotspot_data (
                hotspot_id, title, content, hotspot_type, hotspot_level, 
                status, source, url, publish_time, keywords, 
                related_companies, related_industries, sentiment_score, heat_score
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                update_date = CURRENT_TIMESTAMP
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
                hotspot.heat_score
            ))
            
            connection.commit()
            cursor.close()
            logger.info(f"热点数据插入成功: {hotspot.hotspot_id}")
            return True
            
        except Exception as e:
            logger.error(f"插入热点数据失败: {e}")
            return False

    def batch_insert_hotspots(self, hotspots: List[HotspotModel]) -> int:
        """批量插入热点数据"""
        success_count = 0
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            for hotspot in hotspots:
                try:
                    sql = """
                    INSERT INTO l1_domestic_hotspot_data (
                        hotspot_id, title, content, hotspot_type, hotspot_level, 
                        status, source, url, publish_time, keywords, 
                        related_companies, related_industries, sentiment_score, heat_score
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                        update_date = CURRENT_TIMESTAMP
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
                        hotspot.heat_score
                    ))
                    success_count += 1
                    
                except Exception as e:
                    logger.error(f"插入热点数据失败 {hotspot.hotspot_id}: {e}")
                    continue
            
            connection.commit()
            cursor.close()
            logger.info(f"批量插入完成: {success_count}/{len(hotspots)} 成功")
            return success_count
            
        except Exception as e:
            logger.error(f"批量插入热点数据失败: {e}")
            return success_count

    def get_hotspots(self, page: int = 1, per_page: int = 20, 
                    hotspot_type: Optional[str] = None, 
                    source: Optional[str] = None,
                    sort_by: str = 'publish_time',
                    sort_order: str = 'desc') -> Dict[str, Any]:
        """获取热点数据列表"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # 构建查询条件
            where_conditions = []
            params = []
            
            if hotspot_type:
                where_conditions.append("hotspot_type = %s")
                params.append(hotspot_type)
            
            if source:
                where_conditions.append("source = %s")
                params.append(source)
            
            where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
            
            # 获取总数
            count_sql = f"SELECT COUNT(*) as total FROM l1_domestic_hotspot_data{where_clause}"
            cursor.execute(count_sql, params)
            total = cursor.fetchone()['total']
            
            # 获取分页数据
            offset = (page - 1) * per_page
            sql = f"""
            SELECT * FROM l1_domestic_hotspot_data{where_clause}
            ORDER BY {sort_by} {sort_order} LIMIT %s OFFSET %s
            """
            params.extend([per_page, offset])
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            # 转换为模型对象
            hotspots = []
            for row in rows:
                try:
                    hotspot = self._row_to_hotspot_model(row)
                    hotspots.append(hotspot)
                except Exception as e:
                    logger.error(f"转换热点数据失败: {e}")
                    continue
            
            cursor.close()
            
            return {
                'hotspots': hotspots,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page
            }
            
        except Exception as e:
            logger.error(f"获取热点数据列表失败: {e}")
            return {
                'hotspots': [],
                'total': 0,
                'page': page,
                'per_page': per_page,
                'total_pages': 0
            }

    def get_hotspot_by_id(self, hotspot_id: str) -> Optional[HotspotModel]:
        """根据ID获取热点数据"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            sql = "SELECT * FROM l1_domestic_hotspot_data WHERE hotspot_id = %s"
            cursor.execute(sql, (hotspot_id,))
            row = cursor.fetchone()
            
            cursor.close()
            
            if row:
                return self._row_to_hotspot_model(row)
            return None
            
        except Exception as e:
            logger.error(f"获取热点数据失败: {e}")
            return None

    def get_hotspots_statistics(self) -> Dict[str, Any]:
        """获取热点数据统计信息"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            stats = {}
            
            # 总数统计
            try:
                cursor.execute("SELECT COUNT(*) as total FROM l1_domestic_hotspot_data")
                stats['total'] = cursor.fetchone()['total']
            except Exception as e:
                logger.error(f"获取总数统计失败: {e}")
                stats['total'] = 0
            
            # 按类型统计
            try:
                cursor.execute("""
                    SELECT hotspot_type, COUNT(*) as count 
                    FROM l1_domestic_hotspot_data 
                    GROUP BY hotspot_type
                """)
                stats['by_type'] = {row['hotspot_type']: row['count'] for row in cursor.fetchall()}
            except Exception as e:
                logger.error(f"获取类型统计失败: {e}")
                stats['by_type'] = {}
            
            # 按级别统计
            try:
                cursor.execute("""
                    SELECT hotspot_level, COUNT(*) as count 
                    FROM l1_domestic_hotspot_data 
                    GROUP BY hotspot_level
                """)
                stats['by_level'] = {row['hotspot_level']: row['count'] for row in cursor.fetchall()}
            except Exception as e:
                logger.error(f"获取级别统计失败: {e}")
                stats['by_level'] = {}
            
            # 按状态统计
            try:
                cursor.execute("""
                    SELECT status, COUNT(*) as count 
                    FROM l1_domestic_hotspot_data 
                    GROUP BY status
                """)
                stats['by_status'] = {row['status']: row['count'] for row in cursor.fetchall()}
            except Exception as e:
                logger.error(f"获取状态统计失败: {e}")
                stats['by_status'] = {}
            
            # 按来源统计
            try:
                cursor.execute("""
                    SELECT source, COUNT(*) as count 
                    FROM l1_domestic_hotspot_data 
                    GROUP BY source
                """)
                stats['by_source'] = {row['source']: row['count'] for row in cursor.fetchall()}
            except Exception as e:
                logger.error(f"获取来源统计失败: {e}")
                stats['by_source'] = {}
            
            # 平均热度得分
            try:
                cursor.execute("SELECT AVG(heat_score) as avg_heat_score FROM l1_domestic_hotspot_data")
                result = cursor.fetchone()
                stats['avg_heat_score'] = float(result['avg_heat_score']) if result['avg_heat_score'] else 0
            except Exception as e:
                logger.error(f"获取平均热度得分失败: {e}")
                stats['avg_heat_score'] = 0
            
            # 平均情感得分
            try:
                cursor.execute("SELECT AVG(sentiment_score) as avg_sentiment_score FROM l1_domestic_hotspot_data")
                result = cursor.fetchone()
                stats['avg_sentiment_score'] = float(result['avg_sentiment_score']) if result['avg_sentiment_score'] else 0
            except Exception as e:
                logger.error(f"获取平均情感得分失败: {e}")
                stats['avg_sentiment_score'] = 0
            
            cursor.close()
            return stats
            
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return {
                'total': 0, 'by_type': {}, 'by_level': {}, 'by_status': {},
                'by_source': {}, 'avg_heat_score': 0, 'avg_sentiment_score': 0
            }

    def _row_to_hotspot_model(self, row: Dict[str, Any]) -> HotspotModel:
        """将数据库行转换为热点模型"""
        try:
            # 解析JSON字段
            keywords = json.loads(row['keywords']) if row['keywords'] else []
            related_companies = json.loads(row['related_companies']) if row['related_companies'] else []
            related_industries = json.loads(row['related_industries']) if row['related_industries'] else []
            
            return HotspotModel(
                hotspot_id=row['hotspot_id'],
                title=row['title'],
                content=row['content'] or '',
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
                update_date=row['update_date']
            )
        except Exception as e:
            logger.error(f"转换热点数据失败: {e}")
            raise

    def get_industry_rankings(self) -> List[Dict[str, Any]]:
        """获取行业热度排名"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # 从热点数据中提取行业信息并计算热度
            sql = """
            SELECT 
                JSON_UNQUOTE(JSON_EXTRACT(related_industries, '$[*]')) as industry,
                AVG(heat_score) as avg_heat,
                COUNT(*) as count,
                MAX(heat_score) as max_heat
            FROM l1_domestic_hotspot_data 
            WHERE related_industries IS NOT NULL 
            AND related_industries != '[]'
            GROUP BY industry
            ORDER BY avg_heat DESC
            LIMIT 20
            """
            
            cursor.execute(sql)
            results = cursor.fetchall()
            
            rankings = []
            for row in results:
                rankings.append({
                    'industry': row[0] if row[0] else '未知行业',
                    'heat_score': round(float(row[1]), 1),
                    'count': row[2],
                    'trend': 'up' if float(row[1]) > 80 else 'stable'
                })
            
            cursor.close()
            return rankings
            
        except Exception as e:
            logger.error(f"获取行业热度排名失败: {e}")
            return []

    def get_company_rankings(self) -> List[Dict[str, Any]]:
        """获取公司热度排名"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # 从热点数据中提取公司信息并计算热度
            sql = """
            SELECT 
                JSON_UNQUOTE(JSON_EXTRACT(related_companies, '$[*]')) as company,
                AVG(heat_score) as avg_heat,
                COUNT(*) as count,
                MAX(heat_score) as max_heat
            FROM l1_domestic_hotspot_data 
            WHERE related_companies IS NOT NULL 
            AND related_companies != '[]'
            GROUP BY company
            ORDER BY avg_heat DESC
            LIMIT 20
            """
            
            cursor.execute(sql)
            results = cursor.fetchall()
            
            rankings = []
            for row in results:
                rankings.append({
                    'company': row[0] if row[0] else '未知公司',
                    'heat_score': round(float(row[1]), 1),
                    'count': row[2],
                    'trend': 'up' if float(row[1]) > 85 else 'stable',
                    'industry': '未知行业'  # 简化处理
                })
            
            cursor.close()
            return rankings
            
        except Exception as e:
            logger.error(f"获取公司热度排名失败: {e}")
            return []

    def get_trend_rankings(self) -> List[Dict[str, Any]]:
        """获取趋势热度排名"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # 从关键词中提取趋势信息并计算热度
            sql = """
            SELECT 
                JSON_UNQUOTE(JSON_EXTRACT(keywords, '$[*]')) as keyword,
                AVG(heat_score) as avg_heat,
                COUNT(*) as count
            FROM l1_domestic_hotspot_data 
            WHERE keywords IS NOT NULL 
            AND keywords != '[]'
            GROUP BY keyword
            ORDER BY avg_heat DESC
            LIMIT 20
            """
            
            cursor.execute(sql)
            results = cursor.fetchall()
            
            rankings = []
            for row in results:
                keyword = row[0] if row[0] else '未知趋势'
                rankings.append({
                    'trend': keyword,
                    'heat_score': round(float(row[1]), 1),
                    'count': row[2],
                    'category': self._categorize_trend(keyword)
                })
            
            cursor.close()
            return rankings
            
        except Exception as e:
            logger.error(f"获取趋势热度排名失败: {e}")
            return []

    def _categorize_trend(self, keyword: str) -> str:
        """对趋势关键词进行分类"""
        if any(word in keyword for word in ['转型', '升级', '制造', '产业']):
            return '产业趋势'
        elif any(word in keyword for word in ['数字', '智能', '科技', '创新']):
            return '技术趋势'
        elif any(word in keyword for word in ['绿色', '低碳', '环保', '政策']):
            return '政策趋势'
        elif any(word in keyword for word in ['消费', '市场', '经济']):
            return '市场趋势'
        elif any(word in keyword for word in ['发展', '增长', '改革']):
            return '发展趋势'
        else:
            return '其他趋势'


# 创建全局数据库管理器实例
db_manager = DatabaseManager() 