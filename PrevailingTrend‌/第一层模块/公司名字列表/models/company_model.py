"""
公司信息数据模型
定义公司基本信息的数据结构和数据库表结构
"""

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, field
from enum import Enum


class CompanyStatus(Enum):
    """公司状态枚举"""
    ACTIVE = "active"      # 正常交易
    SUSPENDED = "suspended"  # 暂停交易
    DELISTED = "delisted"  # 退市
    PENDING = "pending"    # 待上市


class MarketType(Enum):
    """市场类型枚举"""
    SH = "SH"  # 上海证券交易所
    SZ = "SZ"  # 深圳证券交易所
    HK = "HK"  # 香港交易所
    US = "US"  # 美国交易所


class CompanyType(Enum):
    """公司类型枚举"""
    MAIN_BOARD = "main_board"      # 主板
    SME_BOARD = "sme_board"        # 中小板
    GEM = "gem"                    # 创业板
    STAR = "star"                  # 科创板
    NEW_THIRD = "new_third"        # 新三板


@dataclass
class CompanyModel:
    """
    公司信息数据模型
    
    属性:
        company_name: 公司全称
        stock_code: 股票代码
        market: 交易市场
        short_name: 股票简称
        industry_code: 行业代码
        list_date: 上市日期
        status: 公司状态
        company_type: 公司类型
        area: 地区
        website: 公司官网
        business_scope: 经营范围
        market_cap: 市值
        employees: 员工数量
        update_date: 数据更新日期
        source: 数据来源标识
        created_at: 创建时间
        updated_at: 更新时间
    """
    
    # 核心字段
    company_name: str
    stock_code: str
    market: str
    
    # 基础信息字段
    short_name: Optional[str] = None
    industry_code: Optional[str] = None
    list_date: Optional[datetime] = None
    
    # 状态字段
    status: CompanyStatus = CompanyStatus.ACTIVE
    
    # 扩展信息字段
    company_type: Optional[CompanyType] = None
    area: Optional[str] = None
    website: Optional[str] = None
    business_scope: Optional[str] = None
    market_cap: Optional[float] = None
    employees: Optional[int] = None
    
    # 元数据字段
    update_date: Optional[datetime] = None
    source: str = "wind"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """数据验证和初始化"""
        # 验证股票代码格式
        if not self._validate_stock_code():
            raise ValueError(f"无效的股票代码格式: {self.stock_code}")
        
        # 验证市场类型
        if not self._validate_market():
            raise ValueError(f"无效的市场类型: {self.market}")
        
        # 验证公司名称
        if not self.company_name or len(self.company_name.strip()) == 0:
            raise ValueError("公司名称不能为空")
    
    def _validate_stock_code(self) -> bool:
        """验证股票代码格式"""
        if not self.stock_code:
            return False
        
        # A股代码格式：6位数字
        if self.market in ['SH', 'SZ'] and len(self.stock_code) == 6 and self.stock_code.isdigit():
            return True
        
        # 港股代码格式：4-5位数字
        if self.market == 'HK' and 4 <= len(self.stock_code) <= 5 and self.stock_code.isdigit():
            return True
        
        # 美股代码格式：字母数字组合
        if self.market == 'US' and len(self.stock_code) >= 1 and self.stock_code.isalnum():
            return True
        
        return False
    
    def _validate_market(self) -> bool:
        """验证市场类型"""
        valid_markets = ['SH', 'SZ', 'HK', 'US']
        return self.market in valid_markets
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "company_name": self.company_name,
            "stock_code": self.stock_code,
            "market": self.market,
            "short_name": self.short_name,
            "industry_code": self.industry_code,
            "list_date": self.list_date.isoformat() if self.list_date else None,
            "status": self.status.value,
            "company_type": self.company_type.value if self.company_type else None,
            "area": self.area,
            "website": self.website,
            "business_scope": self.business_scope,
            "market_cap": self.market_cap,
            "employees": self.employees,
            "update_date": self.update_date.isoformat() if self.update_date else None,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CompanyModel':
        """从字典创建实例"""
        # 处理枚举类型
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = CompanyStatus(data['status'])
        
        if 'company_type' in data and data['company_type'] and isinstance(data['company_type'], str):
            data['company_type'] = CompanyType(data['company_type'])
        
        # 处理日期字段
        for date_field in ['list_date', 'update_date', 'created_at', 'updated_at']:
            if date_field in data and data[date_field]:
                if isinstance(data[date_field], str):
                    data[date_field] = datetime.fromisoformat(data[date_field])
        
        return cls(**data)
    
    def is_active(self) -> bool:
        """判断是否为活跃状态"""
        return self.status == CompanyStatus.ACTIVE
    
    def is_suspended(self) -> bool:
        """判断是否为暂停状态"""
        return self.status == CompanyStatus.SUSPENDED
    
    def is_delisted(self) -> bool:
        """判断是否为退市状态"""
        return self.status == CompanyStatus.DELISTED
    
    def get_full_stock_code(self) -> str:
        """获取完整股票代码（包含市场前缀）"""
        return f"{self.market}.{self.stock_code}"
    
    def get_market_name(self) -> str:
        """获取市场名称"""
        market_names = {
            'SH': '上海证券交易所',
            'SZ': '深圳证券交易所',
            'HK': '香港交易所',
            'US': '美国交易所'
        }
        return market_names.get(self.market, self.market)
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.stock_code} - {self.company_name} ({self.market})"
    
    def __repr__(self) -> str:
        """详细字符串表示"""
        return (f"CompanyModel(company_name='{self.company_name}', "
                f"stock_code='{self.stock_code}', "
                f"market='{self.market}', "
                f"status={self.status.value})")


# 数据库表结构定义
COMPANY_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS company_list (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(200) NOT NULL COMMENT '公司全称',
    stock_code VARCHAR(20) NOT NULL COMMENT '股票代码',
    market VARCHAR(10) NOT NULL COMMENT '交易市场',
    short_name VARCHAR(100) COMMENT '股票简称',
    industry_code VARCHAR(20) COMMENT '行业代码',
    list_date DATE COMMENT '上市日期',
    status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '公司状态',
    company_type VARCHAR(20) COMMENT '公司类型',
    area VARCHAR(100) COMMENT '地区',
    website VARCHAR(500) COMMENT '公司官网',
    business_scope TEXT COMMENT '经营范围',
    market_cap DECIMAL(20,2) COMMENT '市值',
    employees INT COMMENT '员工数量',
    update_date DATETIME COMMENT '数据更新日期',
    source VARCHAR(50) NOT NULL DEFAULT 'wind' COMMENT '数据来源',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    UNIQUE KEY uk_stock_code_market (stock_code, market),
    KEY idx_company_name (company_name),
    KEY idx_market (market),
    KEY idx_industry_code (industry_code),
    KEY idx_status (status),
    KEY idx_company_type (company_type),
    KEY idx_list_date (list_date),
    KEY idx_source (source),
    KEY idx_update_date (update_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公司信息表';
""" 