"""
公司信息验证器
负责验证公司信息的完整性和准确性
"""

from typing import List, Tuple, Dict, Any
from datetime import datetime

from ..models.company_model import CompanyModel, CompanyStatus, MarketType, CompanyType
from ..utils.logger import logger


class CompanyValidator:
    """公司信息验证器"""
    
    def __init__(self):
        """初始化验证器"""
        self.logger = logger
    
    def validate_company_data(self, companies: List[CompanyModel]) -> Tuple[bool, List[str]]:
        """验证公司数据"""
        errors = []
        warnings = []
        
        self.logger.info(f"开始验证公司数据: {len(companies)}条")
        
        for i, company in enumerate(companies):
            # 基本验证
            if not company.company_name:
                errors.append(f"第{i+1}条: 公司名称为空")
            
            if not company.stock_code:
                errors.append(f"第{i+1}条: 股票代码为空")
            
            if not company.market:
                errors.append(f"第{i+1}条: 市场类型为空")
            
            # 股票代码格式验证
            if not self._validate_stock_code_format(company):
                errors.append(f"第{i+1}条: 股票代码格式错误 {company.stock_code}")
            
            # 市场类型验证
            if not self._validate_market_type(company.market):
                errors.append(f"第{i+1}条: 无效市场类型 {company.market}")
            
            # 公司类型验证
            if company.company_type and not self._validate_company_type(company.company_type):
                errors.append(f"第{i+1}条: 无效公司类型 {company.company_type}")
            
            # 上市日期验证
            if company.list_date and not self._validate_list_date(company.list_date):
                errors.append(f"第{i+1}条: 上市日期异常 {company.list_date}")
            
            # 状态验证
            if not self._validate_status(company.status):
                errors.append(f"第{i+1}条: 无效状态 {company.status}")
        
        # 数据量检查
        if len(companies) < 10:
            warnings.append("公司数据量较少")
        
        # 重复检查
        duplicates = self._check_duplicates(companies)
        if duplicates:
            warnings.append(f"发现 {len(duplicates)} 个重复记录")
        
        is_valid = len(errors) == 0
        self.logger.info(f"公司数据验证: {'通过' if is_valid else '失败'}")
        
        return is_valid, errors + warnings
    
    def _validate_stock_code_format(self, company: CompanyModel) -> bool:
        """验证股票代码格式"""
        try:
            code = company.stock_code
            market = company.market
            
            # A股代码格式：6位数字
            if market in ['SH', 'SZ']:
                return len(code) == 6 and code.isdigit()
            
            # 港股代码格式：4-5位数字
            elif market == 'HK':
                return 4 <= len(code) <= 5 and code.isdigit()
            
            # 美股代码格式：字母数字组合
            elif market == 'US':
                return len(code) >= 1 and code.isalnum()
            
            return False
            
        except Exception as e:
            self.logger.error(f"股票代码格式验证失败: {e}")
            return False
    
    def _validate_market_type(self, market: str) -> bool:
        """验证市场类型"""
        valid_markets = ['SH', 'SZ', 'HK', 'US']
        return market in valid_markets
    
    def _validate_company_type(self, company_type: CompanyType) -> bool:
        """验证公司类型"""
        valid_types = [
            CompanyType.MAIN_BOARD,
            CompanyType.SME_BOARD,
            CompanyType.GEM,
            CompanyType.STAR,
            CompanyType.NEW_THIRD
        ]
        return company_type in valid_types
    
    def _validate_list_date(self, list_date: datetime) -> bool:
        """验证上市日期"""
        try:
            # 上市日期不能晚于当前日期
            if list_date > datetime.now():
                return False
            
            # 上市日期不能早于1990年（中国股市开始时间）
            if list_date < datetime(1990, 1, 1):
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"上市日期验证失败: {e}")
            return False
    
    def _validate_status(self, status: CompanyStatus) -> bool:
        """验证公司状态"""
        valid_statuses = [
            CompanyStatus.ACTIVE,
            CompanyStatus.SUSPENDED,
            CompanyStatus.DELISTED,
            CompanyStatus.PENDING
        ]
        return status in valid_statuses
    
    def _check_duplicates(self, companies: List[CompanyModel]) -> List[str]:
        """检查重复记录"""
        duplicates = []
        seen = set()
        
        for company in companies:
            key = f"{company.stock_code}_{company.market}"
            if key in seen:
                duplicates.append(key)
            else:
                seen.add(key)
        
        return duplicates
    
    def validate_company_consistency(self, companies: List[CompanyModel]) -> Tuple[bool, List[str]]:
        """验证公司数据一致性"""
        errors = []
        warnings = []
        
        self.logger.info("开始验证公司数据一致性")
        
        # 检查同一公司在不同数据源中的信息是否一致
        company_groups = {}
        for company in companies:
            key = f"{company.stock_code}_{company.market}"
            if key not in company_groups:
                company_groups[key] = []
            company_groups[key].append(company)
        
        for key, group in company_groups.items():
            if len(group) > 1:
                # 检查公司名称是否一致
                names = [c.company_name for c in group]
                if len(set(names)) > 1:
                    warnings.append(f"公司 {key} 在不同数据源中的名称不一致: {names}")
                
                # 检查状态是否一致
                statuses = [c.status for c in group]
                if len(set(statuses)) > 1:
                    warnings.append(f"公司 {key} 在不同数据源中的状态不一致: {statuses}")
        
        is_consistent = len(errors) == 0
        self.logger.info(f"公司数据一致性验证: {'通过' if is_consistent else '失败'}")
        
        return is_consistent, errors + warnings
    
    def validate_data_completeness(self, companies: List[CompanyModel]) -> Tuple[bool, List[str]]:
        """验证数据完整性"""
        errors = []
        warnings = []
        
        self.logger.info("开始验证数据完整性")
        
        total_companies = len(companies)
        if total_companies == 0:
            errors.append("没有公司数据")
            return False, errors
        
        # 统计各字段的完整性
        field_stats = {
            'company_name': 0,
            'stock_code': 0,
            'market': 0,
            'short_name': 0,
            'company_type': 0,
            'list_date': 0,
            'area': 0,
            'website': 0,
            'business_scope': 0
        }
        
        for company in companies:
            if company.company_name:
                field_stats['company_name'] += 1
            if company.stock_code:
                field_stats['stock_code'] += 1
            if company.market:
                field_stats['market'] += 1
            if company.short_name:
                field_stats['short_name'] += 1
            if company.company_type:
                field_stats['company_type'] += 1
            if company.list_date:
                field_stats['list_date'] += 1
            if company.area:
                field_stats['area'] += 1
            if company.website:
                field_stats['website'] += 1
            if company.business_scope:
                field_stats['business_scope'] += 1
        
        # 计算完整性比例
        for field, count in field_stats.items():
            completeness = count / total_companies
            if completeness < 0.8:
                warnings.append(f"字段 {field} 完整性较低: {completeness:.2%}")
            if completeness < 0.5:
                errors.append(f"字段 {field} 完整性过低: {completeness:.2%}")
        
        is_complete = len(errors) == 0
        self.logger.info(f"数据完整性验证: {'通过' if is_complete else '失败'}")
        
        return is_complete, errors + warnings 