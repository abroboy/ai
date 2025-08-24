"""
后台数据更新任务
定期从爬虫获取数据并存储到数据库
"""

import os
import sys
import time
import threading
from datetime import datetime, timedelta
from typing import List
from loguru import logger

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.web_scraper import WebScraper
from core.real_data_collector import RealDataCollector
from core.data_generator import DataGenerator
from core.data_storage import DataStorage


class DataUpdater:
    """数据更新器"""
    
    def __init__(self):
        self.web_scraper = WebScraper()
        self.real_data_collector = RealDataCollector()
        self.data_generator = DataGenerator()
        self.data_storage = DataStorage()
        self.is_running = False
        self.update_thread = None
        
    def start_background_update(self, interval_minutes: int = 30):
        """启动后台更新任务"""
        if self.is_running:
            logger.warning("后台更新任务已在运行")
            return
        
        self.is_running = True
        self.update_thread = threading.Thread(
            target=self._background_update_loop,
            args=(interval_minutes,),
            daemon=True
        )
        self.update_thread.start()
        logger.info(f"后台数据更新任务已启动，更新间隔: {interval_minutes} 分钟")
    
    def stop_background_update(self):
        """停止后台更新任务"""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join(timeout=5)
        logger.info("后台数据更新任务已停止")
    
    def _background_update_loop(self, interval_minutes: int):
        """后台更新循环"""
        while self.is_running:
            try:
                logger.info("开始执行后台数据更新...")
                self.update_all_data()
                logger.info(f"后台数据更新完成，下次更新时间: {datetime.now() + timedelta(minutes=interval_minutes)}")
            except Exception as e:
                logger.error(f"后台数据更新失败: {e}")
            
            # 等待下次更新
            for _ in range(interval_minutes * 60):
                if not self.is_running:
                    break
                time.sleep(1)
    
    def update_all_data(self) -> int:
        """更新所有数据"""
        total_updated = 0
        
        # 1. 尝试获取真实数据（API + 爬虫）
        logger.info("开始获取真实数据...")
        real_hotspots = self._get_real_data()
        
        if real_hotspots:
            saved_count = self.data_storage.save_hotspots(real_hotspots)
            total_updated += saved_count
            logger.info(f"保存了 {saved_count} 条真实数据")
        
        # 2. 如果真实数据不足，补充模拟数据
        if total_updated < 100:
            logger.info("真实数据不足，补充模拟数据...")
            mock_hotspots = self.data_generator.generate_daily_hotspots(150 - total_updated)
            saved_count = self.data_storage.save_hotspots(mock_hotspots)
            total_updated += saved_count
            logger.info(f"补充了 {saved_count} 条模拟数据")
        
        # 3. 清理旧数据
        self.data_storage.clean_old_data(days=30)
        
        logger.info(f"数据更新完成，总共更新 {total_updated} 条数据")
        return total_updated
    
    def _get_real_data(self) -> List:
        """获取真实数据"""
        all_hotspots = []
        
        # 首先尝试API数据
        try:
            api_hotspots = self.real_data_collector.collect_all_real_data()
            all_hotspots.extend(api_hotspots)
            logger.info(f"从API获取到 {len(api_hotspots)} 条数据")
        except Exception as e:
            logger.error(f"API数据获取失败: {e}")
        
        # 如果API数据不足，使用爬虫
        if len(all_hotspots) < 50:
            try:
                scraped_hotspots = self.web_scraper.scrape_all_sources()
                all_hotspots.extend(scraped_hotspots)
                logger.info(f"从爬虫获取到 {len(scraped_hotspots)} 条数据")
            except Exception as e:
                logger.error(f"爬虫数据获取失败: {e}")
        
        return all_hotspots
    
    def manual_update(self) -> dict:
        """手动触发数据更新"""
        try:
            logger.info("手动触发数据更新...")
            start_time = datetime.now()
            
            updated_count = self.update_all_data()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result = {
                'success': True,
                'updated_count': updated_count,
                'duration': duration,
                'message': f'成功更新 {updated_count} 条数据，耗时 {duration:.2f} 秒'
            }
            
            logger.info(f"手动数据更新完成: {result['message']}")
            return result
            
        except Exception as e:
            logger.error(f"手动数据更新失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f'数据更新失败: {e}'
            }
    
    def get_update_status(self) -> dict:
        """获取更新状态"""
        try:
            stats = self.data_storage.get_statistics()
            
            return {
                'is_running': self.is_running,
                'total_data': stats['total'],
                'today_data': stats['today_count'],
                'type_distribution': stats['type_distribution'],
                'source_distribution': stats['source_distribution'],
                'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logger.error(f"获取更新状态失败: {e}")
            return {
                'is_running': self.is_running,
                'error': str(e)
            }


# 全局数据更新器实例
data_updater = DataUpdater()


def start_data_updater():
    """启动数据更新器"""
    # 确保数据表存在
    data_updater.data_storage.create_table_if_not_exists()
    
    # 启动后台更新任务
    data_updater.start_background_update(interval_minutes=30)
    
    return data_updater


def stop_data_updater():
    """停止数据更新器"""
    data_updater.stop_background_update()


def manual_update_data():
    """手动更新数据"""
    return data_updater.manual_update()


def get_update_status():
    """获取更新状态"""
    return data_updater.get_update_status() 