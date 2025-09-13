"""
国外热点数据收集器
"""

import requests
import time
import hashlib
from datetime import datetime
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from loguru import logger
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from models.international_hotspot_model import HotspotType, Region, HotspotLevel, HotspotStatus


class InternationalHotspotCollector:
    """国外热点数据收集器"""
    
    def __init__(self):
        self.config = Config.COLLECTOR
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.config['user_agent']
        })
    
    def collect_from_source(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """从单个数据源收集数据"""
        try:
            logger.info(f"开始从 {source['name']} 收集数据")
            
            response = self.session.get(
                source['url'],
                timeout=self.config['request_timeout']
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return self._parse_generic(soup, source)
                
        except Exception as e:
            logger.error(f"从 {source['name']} 收集数据失败: {e}")
            return []
    
    def _parse_generic(self, soup: BeautifulSoup, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """通用解析方法"""
        hotspots = []
        try:
            links = soup.find_all('a', href=True)
            
            for link in links[:10]:
                title = link.get_text(strip=True)
                if not title or len(title) < 10:
                    continue
                
                url = link.get('href')
                if url and not url.startswith('http'):
                    url = source['url'].rstrip('/') + '/' + url.lstrip('/')
                
                hotspot_id = hashlib.md5(f"{source['name']}_{title}".encode()).hexdigest()
                
                hotspot = {
                    'hotspot_id': hotspot_id,
                    'title': title,
                    'content': title,
                    'hotspot_type': source['type'],
                    'region': source['region'],
                    'hotspot_level': HotspotLevel.MEDIUM.value,
                    'status': HotspotStatus.ACTIVE.value,
                    'source': source['name'],
                    'url': url,
                    'publish_time': datetime.now(),
                    'keywords': [],
                    'related_companies': [],
                    'related_industries': [],
                    'sentiment_score': None,
                    'heat_score': None
                }
                
                hotspots.append(hotspot)
                
        except Exception as e:
            logger.error(f"通用解析失败: {e}")
        
        return hotspots
    
    def collect_all(self) -> List[Dict[str, Any]]:
        """收集所有数据源的数据"""
        all_hotspots = []
        
        enabled_sources = []
        for category, sources in Config.DATA_SOURCES.items():
            enabled_sources.extend([s for s in sources if s.get('enabled', True)])
        
        logger.info(f"开始收集 {len(enabled_sources)} 个数据源的数据")
        
        for source in enabled_sources:
            try:
                hotspots = self.collect_from_source(source)
                all_hotspots.extend(hotspots)
                logger.info(f"从 {source['name']} 收集到 {len(hotspots)} 条数据")
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"收集 {source['name']} 数据失败: {e}")
                continue
        
        logger.info(f"总共收集到 {len(all_hotspots)} 条热点数据")
        return all_hotspots 