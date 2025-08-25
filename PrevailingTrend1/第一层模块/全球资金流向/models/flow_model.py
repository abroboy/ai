# -*- coding: utf-8 -*-
"""
全球资金流向数据模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GlobalFlowData(Base):
    """全球资金流向数据表"""
    __tablename__ = 'global_flow_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    asset_type = Column(String(50), nullable=False, index=True)  # 资产类型：forex, stock, bond, commodity
    asset_name = Column(String(100), nullable=False, index=True)  # 资产名称
    symbol = Column(String(50), nullable=False, index=True)      # 资产代码
    
    # 价格数据
    open_price = Column(Float, nullable=True)
    high_price = Column(Float, nullable=True)
    low_price = Column(Float, nullable=True)
    close_price = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    
    # 资金流向指标
    net_flow = Column(Float, nullable=True)           # 净流入（正值为流入，负值为流出）
    flow_ratio = Column(Float, nullable=True)         # 资金流向比率
    relative_strength = Column(Float, nullable=True)  # 相对强度
    momentum = Column(Float, nullable=True)           # 动量指标
    volatility = Column(Float, nullable=True)         # 波动率
    
    # 市场情绪指标
    fear_greed_index = Column(Float, nullable=True)   # 恐慌贪婪指数
    market_sentiment = Column(String(20), nullable=True)  # 市场情绪：bullish, bearish, neutral
    
    # 元数据
    data_source = Column(String(50), nullable=False)  # 数据源
    region = Column(String(50), nullable=True)        # 地区
    sector = Column(String(100), nullable=True)       # 行业/板块
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 索引
    __table_args__ = (
        Index('idx_timestamp_asset', 'timestamp', 'asset_type'),
        Index('idx_symbol_timestamp', 'symbol', 'timestamp'),
        Index('idx_region_sector', 'region', 'sector'),
    )

class MarketFlowData(Base):
    """市场资金流向汇总数据表"""
    __tablename__ = 'market_flow_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    market_type = Column(String(50), nullable=False, index=True)  # 市场类型：us, europe, asia, global
    market_name = Column(String(100), nullable=False, index=True)  # 市场名称
    
    # 市场整体资金流向
    total_net_flow = Column(Float, nullable=True)     # 总净流入
    total_volume = Column(Float, nullable=True)       # 总成交量
    avg_flow_ratio = Column(Float, nullable=True)     # 平均资金流向比率
    
    # 市场分类资金流向
    stock_flow = Column(Float, nullable=True)         # 股票市场资金流向
    bond_flow = Column(Float, nullable=True)          # 债券市场资金流向
    forex_flow = Column(Float, nullable=True)         # 外汇市场资金流向
    commodity_flow = Column(Float, nullable=True)     # 大宗商品资金流向
    
    # 市场情绪
    market_sentiment = Column(String(20), nullable=True)  # 市场情绪
    risk_level = Column(String(20), nullable=True)        # 风险等级：low, medium, high
    
    # 趋势指标
    trend_direction = Column(String(20), nullable=True)   # 趋势方向：up, down, sideways
    trend_strength = Column(Float, nullable=True)         # 趋势强度
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 索引
    __table_args__ = (
        Index('idx_timestamp_market', 'timestamp', 'market_type'),
        Index('idx_market_sentiment', 'market_type', 'market_sentiment'),
    )

class AssetFlowData(Base):
    """资产类别资金流向数据表"""
    __tablename__ = 'asset_flow_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    asset_category = Column(String(50), nullable=False, index=True)  # 资产类别：equity, fixed_income, currency, commodity
    category_name = Column(String(100), nullable=False, index=True)  # 类别名称
    
    # 资金流向统计
    total_inflow = Column(Float, nullable=True)       # 总流入
    total_outflow = Column(Float, nullable=True)      # 总流出
    net_flow = Column(Float, nullable=True)           # 净流入
    flow_volume = Column(Float, nullable=True)        # 流向成交量
    
    # 相对指标
    flow_ratio = Column(Float, nullable=True)         # 资金流向比率
    market_share = Column(Float, nullable=True)       # 市场份额
    relative_performance = Column(Float, nullable=True)  # 相对表现
    
    # 风险指标
    volatility = Column(Float, nullable=True)         # 波动率
    sharpe_ratio = Column(Float, nullable=True)       # 夏普比率
    max_drawdown = Column(Float, nullable=True)       # 最大回撤
    
    # 趋势分析
    short_term_trend = Column(String(20), nullable=True)  # 短期趋势
    medium_term_trend = Column(String(20), nullable=True) # 中期趋势
    long_term_trend = Column(String(20), nullable=True)   # 长期趋势
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 索引
    __table_args__ = (
        Index('idx_timestamp_category', 'timestamp', 'asset_category'),
        Index('idx_category_trend', 'asset_category', 'short_term_trend'),
    ) 