"""
数据验证器单元测试
测试SimpleValidator的功能
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.simple_validator import SimpleValidator
from models.industry_model import IndustryModel
from models.stock_industry_model import StockIndustryModel


class TestSimpleValidator(unittest.TestCase):
    """测试简单验证器"""
    
    def setUp(self):
        """测试前准备"""
        self.validator = SimpleValidator()
        
        # 创建测试数据
        self.valid_industries = [
            IndustryModel("010000", "农林牧渔", 1),
            IndustryModel("020000", "采掘", 1),
            IndustryModel("010100", "农业", 2, parent_code="010000"),
        ]
        
        self.valid_mappings = [
            StockIndustryModel("000001", "平安银行", "080000", "食品饮料", 1),
            StockIndustryModel("000002", "万科A", "110000", "房地产", 1),
        ]
    
    def test_validate_industry_data_valid(self):
        """测试验证有效的行业数据"""
        is_valid, issues = self.validator.validate_industry_data(self.valid_industries)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
    
    def test_validate_industry_data_invalid(self):
        """测试验证无效的行业数据"""
        invalid_industries = [
            IndustryModel("", "农林牧渔", 1),  # 空行业代码
            IndustryModel("020000", "", 1),    # 空行业名称
            IndustryModel("030000", "化工", 4), # 无效层级
        ]
        
        is_valid, issues = self.validator.validate_industry_data(invalid_industries)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)
        
        # 检查具体的错误信息
        error_messages = [issue for issue in issues if "错误" in issue or "无效" in issue]
        self.assertGreater(len(error_messages), 0)
    
    def test_validate_industry_data_insufficient(self):
        """测试验证数据量不足的行业数据"""
        insufficient_industries = [
            IndustryModel("010000", "农林牧渔", 1),
        ]
        
        is_valid, issues = self.validator.validate_industry_data(insufficient_industries)
        
        self.assertTrue(is_valid)  # 数据格式正确
        self.assertGreater(len(issues), 0)  # 但有警告
        
        # 检查警告信息
        warning_messages = [issue for issue in issues if "较少" in issue]
        self.assertGreater(len(warning_messages), 0)
    
    def test_validate_stock_mapping_data_valid(self):
        """测试验证有效的股票映射数据"""
        is_valid, issues = self.validator.validate_stock_mapping_data(self.valid_mappings)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
    
    def test_validate_stock_mapping_data_invalid(self):
        """测试验证无效的股票映射数据"""
        invalid_mappings = [
            StockIndustryModel("", "平安银行", "080000", "食品饮料", 1),  # 空股票代码
            StockIndustryModel("000001", "", "080000", "食品饮料", 1),    # 空股票名称
            StockIndustryModel("000002", "万科A", "110000", "", 1),       # 空行业名称
            StockIndustryModel("000003", "测试", "120000", "测试行业", 1, confidence=1.5),  # 无效置信度
        ]
        
        is_valid, issues = self.validator.validate_stock_mapping_data(invalid_mappings)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)
    
    def test_validate_stock_mapping_data_insufficient(self):
        """测试验证数据量不足的股票映射数据"""
        insufficient_mappings = [
            StockIndustryModel("000001", "平安银行", "080000", "食品饮料", 1),
        ]
        
        is_valid, issues = self.validator.validate_stock_mapping_data(insufficient_mappings)
        
        self.assertTrue(is_valid)  # 数据格式正确
        self.assertGreater(len(issues), 0)  # 但有警告
        
        # 检查警告信息
        warning_messages = [issue for issue in issues if "较少" in issue]
        self.assertGreater(len(warning_messages), 0)
    
    def test_validate_confidence_range(self):
        """测试置信度范围验证"""
        # 测试边界值
        valid_mappings = [
            StockIndustryModel("000001", "测试1", "080000", "食品饮料", 1, confidence=0.0),
            StockIndustryModel("000002", "测试2", "080000", "食品饮料", 1, confidence=0.5),
            StockIndustryModel("000003", "测试3", "080000", "食品饮料", 1, confidence=1.0),
        ]
        
        is_valid, issues = self.validator.validate_stock_mapping_data(valid_mappings)
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
        
        # 测试无效值
        invalid_mappings = [
            StockIndustryModel("000001", "测试1", "080000", "食品饮料", 1, confidence=-0.1),
            StockIndustryModel("000002", "测试2", "080000", "食品饮料", 1, confidence=1.1),
        ]
        
        is_valid, issues = self.validator.validate_stock_mapping_data(invalid_mappings)
        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)
    
    def test_validate_industry_level_range(self):
        """测试行业层级范围验证"""
        # 测试有效层级
        valid_industries = [
            IndustryModel("010000", "农林牧渔", 1),
            IndustryModel("010100", "农业", 2, parent_code="010000"),
            IndustryModel("010101", "种植业", 3, parent_code="010100"),
        ]
        
        is_valid, issues = self.validator.validate_industry_data(valid_industries)
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
        
        # 测试无效层级
        invalid_industries = [
            IndustryModel("010000", "农林牧渔", 0),  # 层级为0
            IndustryModel("020000", "采掘", 4),      # 层级为4
        ]
        
        is_valid, issues = self.validator.validate_industry_data(invalid_industries)
        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)
    
    def test_validate_empty_data(self):
        """测试验证空数据"""
        # 测试空行业数据
        is_valid, issues = self.validator.validate_industry_data([])
        self.assertTrue(is_valid)  # 空数据格式上有效
        self.assertGreater(len(issues), 0)  # 但有警告
        
        # 测试空股票映射数据
        is_valid, issues = self.validator.validate_stock_mapping_data([])
        self.assertTrue(is_valid)  # 空数据格式上有效
        self.assertGreater(len(issues), 0)  # 但有警告
    
    def test_validate_large_dataset(self):
        """测试验证大数据集"""
        # 创建大量有效数据
        large_industries = []
        for i in range(100):
            industry = IndustryModel(
                f"{i:06d}", 
                f"行业{i}", 
                1
            )
            large_industries.append(industry)
        
        large_mappings = []
        for i in range(200):
            mapping = StockIndustryModel(
                f"{i:06d}", 
                f"股票{i}", 
                f"{i//10:06d}", 
                f"行业{i//10}", 
                1
            )
            large_mappings.append(mapping)
        
        # 验证大数据集
        is_valid, issues = self.validator.validate_industry_data(large_industries)
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
        
        is_valid, issues = self.validator.validate_stock_mapping_data(large_mappings)
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)


class TestValidatorEdgeCases(unittest.TestCase):
    """测试验证器边界情况"""
    
    def setUp(self):
        """测试前准备"""
        self.validator = SimpleValidator()
    
    def test_validate_special_characters(self):
        """测试特殊字符处理"""
        # 测试包含特殊字符的数据
        special_industries = [
            IndustryModel("010000", "农林牧渔(农业)", 1),
            IndustryModel("020000", "采掘-矿业", 1),
            IndustryModel("030000", "化工&化学", 1),
        ]
        
        is_valid, issues = self.validator.validate_industry_data(special_industries)
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
    
    def test_validate_unicode_characters(self):
        """测试Unicode字符处理"""
        # 测试Unicode字符
        unicode_industries = [
            IndustryModel("010000", "农林牧渔", 1),
            IndustryModel("020000", "采掘业", 1),
            IndustryModel("030000", "化工业", 1),
        ]
        
        is_valid, issues = self.validator.validate_industry_data(unicode_industries)
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
    
    def test_validate_whitespace_handling(self):
        """测试空白字符处理"""
        # 测试包含空白字符的数据
        whitespace_industries = [
            IndustryModel("010000", " 农林牧渔 ", 1),  # 前后空格
            IndustryModel("020000", "采掘", 1),
        ]
        
        is_valid, issues = self.validator.validate_industry_data(whitespace_industries)
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)


if __name__ == '__main__':
    unittest.main() 