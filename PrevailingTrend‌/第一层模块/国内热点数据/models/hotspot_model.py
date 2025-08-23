"""
国内热点数据模型
定义热点信息的数据结构和数据库表结构
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum


class HotspotType(Enum):
    """热点类型枚举"""
    NEWS = "news"              # 新闻热点
    POLICY = "policy"          # 政策热点
    MARKET = "market"          # 市场热点
    INDUSTRY = "industry"      # 行业热点
    COMPANY = "company"        # 公司热点
    ECONOMY = "economy"        # 经济热点


class HotspotLevel(Enum):
    """热点级别枚举"""
    LOW = "low"        # 低热度
    MEDIUM = "medium"  # 中等热度
    HIGH = "high"      # 高热度
    VERY_HIGH = "very_high"  # 极高热度


class HotspotStatus(Enum):
    """热点状态枚举"""
    ACTIVE = "active"      # 活跃
    DECLINING = "declining"  # 热度下降
    EXPIRED = "expired"    # 已过期


@dataclass
class HotspotModel:
    """
    热点数据模型
    
    属性:
        hotspot_id: 热点ID
        title: 热点标题
        content: 热点内容
        hotspot_type: 热点类型
        hotspot_level: 热点级别
        status: 热点状态
        source: 数据来源
        url: 原始链接
        publish_time: 发布时间
        keywords: 关键词列表
        related_companies: 相关公司列表
        related_industries: 相关行业列表
        sentiment_score: 情感得分
        heat_score: 热度得分
        update_date: 数据更新日期
        created_at: 创建时间
        updated_at: 更新时间
    """
    
    # 核心字段
    hotspot_id: str
    title: str
    content: str
    hotspot_type: HotspotType
    
    # 基础信息字段
    hotspot_level: HotspotLevel = HotspotLevel.MEDIUM
    status: HotspotStatus = HotspotStatus.ACTIVE
    source: str = ""
    url: Optional[str] = None
    publish_time: Optional[datetime] = None
    
    # 分析字段
    keywords: List[str] = field(default_factory=list)
    related_companies: List[str] = field(default_factory=list)
    related_industries: List[str] = field(default_factory=list)
    sentiment_score: Optional[float] = None  # -1到1之间
    heat_score: Optional[float] = None  # 0到100之间
    
    # 元数据字段
    update_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """数据验证和初始化"""
        # 验证热点ID
        if not self.hotspot_id or len(self.hotspot_id.strip()) == 0:
            raise ValueError("热点ID不能为空")
        
        # 验证标题
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("热点标题不能为空")
        
        # 验证内容
        if not self.content or len(self.content.strip()) == 0:
            raise ValueError("热点内容不能为空")
        
        # 验证情感得分范围
        if self.sentiment_score is not None and not -1 <= self.sentiment_score <= 1:
            raise ValueError("情感得分必须在-1到1之间")
        
        # 验证热度得分范围
        if self.heat_score is not None and not 0 <= self.heat_score <= 100:
            raise ValueError("热度得分必须在0到100之间")
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "hotspot_id": self.hotspot_id,
            "title": self.title,
            "content": self.content,
            "hotspot_type": self.hotspot_type.value,
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
    
    @classmethod
    def from_dict(cls, data: dict) -> 'HotspotModel':
        """从字典创建实例"""
        # 处理枚举类型
        if 'hotspot_type' in data and isinstance(data['hotspot_type'], str):
            data['hotspot_type'] = HotspotType(data['hotspot_type'])
        
        if 'hotspot_level' in data and isinstance(data['hotspot_level'], str):
            data['hotspot_level'] = HotspotLevel(data['hotspot_level'])
        
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = HotspotStatus(data['status'])
        
        # 处理日期字段
        for date_field in ['publish_time', 'update_date', 'created_at', 'updated_at']:
            if date_field in data and data[date_field]:
                if isinstance(data[date_field], str):
                    data[date_field] = datetime.fromisoformat(data[date_field])
        
        return cls(**data)
    
    def is_active(self) -> bool:
        """判断是否为活跃状态"""
        return self.status == HotspotStatus.ACTIVE
    
    def is_high_heat(self) -> bool:
        """判断是否为高热度"""
        return self.hotspot_level in [HotspotLevel.HIGH, HotspotLevel.VERY_HIGH]
    
    def is_positive_sentiment(self) -> bool:
        """判断是否为正面情感"""
        return self.sentiment_score is not None and self.sentiment_score > 0
    
    def is_negative_sentiment(self) -> bool:
        """判断是否为负面情感"""
        return self.sentiment_score is not None and self.sentiment_score < 0
    
    def get_sentiment_label(self) -> str:
        """获取情感标签"""
        if self.sentiment_score is None:
            return "中性"
        elif self.sentiment_score > 0.3:
            return "正面"
        elif self.sentiment_score < -0.3:
            return "负面"
        else:
            return "中性"
    
    def get_heat_label(self) -> str:
        """获取热度标签"""
        if self.heat_score is None:
            return "未知"
        elif self.heat_score >= 80:
            return "极高热度"
        elif self.heat_score >= 60:
            return "高热度"
        elif self.heat_score >= 40:
            return "中等热度"
        elif self.heat_score >= 20:
            return "低热度"
        else:
            return "极低热度"
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.hotspot_id} - {self.title} ({self.hotspot_type.value})"
    
    def __repr__(self) -> str:
        """详细字符串表示"""
        return (f"HotspotModel(hotspot_id='{self.hotspot_id}', "
                f"title='{self.title}', "
                f"hotspot_type={self.hotspot_type.value}, "
                f"hotspot_level={self.hotspot_level.value}, "
                f"status={self.status.value})")


# 数据库表结构定义
HOTSPOT_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS domestic_hotspot_data (
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