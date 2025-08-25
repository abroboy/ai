"""
股票行业映射数据模型
定义股票与行业的关联关系数据结构
"""

from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum


class MappingStatus(Enum):
    """映射状态枚举"""
    ACTIVE = "active"      # 有效
    INACTIVE = "inactive"  # 无效
    PENDING = "pending"    # 待确认


@dataclass
class StockIndustryModel:
    """
    股票行业映射数据模型
    
    属性:
        stock_code: 股票代码
        stock_name: 股票名称
        industry_code: 行业代码
        industry_name: 行业名称
        industry_level: 行业层级
        mapping_date: 映射日期
        status: 映射状态
        confidence: 映射置信度
        source: 数据来源
        created_at: 创建时间
        updated_at: 更新时间
    """
    
    # 核心字段
    stock_code: str
    stock_name: str
    industry_code: str
    industry_name: str
    industry_level: int
    
    # 状态字段
    mapping_date: Optional[datetime] = None
    status: MappingStatus = MappingStatus.ACTIVE
    confidence: float = 1.0  # 映射置信度 0-1
    
    # 元数据字段
    source: str = "wind"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """数据验证和初始化"""
        # 验证股票代码格式
        if not self._validate_stock_code():
            raise ValueError(f"无效的股票代码格式: {self.stock_code}")
        
        # 验证行业代码格式
        if not self._validate_industry_code():
            raise ValueError(f"无效的行业代码格式: {self.industry_code}")
        
        # 验证行业层级
        if self.industry_level not in [1, 2, 3]:
            raise ValueError(f"无效的行业层级: {self.industry_level}")
        
        # 验证置信度
        if not 0 <= self.confidence <= 1:
            raise ValueError(f"置信度必须在0-1之间: {self.confidence}")
    
    def _validate_stock_code(self) -> bool:
        """验证股票代码格式"""
        if not self.stock_code:
            return False
        
        # A股代码格式：6位数字
        if len(self.stock_code) == 6 and self.stock_code.isdigit():
            return True
        
        # 港股代码格式：4-5位数字
        if 4 <= len(self.stock_code) <= 5 and self.stock_code.isdigit():
            return True
        
        # 美股代码格式：字母数字组合
        if len(self.stock_code) >= 1 and self.stock_code.isalnum():
            return True
        
        return False
    
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
            "stock_code": self.stock_code,
            "stock_name": self.stock_name,
            "industry_code": self.industry_code,
            "industry_name": self.industry_name,
            "industry_level": self.industry_level,
            "mapping_date": self.mapping_date.isoformat() if self.mapping_date else None,
            "status": self.status.value,
            "confidence": self.confidence,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'StockIndustryModel':
        """从字典创建实例"""
        # 处理枚举类型
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = MappingStatus(data['status'])
        
        # 处理日期字段
        for date_field in ['mapping_date', 'created_at', 'updated_at']:
            if date_field in data and data[date_field]:
                if isinstance(data[date_field], str):
                    data[date_field] = datetime.fromisoformat(data[date_field])
        
        return cls(**data)
    
    def is_high_confidence(self) -> bool:
        """判断是否为高置信度映射"""
        return self.confidence >= 0.8
    
    def is_low_confidence(self) -> bool:
        """判断是否为低置信度映射"""
        return self.confidence < 0.5
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.stock_code} -> {self.industry_code} (置信度: {self.confidence:.2f})"
    
    def __repr__(self) -> str:
        """详细字符串表示"""
        return (f"StockIndustryModel(stock_code='{self.stock_code}', "
                f"stock_name='{self.stock_name}', "
                f"industry_code='{self.industry_code}', "
                f"industry_name='{self.industry_name}', "
                f"industry_level={self.industry_level}, "
                f"status={self.status.value}, "
                f"confidence={self.confidence})")


# 数据库表结构定义
STOCK_INDUSTRY_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS stock_industry_mapping (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    stock_code VARCHAR(20) NOT NULL COMMENT '股票代码',
    stock_name VARCHAR(100) NOT NULL COMMENT '股票名称',
    industry_code VARCHAR(20) NOT NULL COMMENT '行业代码',
    industry_name VARCHAR(100) NOT NULL COMMENT '行业名称',
    industry_level TINYINT NOT NULL COMMENT '行业层级(1/2/3)',
    mapping_date DATETIME COMMENT '映射日期',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '映射状态',
    confidence DECIMAL(3,2) NOT NULL DEFAULT 1.00 COMMENT '映射置信度',
    source VARCHAR(50) NOT NULL DEFAULT 'wind' COMMENT '数据来源',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    UNIQUE KEY uk_stock_industry (stock_code, industry_code, industry_level),
    KEY idx_stock_code (stock_code),
    KEY idx_industry_code (industry_code),
    KEY idx_industry_level (industry_level),
    KEY idx_status (status),
    KEY idx_confidence (confidence),
    KEY idx_source (source),
    KEY idx_mapping_date (mapping_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票行业映射表';
""" 