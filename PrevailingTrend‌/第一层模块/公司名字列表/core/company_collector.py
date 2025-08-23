"""
公司信息采集器
负责从各种数据源收集公司基本信息
"""

import asyncio
import aiohttp
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd

from ..models.company_model import CompanyModel, CompanyStatus, MarketType, CompanyType
from ..utils.logger import logger


class CompanyCollector:
    """公司信息采集器"""
    
    def __init__(self):
        """初始化采集器"""
        self.session = None
        self.logger = logger
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    def collect_from_sse(self) -> List[CompanyModel]:
        """从上交所采集公司信息"""
        try:
            self.logger.info("开始从上交所采集公司信息")
            
            # 模拟数据 - 实际项目中需要调用上交所API
            companies = [
                CompanyModel(
                    company_name="中国石油天然气股份有限公司",
                    stock_code="601857",
                    market="SH",
                    short_name="中国石油",
                    company_type=CompanyType.MAIN_BOARD,
                    list_date=datetime(2007, 11, 5),
                    status=CompanyStatus.ACTIVE,
                    area="北京",
                    source="sse"
                ),
                CompanyModel(
                    company_name="中国工商银行股份有限公司",
                    stock_code="601398",
                    market="SH",
                    short_name="工商银行",
                    company_type=CompanyType.MAIN_BOARD,
                    list_date=datetime(2006, 10, 27),
                    status=CompanyStatus.ACTIVE,
                    area="北京",
                    source="sse"
                )
            ]
            
            self.logger.info(f"从上交所采集到 {len(companies)} 家公司信息")
            return companies
            
        except Exception as e:
            self.logger.error(f"从上交所采集数据失败: {e}")
            return []
    
    def collect_from_szse(self) -> List[CompanyModel]:
        """从深交所采集公司信息"""
        try:
            self.logger.info("开始从深交所采集公司信息")
            
            # 模拟数据 - 实际项目中需要调用深交所API
            companies = [
                CompanyModel(
                    company_name="平安银行股份有限公司",
                    stock_code="000001",
                    market="SZ",
                    short_name="平安银行",
                    company_type=CompanyType.MAIN_BOARD,
                    list_date=datetime(1991, 4, 3),
                    status=CompanyStatus.ACTIVE,
                    area="深圳",
                    source="szse"
                ),
                CompanyModel(
                    company_name="万科企业股份有限公司",
                    stock_code="000002",
                    market="SZ",
                    short_name="万科A",
                    company_type=CompanyType.MAIN_BOARD,
                    list_date=datetime(1991, 1, 29),
                    status=CompanyStatus.ACTIVE,
                    area="深圳",
                    source="szse"
                )
            ]
            
            self.logger.info(f"从深交所采集到 {len(companies)} 家公司信息")
            return companies
            
        except Exception as e:
            self.logger.error(f"从深交所采集数据失败: {e}")
            return []
    
    def collect_from_hkex(self) -> List[CompanyModel]:
        """从港交所采集公司信息"""
        try:
            self.logger.info("开始从港交所采集公司信息")
            
            # 模拟数据 - 实际项目中需要调用港交所API
            companies = [
                CompanyModel(
                    company_name="腾讯控股有限公司",
                    stock_code="00700",
                    market="HK",
                    short_name="腾讯控股",
                    company_type=CompanyType.MAIN_BOARD,
                    list_date=datetime(2004, 6, 16),
                    status=CompanyStatus.ACTIVE,
                    area="香港",
                    source="hkex"
                ),
                CompanyModel(
                    company_name="阿里巴巴集团控股有限公司",
                    stock_code="09988",
                    market="HK",
                    short_name="阿里巴巴-SW",
                    company_type=CompanyType.MAIN_BOARD,
                    list_date=datetime(2019, 11, 26),
                    status=CompanyStatus.ACTIVE,
                    area="香港",
                    source="hkex"
                )
            ]
            
            self.logger.info(f"从港交所采集到 {len(companies)} 家公司信息")
            return companies
            
        except Exception as e:
            self.logger.error(f"从港交所采集数据失败: {e}")
            return []
    
    def collect_from_tushare(self) -> List[CompanyModel]:
        """从Tushare采集公司信息"""
        try:
            self.logger.info("开始从Tushare采集公司信息")
            
            # 模拟数据 - 实际项目中需要调用Tushare API
            companies = [
                CompanyModel(
                    company_name="贵州茅台酒股份有限公司",
                    stock_code="600519",
                    market="SH",
                    short_name="贵州茅台",
                    company_type=CompanyType.MAIN_BOARD,
                    list_date=datetime(2001, 8, 27),
                    status=CompanyStatus.ACTIVE,
                    area="贵州",
                    source="tushare"
                )
            ]
            
            self.logger.info(f"从Tushare采集到 {len(companies)} 家公司信息")
            return companies
            
        except Exception as e:
            self.logger.error(f"从Tushare采集数据失败: {e}")
            return []
    
    def collect_from_akshare(self) -> List[CompanyModel]:
        """从AKShare采集公司信息"""
        try:
            self.logger.info("开始从AKShare采集公司信息")
            
            # 模拟数据 - 实际项目中需要调用AKShare API
            companies = [
                CompanyModel(
                    company_name="比亚迪股份有限公司",
                    stock_code="002594",
                    market="SZ",
                    short_name="比亚迪",
                    company_type=CompanyType.SME_BOARD,
                    list_date=datetime(2011, 6, 30),
                    status=CompanyStatus.ACTIVE,
                    area="深圳",
                    source="akshare"
                )
            ]
            
            self.logger.info(f"从AKShare采集到 {len(companies)} 家公司信息")
            return companies
            
        except Exception as e:
            self.logger.error(f"从AKShare采集数据失败: {e}")
            return []
    
    def collect_all(self) -> List[CompanyModel]:
        """采集所有数据源的公司信息"""
        try:
            self.logger.info("开始采集所有数据源的公司信息")
            
            all_companies = []
            
            # 采集各个数据源
            all_companies.extend(self.collect_from_sse())
            all_companies.extend(self.collect_from_szse())
            all_companies.extend(self.collect_from_hkex())
            all_companies.extend(self.collect_from_tushare())
            all_companies.extend(self.collect_from_akshare())
            
            # 去重处理
            unique_companies = self._deduplicate_companies(all_companies)
            
            self.logger.info(f"总共采集到 {len(unique_companies)} 家唯一公司信息")
            return unique_companies
            
        except Exception as e:
            self.logger.error(f"采集所有数据源失败: {e}")
            return []
    
    def _deduplicate_companies(self, companies: List[CompanyModel]) -> List[CompanyModel]:
        """去重处理公司信息"""
        try:
            # 使用股票代码+市场作为唯一标识
            unique_dict = {}
            
            for company in companies:
                key = f"{company.stock_code}_{company.market}"
                if key not in unique_dict:
                    unique_dict[key] = company
                else:
                    # 如果已存在，选择更完整的信息
                    existing = unique_dict[key]
                    if len(company.company_name) > len(existing.company_name):
                        unique_dict[key] = company
            
            return list(unique_dict.values())
            
        except Exception as e:
            self.logger.error(f"去重处理失败: {e}")
            return companies
    
    def collect_by_market(self, market: str) -> List[CompanyModel]:
        """按市场采集公司信息"""
        try:
            self.logger.info(f"开始采集 {market} 市场的公司信息")
            
            if market == "SH":
                return self.collect_from_sse()
            elif market == "SZ":
                return self.collect_from_szse()
            elif market == "HK":
                return self.collect_from_hkex()
            else:
                self.logger.warning(f"不支持的市场类型: {market}")
                return []
                
        except Exception as e:
            self.logger.error(f"按市场采集数据失败: {e}")
            return []
    
    def collect_by_company_type(self, company_type: CompanyType) -> List[CompanyModel]:
        """按公司类型采集公司信息"""
        try:
            self.logger.info(f"开始采集 {company_type.value} 类型的公司信息")
            
            all_companies = self.collect_all()
            filtered_companies = [
                company for company in all_companies 
                if company.company_type == company_type
            ]
            
            self.logger.info(f"采集到 {len(filtered_companies)} 家 {company_type.value} 类型公司")
            return filtered_companies
            
        except Exception as e:
            self.logger.error(f"按公司类型采集数据失败: {e}")
            return [] 