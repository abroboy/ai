# -*- coding: utf-8 -*-
"""
公司数据结构定义 - 基于AKShare字段结构
"""

from __future__ import annotations
from typing import Dict, Any, Optional

class StockCompany:
    """股票公司数据结构，基于AKShare的字段"""
    
    def __init__(self, data: Dict[str, Any]):
        self.code = data.get("code", "")
        self.name = data.get("name", "")
        self.latest_price = data.get("latest_price", 0.0)
        self.change_percent = data.get("change_percent", 0.0)
        self.change_amount = data.get("change_amount", 0.0)
        self.volume = data.get("volume", 0)
        self.turnover = data.get("turnover", 0.0)
        self.amplitude = data.get("amplitude", 0.0)
        self.highest = data.get("highest", 0.0)
        self.lowest = data.get("lowest", 0.0)
        self.open_price = data.get("open_price", 0.0)
        self.prev_close = data.get("prev_close", 0.0)
        self.volume_ratio = data.get("volume_ratio", 0.0)
        self.turnover_rate = data.get("turnover_rate", 0.0)
        self.pe_ratio = data.get("pe_ratio", 0.0)
        self.pb_ratio = data.get("pb_ratio", 0.0)
        self.total_market_value = data.get("total_market_value", 0.0)
        self.circulating_market_value = data.get("circulating_market_value", 0.0)
        self.industry = data.get("industry", "未知")
        self.heat_score = data.get("heat_score", 0.0)
        self.sentiment = data.get("sentiment", "中性")
        self.update_time = data.get("update_time", "")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "code": self.code,
            "name": self.name,
            "latest_price": self.latest_price,
            "change_percent": self.change_percent,
            "change_amount": self.change_amount,
            "volume": self.volume,
            "turnover": self.turnover,
            "amplitude": self.amplitude,
            "highest": self.highest,
            "lowest": self.lowest,
            "open_price": self.open_price,
            "prev_close": self.prev_close,
            "volume_ratio": self.volume_ratio,
            "turnover_rate": self.turnover_rate,
            "pe_ratio": self.pe_ratio,
            "pb_ratio": self.pb_ratio,
            "total_market_value": self.total_market_value,
            "circulating_market_value": self.circulating_market_value,
            "industry": self.industry,
            "heat_score": self.heat_score,
            "sentiment": self.sentiment,
            "update_time": self.update_time
        }
    
    def to_api_format(self) -> Dict[str, Any]:
        """转换为API响应格式"""
        return {
            "stockCode": self.code,
            "stockName": self.name,
            "latestPrice": self.latest_price,
            "priceChangeRate": self.change_percent,
            "totalMarketValue": self.total_market_value,
            "industry": self.industry,
            "heatScore": self.heat_score,
            "sentiment": self.sentiment,
            "peRatio": str(self.pe_ratio),
            "pbRatio": str(self.pb_ratio),
        }

def create_company_from_akshare_data(akshare_data: Dict[str, Any]) -> StockCompany:
    """从AKShare数据创建公司对象"""
    return StockCompany(akshare_data)