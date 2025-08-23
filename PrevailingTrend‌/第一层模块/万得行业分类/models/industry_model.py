"""
行业分类数据模型
定义行业分类的数据结构和数据库表结构
"""

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, field
from enum import Enum


class IndustryStatus(Enum):
    """行业状态枚举"""
    ACTIVE = "active"      # 有效
    INACTIVE = "inactive"  # 无效
    MERGED = "merged"      # 已合并
    SPLIT = "split"        # 已拆分


class IndustryLevel(Enum):
    """行业层级枚举"""
    LEVEL_1 = 1  # 一级行业
    LEVEL_2 = 2  # 二级行业
    LEVEL_3 = 3  # 三级行业


@dataclass
class IndustryModel:
    """
    行业分类数据模型
    
    属性:
        industry_code: 行业代码（万得标准）
        industry_name: 行业名称
        industry_level: 行业层级（1/2/3级）
        parent_code: 父级行业代码
        sw_code: 申万行业代码
        csrc_code: 证监会行业代码
        status: 行业状态
        industry_desc: 行业描述
        major_companies: 主要公司列表
        industry_keywords: 行业关键词
        market_cap_total: 行业总市值
        company_count: 行业公司数量
        update_date: 数据更新日期
        source: 数据来源标识
        created_at: 创建时间
        updated_at: 更新时间
    """
    
    # 核心字段
    industry_code: str
    industry_name: str
    industry_level: int
    
    # 关联字段
    parent_code: Optional[str] = None
    sw_code: Optional[str] = None
    csrc_code: Optional[str] = None
    
    # 状态字段
    status: IndustryStatus = IndustryStatus.ACTIVE
    
    # 描述字段
    industry_desc: Optional[str] = None
    major_companies: List[str] = field(default_factory=list)
    industry_keywords: List[str] = field(default_factory=list)
    
    # 统计字段
    market_cap_total: Optional[float] = None
    company_count: Optional[int] = None
    
    # 元数据字段
    update_date: Optional[datetime] = None
    source: str = "wind"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """数据验证和初始化"""
        # 验证行业代码格式
        if not self._validate_industry_code():
            raise ValueError(f"无效的行业代码格式: {self.industry_code}")
        
        # 验证行业层级
        if self.industry_level not in [1, 2, 3]:
            raise ValueError(f"无效的行业层级: {self.industry_level}")
        
        # 验证父级关系
        if self.industry_level > 1 and not self.parent_code:
            raise ValueError(f"二级和三级行业必须指定父级行业代码")
    
    def _validate_industry_code(self) -> bool:
        """验证行业代码格式"""
        if not self.industry_code:
            return False
        
        # 万得行业代码格式：6位数字
        if len(self.industry_code) == 6 and self.industry_code.isdigit():
            return True
        
        # 申万行业代码格式：6位数字
        if len(self.industry_code) == 6 and self.industry_code.isdigit():
            return True
        
        return False
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "industry_code": self.industry_code,
            "industry_name": self.industry_name,
            "industry_level": self.industry_level,
            "parent_code": self.parent_code,
            "sw_code": self.sw_code,
            "csrc_code": self.csrc_code,
            "status": self.status.value,
            "industry_desc": self.industry_desc,
            "major_companies": self.major_companies,
            "industry_keywords": self.industry_keywords,
            "market_cap_total": self.market_cap_total,
            "company_count": self.company_count,
            "update_date": self.update_date.isoformat() if self.update_date else None,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'IndustryModel':
        """从字典创建实例"""
        # 处理枚举类型
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = IndustryStatus(data['status'])
        
        # 处理日期字段
        for date_field in ['update_date', 'created_at', 'updated_at']:
            if date_field in data and data[date_field]:
                if isinstance(data[date_field], str):
                    data[date_field] = datetime.fromisoformat(data[date_field])
        
        return cls(**data)
    
    def is_parent_of(self, other: 'IndustryModel') -> bool:
        """判断是否为指定行业的父级行业"""
        return (self.industry_level == other.industry_level - 1 and 
                self.industry_code == other.parent_code)
    
    def is_child_of(self, other: 'IndustryModel') -> bool:
        """判断是否为指定行业的子级行业"""
        return (self.industry_level == other.industry_level + 1 and 
                other.industry_code == self.parent_code)
    
    def get_full_path(self, industry_map: dict) -> List[str]:
        """获取行业完整路径"""
        path = [self.industry_name]
        current = self
        
        while current.parent_code and current.parent_code in industry_map:
            current = industry_map[current.parent_code]
            path.insert(0, current.industry_name)
        
        return path
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.industry_code} - {self.industry_name} (L{self.industry_level})"
    
    def __repr__(self) -> str:
        """详细字符串表示"""
        return (f"IndustryModel(industry_code='{self.industry_code}', "
                f"industry_name='{self.industry_name}', "
                f"industry_level={self.industry_level}, "
                f"parent_code='{self.parent_code}', "
                f"status={self.status.value})")


# 数据库表结构定义
INDUSTRY_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS wind_industry_classification (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    industry_code VARCHAR(20) NOT NULL COMMENT '行业代码',
    industry_name VARCHAR(100) NOT NULL COMMENT '行业名称',
    industry_level TINYINT NOT NULL COMMENT '行业层级(1/2/3)',
    parent_code VARCHAR(20) COMMENT '父级行业代码',
    sw_code VARCHAR(20) COMMENT '申万行业代码',
    csrc_code VARCHAR(20) COMMENT '证监会行业代码',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '行业状态',
    industry_desc TEXT COMMENT '行业描述',
    major_companies JSON COMMENT '主要公司列表',
    industry_keywords JSON COMMENT '行业关键词',
    market_cap_total DECIMAL(20,2) COMMENT '行业总市值',
    company_count INT COMMENT '行业公司数量',
    update_date DATETIME COMMENT '数据更新日期',
    source VARCHAR(50) NOT NULL DEFAULT 'wind' COMMENT '数据来源',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    UNIQUE KEY uk_industry_code_level (industry_code, industry_level),
    KEY idx_parent_code (parent_code),
    KEY idx_industry_level (industry_level),
    KEY idx_status (status),
    KEY idx_source (source),
    KEY idx_update_date (update_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='万得行业分类表';
""" 