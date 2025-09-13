"""
国外热点数据模型
"""

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, field
from enum import Enum


class HotspotType(Enum):
    """热点类型枚举"""
    NEWS = "news"
    POLICY = "policy"
    MARKET = "market"
    ECONOMY = "economy"
    RESEARCH = "research"


class HotspotLevel(Enum):
    """热点级别枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class HotspotStatus(Enum):
    """热点状态枚举"""
    ACTIVE = "active"
    DECLINING = "declining"
    EXPIRED = "expired"


class Region(Enum):
    """地区枚举"""
    GLOBAL = "global"
    US = "us"
    EU = "eu"
    UK = "uk"
    ASIA = "asia"
    JAPAN = "japan"
    AUSTRALIA = "australia"


@dataclass
class InternationalHotspotModel:
    """国外热点数据模型"""
    
    hotspot_id: str
    title: str
    content: str
    hotspot_type: HotspotType
    region: Region
    
    hotspot_level: HotspotLevel = HotspotLevel.MEDIUM
    status: HotspotStatus = HotspotStatus.ACTIVE
    source: str = ""
    url: Optional[str] = None
    publish_time: Optional[datetime] = None
    
    keywords: List[str] = field(default_factory=list)
    related_companies: List[str] = field(default_factory=list)
    related_industries: List[str] = field(default_factory=list)
    sentiment_score: Optional[float] = None
    heat_score: Optional[float] = None
    
    update_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "hotspot_id": self.hotspot_id,
            "title": self.title,
            "content": self.content,
            "hotspot_type": self.hotspot_type.value,
            "region": self.region.value,
            "hotspot_level": self.hotspot_level.value,
            "status": self.status.value,
            "source": self.source,
            "url": self.url,
            "publish_time": self.publish_time.isoformat() if self.publish_time else None,
            "keywords": self.keywords,
            "related_companies": self.related_companies,
            "related_industries": self.related_industries,
            "sentiment_score": self.sentiment_score,
            "heat_score": self.heat_score,
            "update_date": self.update_date.isoformat() if self.update_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


# 数据库表结构定义
INTERNATIONAL_HOTSPOT_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS international_hotspot_data (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    hotspot_id VARCHAR(100) NOT NULL COMMENT '热点ID',
    title VARCHAR(500) NOT NULL COMMENT '热点标题',
    content TEXT NOT NULL COMMENT '热点内容',
    hotspot_type VARCHAR(20) NOT NULL COMMENT '热点类型',
    region VARCHAR(20) NOT NULL COMMENT '地区',
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
    KEY idx_region (region),
    KEY idx_hotspot_level (hotspot_level),
    KEY idx_status (status),
    KEY idx_source (source),
    KEY idx_publish_time (publish_time),
    KEY idx_sentiment_score (sentiment_score),
    KEY idx_heat_score (heat_score),
    KEY idx_update_date (update_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='国外热点数据表';
""" 