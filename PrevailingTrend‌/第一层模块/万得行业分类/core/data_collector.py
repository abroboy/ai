"""
数据采集器
负责从万得Wind、Tushare、AKShare等数据源获取行业分类数据
"""

import time
import requests
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

from ..models.industry_model import IndustryModel, IndustryStatus
from ..models.stock_industry_model import StockIndustryModel, MappingStatus
from ..utils.logger import logger
from ..config import config


class BaseDataCollector(ABC):
    """数据采集器基类"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    @abstractmethod
    def collect_industry_data(self) -> List[IndustryModel]:
        """采集行业分类数据"""
        pass
    
    @abstractmethod
    def collect_stock_industry_mapping(self) -> List[StockIndustryModel]:
        """采集股票行业映射数据"""
        pass
    
    def _make_request(self, url: str, params: Optional[Dict] = None, 
                     timeout: int = 30, retries: int = 3) -> Optional[Dict]:
        """发送HTTP请求"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, params=params, timeout=timeout)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                logger.warning(f"请求失败 (尝试 {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    logger.error(f"请求最终失败: {url}")
                    return None


class WindDataCollector(BaseDataCollector):
    """万得Wind数据采集器"""
    
    def __init__(self):
        super().__init__()
        self.wind_config = config.wind
        
        # 尝试导入WindPy
        try:
            import WindPy as w
            self.wind = w
            self.wind.start()
            logger.info("万得Wind连接成功")
        except ImportError:
            logger.warning("WindPy未安装，将使用模拟数据")
            self.wind = None
    
    def collect_industry_data(self) -> List[IndustryModel]:
        """采集万得行业分类数据"""
        if not self.wind:
            return self._get_mock_industry_data()
        
        try:
            # 获取万得行业分类数据
            wind_data = self.wind.wss("", "industry_sw", "industryType=1")
            
            industries = []
            for i, code in enumerate(wind_data.Data[0]):
                name = wind_data.Data[1][i] if i < len(wind_data.Data[1]) else ""
                
                industry = IndustryModel(
                    industry_code=str(code),
                    industry_name=str(name),
                    industry_level=1,
                    source="wind",
                    update_date=datetime.now()
                )
                industries.append(industry)
            
            logger.info(f"成功采集万得行业数据: {len(industries)}条")
            return industries
            
        except Exception as e:
            logger.error(f"万得数据采集失败: {e}")
            return self._get_mock_industry_data()
    
    def collect_stock_industry_mapping(self) -> List[StockIndustryModel]:
        """采集股票行业映射数据"""
        if not self.wind:
            return self._get_mock_stock_mapping_data()
        
        try:
            # 获取股票行业映射数据
            wind_data = self.wind.wss("", "industry_sw,sec_name", "industryType=1")
            
            mappings = []
            for i, stock_code in enumerate(wind_data.Data[0]):
                industry_code = wind_data.Data[1][i] if i < len(wind_data.Data[1]) else ""
                stock_name = wind_data.Data[2][i] if i < len(wind_data.Data[2]) else ""
                
                mapping = StockIndustryModel(
                    stock_code=str(stock_code),
                    stock_name=str(stock_name),
                    industry_code=str(industry_code),
                    industry_name="",  # 需要单独获取
                    industry_level=1,
                    source="wind",
                    mapping_date=datetime.now()
                )
                mappings.append(mapping)
            
            logger.info(f"成功采集万得股票映射数据: {len(mappings)}条")
            return mappings
            
        except Exception as e:
            logger.error(f"万得股票映射数据采集失败: {e}")
            return self._get_mock_stock_mapping_data()
    
    def _get_mock_industry_data(self) -> List[IndustryModel]:
        """获取模拟行业数据"""
        mock_data = [
            IndustryModel("010000", "农林牧渔", 1, source="wind"),
            IndustryModel("020000", "采掘", 1, source="wind"),
            IndustryModel("030000", "化工", 1, source="wind"),
            IndustryModel("040000", "钢铁", 1, source="wind"),
            IndustryModel("050000", "有色金属", 1, source="wind"),
            IndustryModel("060000", "电子", 1, source="wind"),
            IndustryModel("070000", "家用电器", 1, source="wind"),
            IndustryModel("080000", "食品饮料", 1, source="wind"),
            IndustryModel("090000", "纺织服装", 1, source="wind"),
            IndustryModel("100000", "轻工制造", 1, source="wind"),
        ]
        logger.info(f"使用模拟行业数据: {len(mock_data)}条")
        return mock_data
    
    def _get_mock_stock_mapping_data(self) -> List[StockIndustryModel]:
        """获取模拟股票映射数据"""
        mock_data = [
            StockIndustryModel("000001", "平安银行", "080000", "食品饮料", 1, source="wind"),
            StockIndustryModel("000002", "万科A", "110000", "房地产", 1, source="wind"),
            StockIndustryModel("000858", "五粮液", "080000", "食品饮料", 1, source="wind"),
            StockIndustryModel("002415", "海康威视", "060000", "电子", 1, source="wind"),
            StockIndustryModel("600036", "招商银行", "120000", "银行", 1, source="wind"),
        ]
        logger.info(f"使用模拟股票映射数据: {len(mock_data)}条")
        return mock_data


class TushareDataCollector(BaseDataCollector):
    """Tushare数据采集器"""
    
    def __init__(self):
        super().__init__()
        self.tushare_config = config.tushare
        self.base_url = "http://api.tushare.pro"
    
    def collect_industry_data(self) -> List[IndustryModel]:
        """采集Tushare行业分类数据"""
        try:
            # 获取申万行业分类
            params = {
                'api_name': 'industry_classified',
                'token': self.tushare_config.token,
                'params': {'level': 'L1'},
                'fields': 'industry_code,industry_name'
            }
            
            response = self._make_request(self.base_url, params)
            if not response:
                return []
            
            industries = []
            for item in response.get('data', {}).get('items', []):
                industry = IndustryModel(
                    industry_code=str(item[0]),
                    industry_name=str(item[1]),
                    industry_level=1,
                    sw_code=str(item[0]),
                    source="tushare",
                    update_date=datetime.now()
                )
                industries.append(industry)
            
            logger.info(f"成功采集Tushare行业数据: {len(industries)}条")
            return industries
            
        except Exception as e:
            logger.error(f"Tushare数据采集失败: {e}")
            return []
    
    def collect_stock_industry_mapping(self) -> List[StockIndustryModel]:
        """采集Tushare股票行业映射数据"""
        try:
            # 获取股票行业分类
            params = {
                'api_name': 'stock_basic',
                'token': self.tushare_config.token,
                'params': {'list_status': 'L'},
                'fields': 'ts_code,symbol,name,industry'
            }
            
            response = self._make_request(self.base_url, params)
            if not response:
                return []
            
            mappings = []
            for item in response.get('data', {}).get('items', []):
                if item[3]:  # 行业不为空
                    mapping = StockIndustryModel(
                        stock_code=str(item[1]),
                        stock_name=str(item[2]),
                        industry_code="",  # Tushare没有标准行业代码
                        industry_name=str(item[3]),
                        industry_level=1,
                        source="tushare",
                        mapping_date=datetime.now(),
                        confidence=0.8  # 置信度稍低
                    )
                    mappings.append(mapping)
            
            logger.info(f"成功采集Tushare股票映射数据: {len(mappings)}条")
            return mappings
            
        except Exception as e:
            logger.error(f"Tushare股票映射数据采集失败: {e}")
            return []


class AKShareDataCollector(BaseDataCollector):
    """AKShare数据采集器"""
    
    def __init__(self):
        super().__init__()
        self.akshare_config = config.akshare
    
    def collect_industry_data(self) -> List[IndustryModel]:
        """采集AKShare行业分类数据"""
        try:
            import akshare as ak
            
            # 获取申万行业分类
            industry_data = ak.sw_index_spot()
            
            industries = []
            for _, row in industry_data.iterrows():
                industry = IndustryModel(
                    industry_code=str(row.get('代码', '')),
                    industry_name=str(row.get('名称', '')),
                    industry_level=1,
                    source="akshare",
                    update_date=datetime.now()
                )
                industries.append(industry)
            
            logger.info(f"成功采集AKShare行业数据: {len(industries)}条")
            return industries
            
        except ImportError:
            logger.warning("AKShare未安装，跳过数据采集")
            return []
        except Exception as e:
            logger.error(f"AKShare数据采集失败: {e}")
            return []
    
    def collect_stock_industry_mapping(self) -> List[StockIndustryModel]:
        """采集AKShare股票行业映射数据"""
        try:
            import akshare as ak
            
            # 获取股票行业分类
            stock_data = ak.stock_board_industry_name_em()
            
            mappings = []
            for _, row in stock_data.iterrows():
                mapping = StockIndustryModel(
                    stock_code=str(row.get('代码', '')),
                    stock_name=str(row.get('名称', '')),
                    industry_code="",
                    industry_name=str(row.get('所属行业', '')),
                    industry_level=1,
                    source="akshare",
                    mapping_date=datetime.now(),
                    confidence=0.7  # 置信度较低
                )
                mappings.append(mapping)
            
            logger.info(f"成功采集AKShare股票映射数据: {len(mappings)}条")
            return mappings
            
        except ImportError:
            logger.warning("AKShare未安装，跳过数据采集")
            return []
        except Exception as e:
            logger.error(f"AKShare股票映射数据采集失败: {e}")
            return []


class DataCollector:
    """数据采集管理器"""
    
    def __init__(self):
        self.collectors = {
            'wind': WindDataCollector(),
            'tushare': TushareDataCollector(),
            'akshare': AKShareDataCollector()
        }
    
    def collect_all_industry_data(self) -> Dict[str, List[IndustryModel]]:
        """从所有数据源采集行业数据"""
        results = {}
        
        for source, collector in self.collectors.items():
            try:
                logger.info(f"开始从{source}采集行业数据...")
                data = collector.collect_industry_data()
                results[source] = data
                logger.info(f"{source}行业数据采集完成: {len(data)}条")
            except Exception as e:
                logger.error(f"{source}行业数据采集失败: {e}")
                results[source] = []
        
        return results
    
    def collect_all_stock_mapping_data(self) -> Dict[str, List[StockIndustryModel]]:
        """从所有数据源采集股票映射数据"""
        results = {}
        
        for source, collector in self.collectors.items():
            try:
                logger.info(f"开始从{source}采集股票映射数据...")
                data = collector.collect_stock_industry_mapping()
                results[source] = data
                logger.info(f"{source}股票映射数据采集完成: {len(data)}条")
            except Exception as e:
                logger.error(f"{source}股票映射数据采集失败: {e}")
                results[source] = []
        
        return results
    
    def get_primary_industry_data(self) -> List[IndustryModel]:
        """获取主要数据源的行业数据（优先万得）"""
        # 优先使用万得数据
        wind_data = self.collectors['wind'].collect_industry_data()
        if wind_data:
            return wind_data
        
        # 备用Tushare数据
        tushare_data = self.collectors['tushare'].collect_industry_data()
        if tushare_data:
            return tushare_data
        
        # 最后使用AKShare数据
        akshare_data = self.collectors['akshare'].collect_industry_data()
        return akshare_data
    
    def get_primary_stock_mapping_data(self) -> List[StockIndustryModel]:
        """获取主要数据源的股票映射数据（优先万得）"""
        # 优先使用万得数据
        wind_data = self.collectors['wind'].collect_stock_industry_mapping()
        if wind_data:
            return wind_data
        
        # 备用Tushare数据
        tushare_data = self.collectors['tushare'].collect_stock_industry_mapping()
        if tushare_data:
            return tushare_data
        
        # 最后使用AKShare数据
        akshare_data = self.collectors['akshare'].collect_stock_industry_mapping()
        return akshare_data 