"""
公司信息管理器
负责公司信息的存储、查询和管理
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date
import pandas as pd

from ..models.company_model import CompanyModel, CompanyStatus, MarketType, CompanyType
from ..utils.database import db_manager
from ..utils.logger import logger


class CompanyManager:
    """公司信息管理器"""
    
    def __init__(self):
        """初始化管理器"""
        self.logger = logger
        self.db = db_manager
    
    def save_companies(self, companies: List[CompanyModel]) -> bool:
        """保存公司信息"""
        try:
            self.logger.info(f"开始保存 {len(companies)} 家公司信息")
            
            if not companies:
                self.logger.warning("没有公司数据需要保存")
                return True
            
            # 转换为数据库格式
            data_list = []
            for company in companies:
                data = {
                    'company_name': company.company_name,
                    'stock_code': company.stock_code,
                    'market': company.market,
                    'short_name': company.short_name,
                    'industry_code': company.industry_code,
                    'list_date': company.list_date,
                    'status': company.status.value,
                    'company_type': company.company_type.value if company.company_type else None,
                    'area': company.area,
                    'website': company.website,
                    'business_scope': company.business_scope,
                    'market_cap': company.market_cap,
                    'employees': company.employees,
                    'update_date': datetime.now(),
                    'source': company.source
                }
                data_list.append(data)
            
            # 批量插入数据库
            success = self.db.insert_many('company_list', data_list)
            
            if success:
                self.logger.info(f"成功保存 {len(companies)} 家公司信息")
            else:
                self.logger.error("保存公司信息失败")
            
            return success
            
        except Exception as e:
            self.logger.error(f"保存公司信息异常: {e}")
            return False
    
    def get_companies_by_market(self, market: str) -> List[CompanyModel]:
        """按市场获取公司信息"""
        try:
            self.logger.info(f"查询 {market} 市场的公司信息")
            
            query = "SELECT * FROM company_list WHERE market = %s AND status = 'active'"
            result = self.db.execute_query(query, (market,))
            
            companies = []
            for row in result:
                company = self._row_to_company_model(row)
                companies.append(company)
            
            self.logger.info(f"查询到 {len(companies)} 家 {market} 市场公司")
            return companies
            
        except Exception as e:
            self.logger.error(f"按市场查询公司信息失败: {e}")
            return []
    
    def get_companies_by_type(self, company_type: CompanyType) -> List[CompanyModel]:
        """按公司类型获取公司信息"""
        try:
            self.logger.info(f"查询 {company_type.value} 类型的公司信息")
            
            query = "SELECT * FROM company_list WHERE company_type = %s AND status = 'active'"
            result = self.db.execute_query(query, (company_type.value,))
            
            companies = []
            for row in result:
                company = self._row_to_company_model(row)
                companies.append(company)
            
            self.logger.info(f"查询到 {len(companies)} 家 {company_type.value} 类型公司")
            return companies
            
        except Exception as e:
            self.logger.error(f"按类型查询公司信息失败: {e}")
            return []
    
    def get_company_by_code(self, stock_code: str, market: str) -> Optional[CompanyModel]:
        """根据股票代码获取公司信息"""
        try:
            self.logger.info(f"查询公司信息: {stock_code}.{market}")
            
            query = "SELECT * FROM company_list WHERE stock_code = %s AND market = %s"
            result = self.db.execute_query(query, (stock_code, market))
            
            if result:
                company = self._row_to_company_model(result[0])
                self.logger.info(f"查询到公司: {company.company_name}")
                return company
            else:
                self.logger.warning(f"未找到公司: {stock_code}.{market}")
                return None
                
        except Exception as e:
            self.logger.error(f"根据代码查询公司信息失败: {e}")
            return None
    
    def search_companies(self, keyword: str) -> List[CompanyModel]:
        """搜索公司信息"""
        try:
            self.logger.info(f"搜索公司信息: {keyword}")
            
            query = """
                SELECT * FROM company_list 
                WHERE (company_name LIKE %s OR short_name LIKE %s OR stock_code LIKE %s)
                AND status = 'active'
            """
            pattern = f"%{keyword}%"
            result = self.db.execute_query(query, (pattern, pattern, pattern))
            
            companies = []
            for row in result:
                company = self._row_to_company_model(row)
                companies.append(company)
            
            self.logger.info(f"搜索到 {len(companies)} 家公司")
            return companies
            
        except Exception as e:
            self.logger.error(f"搜索公司信息失败: {e}")
            return []
    
    def get_companies_by_area(self, area: str) -> List[CompanyModel]:
        """按地区获取公司信息"""
        try:
            self.logger.info(f"查询 {area} 地区的公司信息")
            
            query = "SELECT * FROM company_list WHERE area LIKE %s AND status = 'active'"
            result = self.db.execute_query(query, (f"%{area}%",))
            
            companies = []
            for row in result:
                company = self._row_to_company_model(row)
                companies.append(company)
            
            self.logger.info(f"查询到 {len(companies)} 家 {area} 地区公司")
            return companies
            
        except Exception as e:
            self.logger.error(f"按地区查询公司信息失败: {e}")
            return []
    
    def get_companies_by_industry(self, industry_code: str) -> List[CompanyModel]:
        """按行业获取公司信息"""
        try:
            self.logger.info(f"查询行业 {industry_code} 的公司信息")
            
            query = "SELECT * FROM company_list WHERE industry_code = %s AND status = 'active'"
            result = self.db.execute_query(query, (industry_code,))
            
            companies = []
            for row in result:
                company = self._row_to_company_model(row)
                companies.append(company)
            
            self.logger.info(f"查询到 {len(companies)} 家行业 {industry_code} 公司")
            return companies
            
        except Exception as e:
            self.logger.error(f"按行业查询公司信息失败: {e}")
            return []
    
    def update_company_status(self, stock_code: str, market: str, status: CompanyStatus) -> bool:
        """更新公司状态"""
        try:
            self.logger.info(f"更新公司状态: {stock_code}.{market} -> {status.value}")
            
            query = "UPDATE company_list SET status = %s, updated_at = NOW() WHERE stock_code = %s AND market = %s"
            success = self.db.execute_update(query, (status.value, stock_code, market))
            
            if success:
                self.logger.info(f"成功更新公司状态: {stock_code}.{market}")
            else:
                self.logger.error(f"更新公司状态失败: {stock_code}.{market}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"更新公司状态异常: {e}")
            return False
    
    def get_company_statistics(self) -> Dict[str, Any]:
        """获取公司统计信息"""
        try:
            self.logger.info("获取公司统计信息")
            
            stats = {}
            
            # 总公司数量
            query = "SELECT COUNT(*) as total FROM company_list WHERE status = 'active'"
            result = self.db.execute_query(query)
            stats['total_companies'] = result[0]['total'] if result else 0
            
            # 按市场统计
            query = "SELECT market, COUNT(*) as count FROM company_list WHERE status = 'active' GROUP BY market"
            result = self.db.execute_query(query)
            stats['by_market'] = {row['market']: row['count'] for row in result}
            
            # 按公司类型统计
            query = "SELECT company_type, COUNT(*) as count FROM company_list WHERE status = 'active' GROUP BY company_type"
            result = self.db.execute_query(query)
            stats['by_type'] = {row['company_type']: row['count'] for row in result}
            
            # 按地区统计
            query = "SELECT area, COUNT(*) as count FROM company_list WHERE status = 'active' GROUP BY area ORDER BY count DESC LIMIT 10"
            result = self.db.execute_query(query)
            stats['by_area'] = {row['area']: row['count'] for row in result}
            
            self.logger.info(f"统计信息: 总共有 {stats['total_companies']} 家公司")
            return stats
            
        except Exception as e:
            self.logger.error(f"获取公司统计信息失败: {e}")
            return {}
    
    def _row_to_company_model(self, row: Dict[str, Any]) -> CompanyModel:
        """将数据库行转换为公司模型"""
        try:
            return CompanyModel(
                company_name=row['company_name'],
                stock_code=row['stock_code'],
                market=row['market'],
                short_name=row['short_name'],
                industry_code=row['industry_code'],
                list_date=row['list_date'] if row['list_date'] else None,
                status=CompanyStatus(row['status']),
                company_type=CompanyType(row['company_type']) if row['company_type'] else None,
                area=row['area'],
                website=row['website'],
                business_scope=row['business_scope'],
                market_cap=row['market_cap'],
                employees=row['employees'],
                update_date=row['update_date'] if row['update_date'] else None,
                source=row['source'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        except Exception as e:
            self.logger.error(f"转换公司模型失败: {e}")
            raise 