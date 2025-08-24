"""
数据处理器
负责热点数据的分析和处理
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from loguru import logger
from models.hotspot_model import HotspotModel, HotspotType, HotspotLevel, HotspotStatus
from config import config


class DataProcessor:
    """数据处理器"""
    
    def __init__(self):
        self.config = config.ANALYSIS
    
    def process_hotspots(self, hotspots: List[HotspotModel]) -> List[HotspotModel]:
        """处理热点数据"""
        processed_hotspots = []
        
        for hotspot in hotspots:
            try:
                # 增强关键词提取
                hotspot.keywords = self._enhance_keywords(hotspot)
                
                # 增强公司关联
                hotspot.related_companies = self._enhance_companies(hotspot)
                
                # 增强行业关联
                hotspot.related_industries = self._enhance_industries(hotspot)
                
                # 重新计算情感得分
                if self.config['sentiment_analysis']['enabled']:
                    hotspot.sentiment_score = self._enhance_sentiment_analysis(hotspot)
                
                # 重新计算热度得分
                if self.config['heat_calculation']['enabled']:
                    hotspot.heat_score = self._enhance_heat_calculation(hotspot)
                
                # 更新状态
                hotspot.status = self._determine_status(hotspot)
                
                # 更新级别
                hotspot.hotspot_level = self._determine_level(hotspot)
                
                processed_hotspots.append(hotspot)
                
            except Exception as e:
                logger.error(f"处理热点数据失败 {hotspot.hotspot_id}: {e}")
                processed_hotspots.append(hotspot)  # 保留原始数据
        
        logger.info(f"数据处理完成，共处理 {len(processed_hotspots)} 条热点")
        return processed_hotspots
    
    def _enhance_keywords(self, hotspot: HotspotModel) -> List[str]:
        """增强关键词提取"""
        try:
            keywords = set(hotspot.keywords)  # 去重
            
            # 从标题和内容中提取更多关键词
            text = hotspot.title + " " + hotspot.content
            
            # 金融相关关键词
            finance_keywords = [
                '股票', '基金', '债券', '期货', '外汇', '黄金', '原油',
                'A股', '港股', '美股', '科创板', '创业板', '主板',
                '央行', '证监会', '银保监会', '财政部', '发改委',
                '利率', '汇率', '通胀', 'GDP', 'CPI', 'PPI',
                '房地产', '汽车', '科技', '医药', '消费', '新能源',
                '人工智能', '大数据', '云计算', '区块链', '5G'
            ]
            
            for keyword in finance_keywords:
                if keyword in text and len(keywords) < self.config['keyword_extraction']['max_keywords']:
                    keywords.add(keyword)
            
            return list(keywords)
            
        except Exception as e:
            logger.warning(f"增强关键词提取失败: {e}")
            return hotspot.keywords
    
    def _enhance_companies(self, hotspot: HotspotModel) -> List[str]:
        """增强公司关联"""
        try:
            companies = set(hotspot.related_companies)  # 去重
            
            # 从标题和内容中提取公司名称
            text = hotspot.title + " " + hotspot.content
            
            # 常见公司名称
            company_names = [
                '阿里巴巴', '腾讯', '百度', '京东', '美团', '滴滴',
                '字节跳动', '小米', '华为', '中兴', '联想', '比亚迪',
                '宁德时代', '隆基绿能', '通威股份', '阳光电源',
                '招商银行', '平安银行', '工商银行', '建设银行',
                '中国石油', '中国石化', '中国移动', '中国联通',
                '中国平安', '中国人寿', '中国太保', '新华保险'
            ]
            
            for company in company_names:
                if company in text:
                    companies.add(company)
            
            return list(companies)
            
        except Exception as e:
            logger.warning(f"增强公司关联失败: {e}")
            return hotspot.related_companies
    
    def _enhance_industries(self, hotspot: HotspotModel) -> List[str]:
        """增强行业关联"""
        try:
            industries = set(hotspot.related_industries)  # 去重
            
            # 根据关键词映射行业代码
            industry_mapping = {
                '科技': ['801080', '801090'],  # 计算机、通信
                '医药': ['801150'],  # 医药生物
                '新能源': ['801770'],  # 电力设备
                '汽车': ['801880'],  # 汽车
                '房地产': ['801180'],  # 房地产
                '银行': ['801780'],  # 银行
                '保险': ['801790'],  # 非银金融
                '消费': ['801110'],  # 食品饮料
                '电子': ['801080'],  # 电子
                '化工': ['801030'],  # 化工
                '钢铁': ['801040'],  # 钢铁
                '有色金属': ['801050'],  # 有色金属
                '煤炭': ['801020'],  # 煤炭
                '电力': ['801770'],  # 电力设备
                '交通运输': ['801170'],  # 交通运输
            }
            
            text = hotspot.title + " " + hotspot.content
            
            for keyword, codes in industry_mapping.items():
                if keyword in text:
                    industries.update(codes)
            
            return list(industries)
            
        except Exception as e:
            logger.warning(f"增强行业关联失败: {e}")
            return hotspot.related_industries
    
    def _enhance_sentiment_analysis(self, hotspot: HotspotModel) -> float:
        """增强情感分析"""
        try:
            text = hotspot.title + " " + hotspot.content
            
            # 正面词汇
            positive_words = [
                '利好', '上涨', '增长', '突破', '创新', '发展', '机遇', '优势',
                '成功', '盈利', '收益', '利好', '积极', '乐观', '看好', '推荐',
                '买入', '增持', '优秀', '领先', '第一', '最佳', '突破性'
            ]
            
            # 负面词汇
            negative_words = [
                '利空', '下跌', '下降', '风险', '问题', '困难', '挑战', '危机',
                '亏损', '损失', '失败', '利空', '消极', '悲观', '看空', '卖出',
                '减持', '问题', '违规', '处罚', '退市', '破产', '违约'
            ]
            
            positive_count = sum(1 for word in positive_words if word in text)
            negative_count = sum(1 for word in negative_words if word in text)
            
            # 计算情感得分
            if positive_count == 0 and negative_count == 0:
                return 0.0
            elif positive_count > negative_count:
                score = min(0.9, positive_count * 0.15)
                return score
            else:
                score = max(-0.9, -negative_count * 0.15)
                return score
                
        except Exception as e:
            logger.warning(f"增强情感分析失败: {e}")
            return hotspot.sentiment_score or 0.0
    
    def _enhance_heat_calculation(self, hotspot: HotspotModel) -> float:
        """增强热度计算"""
        try:
            base_score = 50.0
            text = hotspot.title + " " + hotspot.content
            
            # 热度关键词
            hot_keywords = [
                '涨停', '跌停', '暴涨', '暴跌', '紧急', '重大', '突发',
                '创新高', '创新低', '突破', '历史', '首次', '重要',
                '政策', '法规', '通知', '意见', '规划', '方案'
            ]
            
            # 根据关键词增加热度
            for keyword in hot_keywords:
                if keyword in text:
                    base_score += 8.0
            
            # 根据类型调整热度
            if hotspot.hotspot_type == HotspotType.POLICY:
                base_score += 15.0
            elif hotspot.hotspot_type == HotspotType.NEWS:
                base_score += 5.0
            
            # 根据情感得分调整热度
            if hotspot.sentiment_score:
                if abs(hotspot.sentiment_score) > 0.5:
                    base_score += 10.0
            
            # 根据相关公司数量调整热度
            if len(hotspot.related_companies) > 3:
                base_score += 5.0
            
            # 限制在0-100范围内
            return max(0.0, min(100.0, base_score))
            
        except Exception as e:
            logger.warning(f"增强热度计算失败: {e}")
            return hotspot.heat_score or 50.0
    
    def _determine_status(self, hotspot: HotspotModel) -> HotspotStatus:
        """确定热点状态"""
        try:
            # 根据发布时间和热度确定状态
            if hotspot.publish_time:
                days_old = (datetime.now() - hotspot.publish_time).days
                
                if days_old > 7:
                    return HotspotStatus.EXPIRED
                elif days_old > 3 and hotspot.heat_score and hotspot.heat_score < 30:
                    return HotspotStatus.DECLINING
                else:
                    return HotspotStatus.ACTIVE
            
            return HotspotStatus.ACTIVE
            
        except Exception as e:
            logger.warning(f"确定状态失败: {e}")
            return HotspotStatus.ACTIVE
    
    def _determine_level(self, hotspot: HotspotModel) -> HotspotLevel:
        """确定热点级别"""
        try:
            if not hotspot.heat_score:
                return HotspotLevel.MEDIUM
            
            if hotspot.heat_score >= 80:
                return HotspotLevel.VERY_HIGH
            elif hotspot.heat_score >= 60:
                return HotspotLevel.HIGH
            elif hotspot.heat_score >= 40:
                return HotspotLevel.MEDIUM
            else:
                return HotspotLevel.LOW
                
        except Exception as e:
            logger.warning(f"确定级别失败: {e}")
            return HotspotLevel.MEDIUM
    
    def analyze_hotspots_trend(self, hotspots: List[HotspotModel]) -> Dict[str, Any]:
        """分析热点趋势"""
        try:
            analysis = {
                'total_count': len(hotspots),
                'by_type': {},
                'by_level': {},
                'by_status': {},
                'by_source': {},
                'avg_sentiment': 0.0,
                'avg_heat': 0.0,
                'top_keywords': [],
                'top_companies': [],
                'top_industries': []
            }
            
            if not hotspots:
                return analysis
            
            # 按类型统计
            for hotspot in hotspots:
                type_name = hotspot.hotspot_type.value
                analysis['by_type'][type_name] = analysis['by_type'].get(type_name, 0) + 1
            
            # 按级别统计
            for hotspot in hotspots:
                level_name = hotspot.hotspot_level.value
                analysis['by_level'][level_name] = analysis['by_level'].get(level_name, 0) + 1
            
            # 按状态统计
            for hotspot in hotspots:
                status_name = hotspot.status.value
                analysis['by_status'][status_name] = analysis['by_status'].get(status_name, 0) + 1
            
            # 按来源统计
            for hotspot in hotspots:
                source_name = hotspot.source
                analysis['by_source'][source_name] = analysis['by_source'].get(source_name, 0) + 1
            
            # 计算平均情感得分
            sentiment_scores = [h.sentiment_score for h in hotspots if h.sentiment_score is not None]
            if sentiment_scores:
                analysis['avg_sentiment'] = sum(sentiment_scores) / len(sentiment_scores)
            
            # 计算平均热度得分
            heat_scores = [h.heat_score for h in hotspots if h.heat_score is not None]
            if heat_scores:
                analysis['avg_heat'] = sum(heat_scores) / len(heat_scores)
            
            # 统计关键词
            keyword_count = {}
            for hotspot in hotspots:
                for keyword in hotspot.keywords:
                    keyword_count[keyword] = keyword_count.get(keyword, 0) + 1
            
            analysis['top_keywords'] = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # 统计公司
            company_count = {}
            for hotspot in hotspots:
                for company in hotspot.related_companies:
                    company_count[company] = company_count.get(company, 0) + 1
            
            analysis['top_companies'] = sorted(company_count.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # 统计行业
            industry_count = {}
            for hotspot in hotspots:
                for industry in hotspot.related_industries:
                    industry_count[industry] = industry_count.get(industry, 0) + 1
            
            analysis['top_industries'] = sorted(industry_count.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return analysis
            
        except Exception as e:
            logger.error(f"分析热点趋势失败: {e}")
            return {}
    
    def filter_hotspots(self, 
                       hotspots: List[HotspotModel],
                       hotspot_type: Optional[str] = None,
                       hotspot_level: Optional[str] = None,
                       status: Optional[str] = None,
                       source: Optional[str] = None,
                       min_heat_score: Optional[float] = None,
                       max_heat_score: Optional[float] = None,
                       min_sentiment_score: Optional[float] = None,
                       max_sentiment_score: Optional[float] = None) -> List[HotspotModel]:
        """过滤热点数据"""
        try:
            filtered_hotspots = []
            
            for hotspot in hotspots:
                # 类型过滤
                if hotspot_type and hotspot.hotspot_type.value != hotspot_type:
                    continue
                
                # 级别过滤
                if hotspot_level and hotspot.hotspot_level.value != hotspot_level:
                    continue
                
                # 状态过滤
                if status and hotspot.status.value != status:
                    continue
                
                # 来源过滤
                if source and hotspot.source != source:
                    continue
                
                # 热度得分过滤
                if min_heat_score is not None and (hotspot.heat_score is None or hotspot.heat_score < min_heat_score):
                    continue
                
                if max_heat_score is not None and (hotspot.heat_score is None or hotspot.heat_score > max_heat_score):
                    continue
                
                # 情感得分过滤
                if min_sentiment_score is not None and (hotspot.sentiment_score is None or hotspot.sentiment_score < min_sentiment_score):
                    continue
                
                if max_sentiment_score is not None and (hotspot.sentiment_score is None or hotspot.sentiment_score > max_sentiment_score):
                    continue
                
                filtered_hotspots.append(hotspot)
            
            return filtered_hotspots
            
        except Exception as e:
            logger.error(f"过滤热点数据失败: {e}")
            return hotspots 