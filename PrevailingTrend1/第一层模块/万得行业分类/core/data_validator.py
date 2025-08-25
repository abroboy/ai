"""
数据验证器
负责验证行业分类数据的质量和一致性
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime
import re

from ..models.industry_model import IndustryModel, IndustryStatus
from ..models.stock_industry_model import StockIndustryModel, MappingStatus
from ..utils.logger import logger


class DataValidator:
    """数据验证器"""
    
    def __init__(self):
        self.validation_errors = []
        self.validation_warnings = []
    
    def validate_industry_data(self, industries: List[IndustryModel]) -> Tuple[bool, List[str]]:
        """验证行业分类数据"""
        self.validation_errors = []
        self.validation_warnings = []
        
        logger.info(f"开始验证行业数据，共{len(industries)}条记录")
        
        # 基础格式验证
        self._validate_industry_format(industries)
        
        # 业务逻辑验证
        self._validate_industry_logic(industries)
        
        # 数据完整性验证
        self._validate_industry_completeness(industries)
        
        # 输出验证结果
        is_valid = len(self.validation_errors) == 0
        logger.info(f"行业数据验证完成: {'通过' if is_valid else '失败'}")
        logger.info(f"错误数量: {len(self.validation_errors)}, 警告数量: {len(self.validation_warnings)}")
        
        return is_valid, self.validation_errors + self.validation_warnings
    
    def validate_stock_mapping_data(self, mappings: List[StockIndustryModel]) -> Tuple[bool, List[str]]:
        """验证股票行业映射数据"""
        self.validation_errors = []
        self.validation_warnings = []
        
        logger.info(f"开始验证股票映射数据，共{len(mappings)}条记录")
        
        # 基础格式验证
        self._validate_mapping_format(mappings)
        
        # 业务逻辑验证
        self._validate_mapping_logic(mappings)
        
        # 数据完整性验证
        self._validate_mapping_completeness(mappings)
        
        # 输出验证结果
        is_valid = len(self.validation_errors) == 0
        logger.info(f"股票映射数据验证完成: {'通过' if is_valid else '失败'}")
        logger.info(f"错误数量: {len(self.validation_errors)}, 警告数量: {len(self.validation_warnings)}")
        
        return is_valid, self.validation_errors + self.validation_warnings
    
    def _validate_industry_format(self, industries: List[IndustryModel]):
        """验证行业数据格式"""
        for i, industry in enumerate(industries):
            # 验证行业代码格式
            if not self._is_valid_industry_code(industry.industry_code):
                self.validation_errors.append(
                    f"第{i+1}条记录: 无效的行业代码格式 '{industry.industry_code}'"
                )
            
            # 验证行业名称
            if not industry.industry_name or len(industry.industry_name.strip()) == 0:
                self.validation_errors.append(
                    f"第{i+1}条记录: 行业名称为空"
                )
            
            # 验证行业层级
            if industry.industry_level not in [1, 2, 3]:
                self.validation_errors.append(
                    f"第{i+1}条记录: 无效的行业层级 {industry.industry_level}"
                )
            
            # 验证状态
            if not isinstance(industry.status, IndustryStatus):
                self.validation_errors.append(
                    f"第{i+1}条记录: 无效的行业状态 {industry.status}"
                )
    
    def _validate_industry_logic(self, industries: List[IndustryModel]):
        """验证行业数据业务逻辑"""
        # 构建行业代码映射
        industry_map = {ind.industry_code: ind for ind in industries}
        
        for i, industry in enumerate(industries):
            # 验证父级关系
            if industry.industry_level > 1:
                if not industry.parent_code:
                    self.validation_errors.append(
                        f"第{i+1}条记录: 二级/三级行业缺少父级行业代码"
                    )
                elif industry.parent_code not in industry_map:
                    self.validation_errors.append(
                        f"第{i+1}条记录: 父级行业代码 '{industry.parent_code}' 不存在"
                    )
                else:
                    parent = industry_map[industry.parent_code]
                    if parent.industry_level != industry.industry_level - 1:
                        self.validation_errors.append(
                            f"第{i+1}条记录: 父级行业层级关系错误"
                        )
            
            # 验证行业代码唯一性
            same_code_industries = [ind for ind in industries 
                                  if ind.industry_code == industry.industry_code]
            if len(same_code_industries) > 1:
                self.validation_warnings.append(
                    f"第{i+1}条记录: 行业代码 '{industry.industry_code}' 重复"
                )
    
    def _validate_industry_completeness(self, industries: List[IndustryModel]):
        """验证行业数据完整性"""
        # 检查是否有足够的行业数据
        if len(industries) < 10:
            self.validation_warnings.append("行业数据量较少，可能不完整")
        
        # 检查各层级行业数量
        level_counts = {}
        for industry in industries:
            level = industry.industry_level
            level_counts[level] = level_counts.get(level, 0) + 1
        
        for level in [1, 2, 3]:
            count = level_counts.get(level, 0)
            if count == 0:
                self.validation_warnings.append(f"缺少{level}级行业数据")
            elif level == 1 and count < 20:
                self.validation_warnings.append(f"一级行业数量较少: {count}个")
    
    def _validate_mapping_format(self, mappings: List[StockIndustryModel]):
        """验证股票映射数据格式"""
        for i, mapping in enumerate(mappings):
            # 验证股票代码格式
            if not self._is_valid_stock_code(mapping.stock_code):
                self.validation_errors.append(
                    f"第{i+1}条记录: 无效的股票代码格式 '{mapping.stock_code}'"
                )
            
            # 验证股票名称
            if not mapping.stock_name or len(mapping.stock_name.strip()) == 0:
                self.validation_errors.append(
                    f"第{i+1}条记录: 股票名称为空"
                )
            
            # 验证行业代码格式
            if mapping.industry_code and not self._is_valid_industry_code(mapping.industry_code):
                self.validation_errors.append(
                    f"第{i+1}条记录: 无效的行业代码格式 '{mapping.industry_code}'"
                )
            
            # 验证行业名称
            if not mapping.industry_name or len(mapping.industry_name.strip()) == 0:
                self.validation_errors.append(
                    f"第{i+1}条记录: 行业名称为空"
                )
            
            # 验证置信度
            if not 0 <= mapping.confidence <= 1:
                self.validation_errors.append(
                    f"第{i+1}条记录: 置信度超出范围 {mapping.confidence}"
                )
    
    def _validate_mapping_logic(self, mappings: List[StockIndustryModel]):
        """验证股票映射数据业务逻辑"""
        # 检查股票代码重复
        stock_codes = [mapping.stock_code for mapping in mappings]
        duplicate_stocks = [code for code in set(stock_codes) if stock_codes.count(code) > 1]
        
        if duplicate_stocks:
            self.validation_warnings.append(f"发现重复股票代码: {duplicate_stocks[:5]}")
        
        # 检查行业名称一致性
        industry_names = {}
        for mapping in mappings:
            if mapping.industry_code:
                if mapping.industry_code not in industry_names:
                    industry_names[mapping.industry_code] = mapping.industry_name
                elif industry_names[mapping.industry_code] != mapping.industry_name:
                    self.validation_warnings.append(
                        f"行业代码 '{mapping.industry_code}' 对应多个行业名称"
                    )
    
    def _validate_mapping_completeness(self, mappings: List[StockIndustryModel]):
        """验证股票映射数据完整性"""
        # 检查数据量
        if len(mappings) < 100:
            self.validation_warnings.append("股票映射数据量较少，可能不完整")
        
        # 检查高置信度数据比例
        high_confidence_count = sum(1 for m in mappings if m.confidence >= 0.8)
        high_confidence_ratio = high_confidence_count / len(mappings) if mappings else 0
        
        if high_confidence_ratio < 0.7:
            self.validation_warnings.append(
                f"高置信度数据比例较低: {high_confidence_ratio:.2%}"
            )
    
    def _is_valid_industry_code(self, code: str) -> bool:
        """验证行业代码格式"""
        if not code:
            return False
        
        # 万得行业代码：6位数字
        if re.match(r'^\d{6}$', code):
            return True
        
        # 申万行业代码：6位数字
        if re.match(r'^\d{6}$', code):
            return True
        
        return False
    
    def _is_valid_stock_code(self, code: str) -> bool:
        """验证股票代码格式"""
        if not code:
            return False
        
        # A股代码：6位数字
        if re.match(r'^\d{6}$', code):
            return True
        
        # 港股代码：4-5位数字
        if re.match(r'^\d{4,5}$', code):
            return True
        
        # 美股代码：字母数字组合
        if re.match(r'^[A-Za-z0-9]+$', code):
            return True
        
        return False
    
    def validate_data_consistency(self, industries: List[IndustryModel], 
                                mappings: List[StockIndustryModel]) -> Tuple[bool, List[str]]:
        """验证行业数据和股票映射数据的一致性"""
        self.validation_errors = []
        self.validation_warnings = []
        
        logger.info("开始验证数据一致性")
        
        # 构建行业代码映射
        industry_map = {ind.industry_code: ind for ind in industries}
        
        # 检查股票映射中的行业代码是否存在于行业数据中
        missing_industries = set()
        for mapping in mappings:
            if mapping.industry_code and mapping.industry_code not in industry_map:
                missing_industries.add(mapping.industry_code)
        
        if missing_industries:
            self.validation_errors.append(
                f"股票映射中存在未定义的行业代码: {list(missing_industries)[:10]}"
            )
        
        # 检查行业名称一致性
        for mapping in mappings:
            if mapping.industry_code in industry_map:
                industry = industry_map[mapping.industry_code]
                if mapping.industry_name != industry.industry_name:
                    self.validation_warnings.append(
                        f"股票 {mapping.stock_code} 的行业名称不一致: "
                        f"映射表='{mapping.industry_name}', 行业表='{industry.industry_name}'"
                    )
        
        is_consistent = len(self.validation_errors) == 0
        logger.info(f"数据一致性验证完成: {'通过' if is_consistent else '失败'}")
        
        return is_consistent, self.validation_errors + self.validation_warnings
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """获取验证结果摘要"""
        return {
            'total_errors': len(self.validation_errors),
            'total_warnings': len(self.validation_warnings),
            'errors': self.validation_errors[:10],  # 只显示前10个错误
            'warnings': self.validation_warnings[:10],  # 只显示前10个警告
            'validation_time': datetime.now().isoformat()
        } 