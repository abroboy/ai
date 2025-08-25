# -*- coding: utf-8 -*-
"""
资金流向趋势分析数据模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FlowTrend(Base):
    """资金流向趋势分析表"""
    __tablename__ = 'flow_trends'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    analysis_period = Column(String(20), nullable=False, index=True)  # 分析周期：daily, weekly, monthly
    asset_type = Column(String(50), nullable=False, index=True)      # 资产类型
    symbol = Column(String(50), nullable=False, index=True)          # 资产代码
    
    # 趋势指标
    trend_direction = Column(String(20), nullable=True)   # 趋势方向：up, down, sideways
    trend_strength = Column(Float, nullable=True)         # 趋势强度（0-1）
    trend_duration = Column(Integer, nullable=True)       # 趋势持续时间（天数）
    
    # 技术指标
    moving_average_5 = Column(Float, nullable=True)       # 5日均线
    moving_average_10 = Column(Float, nullable=True)      # 10日均线
    moving_average_20 = Column(Float, nullable=True)      # 20日均线
    moving_average_50 = Column(Float, nullable=True)      # 50日均线
    
    # 动量指标
    rsi = Column(Float, nullable=True)                    # RSI指标
    macd = Column(Float, nullable=True)                   # MACD指标
    macd_signal = Column(Float, nullable=True)            # MACD信号线
    macd_histogram = Column(Float, nullable=True)         # MACD柱状图
    
    # 布林带指标
    bollinger_upper = Column(Float, nullable=True)        # 布林带上轨
    bollinger_middle = Column(Float, nullable=True)       # 布林带中轨
    bollinger_lower = Column(Float, nullable=True)        # 布林带下轨
    
    # 成交量指标
    volume_ma = Column(Float, nullable=True)              # 成交量均线
    volume_ratio = Column(Float, nullable=True)           # 成交量比率
    
    # 趋势信号
    buy_signal = Column(Boolean, nullable=True)           # 买入信号
    sell_signal = Column(Boolean, nullable=True)          # 卖出信号
    hold_signal = Column(Boolean, nullable=True)          # 持有信号
    
    # 置信度
    confidence_level = Column(Float, nullable=True)       # 信号置信度（0-1）
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 索引
    __table_args__ = (
        Index('idx_timestamp_symbol', 'timestamp', 'symbol'),
        Index('idx_trend_direction', 'trend_direction', 'trend_strength'),
        Index('idx_signal_confidence', 'buy_signal', 'sell_signal', 'confidence_level'),
    )

class MarketTrend(Base):
    """市场整体趋势分析表"""
    __tablename__ = 'market_trends'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    market_type = Column(String(50), nullable=False, index=True)  # 市场类型
    analysis_period = Column(String(20), nullable=False, index=True)  # 分析周期
    
    # 市场趋势
    market_trend = Column(String(20), nullable=True)      # 市场趋势：bull, bear, neutral
    trend_strength = Column(Float, nullable=True)         # 趋势强度
    trend_confidence = Column(Float, nullable=True)       # 趋势置信度
    
    # 市场广度指标
    advancing_stocks = Column(Integer, nullable=True)     # 上涨股票数量
    declining_stocks = Column(Integer, nullable=True)     # 下跌股票数量
    unchanged_stocks = Column(Integer, nullable=True)     # 平盘股票数量
    advance_decline_ratio = Column(Float, nullable=True)  # 涨跌比
    
    # 市场情绪指标
    fear_greed_index = Column(Float, nullable=True)       # 恐慌贪婪指数
    volatility_index = Column(Float, nullable=True)       # 波动率指数
    put_call_ratio = Column(Float, nullable=True)         # 看跌看涨比率
    
    # 资金流向趋势
    institutional_flow = Column(Float, nullable=True)     # 机构资金流向
    retail_flow = Column(Float, nullable=True)            # 散户资金流向
    foreign_flow = Column(Float, nullable=True)           # 外资流向
    
    # 行业轮动
    leading_sectors = Column(Text, nullable=True)         # 领涨行业（JSON格式）
    lagging_sectors = Column(Text, nullable=True)         # 领跌行业（JSON格式）
    
    # 风险指标
    market_risk_level = Column(String(20), nullable=True) # 市场风险等级
    correlation_matrix = Column(Text, nullable=True)      # 相关性矩阵（JSON格式）
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 索引
    __table_args__ = (
        Index('idx_timestamp_market', 'timestamp', 'market_type'),
        Index('idx_market_trend', 'market_type', 'market_trend'),
        Index('idx_risk_level', 'market_risk_level', 'trend_strength'),
    )

class AssetTrend(Base):
    """资产类别趋势分析表"""
    __tablename__ = 'asset_trends'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    asset_category = Column(String(50), nullable=False, index=True)  # 资产类别
    analysis_period = Column(String(20), nullable=False, index=True)  # 分析周期
    
    # 资产类别趋势
    category_trend = Column(String(20), nullable=True)    # 类别趋势
    trend_strength = Column(Float, nullable=True)         # 趋势强度
    momentum_score = Column(Float, nullable=True)         # 动量得分
    
    # 相对表现
    relative_performance = Column(Float, nullable=True)   # 相对表现
    alpha = Column(Float, nullable=True)                  # Alpha值
    beta = Column(Float, nullable=True)                   # Beta值
    
    # 风险调整收益
    sharpe_ratio = Column(Float, nullable=True)           # 夏普比率
    sortino_ratio = Column(Float, nullable=True)          # 索提诺比率
    calmar_ratio = Column(Float, nullable=True)           # 卡玛比率
    
    # 资金流向分析
    flow_momentum = Column(Float, nullable=True)          # 流向动量
    flow_acceleration = Column(Float, nullable=True)      # 流向加速度
    flow_divergence = Column(Float, nullable=True)        # 流向背离
    
    # 相关性分析
    correlation_with_market = Column(Float, nullable=True)  # 与市场相关性
    correlation_with_other_assets = Column(Text, nullable=True)  # 与其他资产相关性（JSON格式）
    
    # 预测指标
    forecast_direction = Column(String(20), nullable=True)  # 预测方向
    forecast_probability = Column(Float, nullable=True)     # 预测概率
    forecast_horizon = Column(Integer, nullable=True)       # 预测时间范围（天）
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 索引
    __table_args__ = (
        Index('idx_timestamp_category', 'timestamp', 'asset_category'),
        Index('idx_category_trend', 'asset_category', 'category_trend'),
        Index('idx_forecast', 'forecast_direction', 'forecast_probability'),
    ) 