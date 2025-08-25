"""
数据模型单元测试
测试IndustryModel和StockIndustryModel的功能
"""

import unittest
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.industry_model import IndustryModel, IndustryStatus
from models.stock_industry_model import StockIndustryModel, MappingStatus


class TestIndustryModel(unittest.TestCase):
    """测试行业模型"""
    
    def setUp(self):
        """测试前准备"""
        self.valid_industry = IndustryModel(
            industry_code="010000",
            industry_name="农林牧渔",
            industry_level=1,
            industry_desc="农业、林业、畜牧业、渔业相关行业"
        )
    
    def test_industry_creation(self):
        """测试行业模型创建"""
        self.assertEqual(self.valid_industry.industry_code, "010000")
        self.assertEqual(self.valid_industry.industry_name, "农林牧渔")
        self.assertEqual(self.valid_industry.industry_level, 1)
        self.assertEqual(self.valid_industry.status, IndustryStatus.ACTIVE)
    
    def test_industry_validation(self):
        """测试行业模型验证"""
        # 测试无效的行业代码
        with self.assertRaises(ValueError):
            IndustryModel(
                industry_code="invalid",
                industry_name="测试行业",
                industry_level=1
            )
        
        # 测试无效的行业层级
        with self.assertRaises(ValueError):
            IndustryModel(
                industry_code="010000",
                industry_name="测试行业",
                industry_level=4
            )
        
        # 测试二级行业缺少父级代码
        with self.assertRaises(ValueError):
            IndustryModel(
                industry_code="010100",
                industry_name="农业",
                industry_level=2
            )
    
    def test_industry_to_dict(self):
        """测试行业模型转字典"""
        industry_dict = self.valid_industry.to_dict()
        
        self.assertEqual(industry_dict['industry_code'], "010000")
        self.assertEqual(industry_dict['industry_name'], "农林牧渔")
        self.assertEqual(industry_dict['industry_level'], 1)
        self.assertEqual(industry_dict['status'], "active")
    
    def test_industry_from_dict(self):
        """测试从字典创建行业模型"""
        industry_dict = {
            'industry_code': '020000',
            'industry_name': '采掘',
            'industry_level': 1,
            'status': 'active',
            'source': 'wind'
        }
        
        industry = IndustryModel.from_dict(industry_dict)
        self.assertEqual(industry.industry_code, "020000")
        self.assertEqual(industry.industry_name, "采掘")
        self.assertEqual(industry.status, IndustryStatus.ACTIVE)
    
    def test_industry_hierarchy(self):
        """测试行业层级关系"""
        parent = IndustryModel("010000", "农林牧渔", 1)
        child = IndustryModel("010100", "农业", 2, parent_code="010000")
        
        self.assertTrue(parent.is_parent_of(child))
        self.assertTrue(child.is_child_of(parent))
    
    def test_industry_string_representation(self):
        """测试行业模型字符串表示"""
        industry_str = str(self.valid_industry)
        self.assertIn("010000", industry_str)
        self.assertIn("农林牧渔", industry_str)
        self.assertIn("L1", industry_str)


class TestStockIndustryModel(unittest.TestCase):
    """测试股票行业映射模型"""
    
    def setUp(self):
        """测试前准备"""
        self.valid_mapping = StockIndustryModel(
            stock_code="000001",
            stock_name="平安银行",
            industry_code="080000",
            industry_name="食品饮料",
            industry_level=1,
            confidence=0.95
        )
    
    def test_mapping_creation(self):
        """测试股票映射模型创建"""
        self.assertEqual(self.valid_mapping.stock_code, "000001")
        self.assertEqual(self.valid_mapping.stock_name, "平安银行")
        self.assertEqual(self.valid_mapping.industry_code, "080000")
        self.assertEqual(self.valid_mapping.confidence, 0.95)
        self.assertEqual(self.valid_mapping.status, MappingStatus.ACTIVE)
    
    def test_mapping_validation(self):
        """测试股票映射模型验证"""
        # 测试无效的股票代码
        with self.assertRaises(ValueError):
            StockIndustryModel(
                stock_code="invalid",
                stock_name="测试股票",
                industry_code="080000",
                industry_name="食品饮料",
                industry_level=1
            )
        
        # 测试无效的置信度
        with self.assertRaises(ValueError):
            StockIndustryModel(
                stock_code="000001",
                stock_name="测试股票",
                industry_code="080000",
                industry_name="食品饮料",
                industry_level=1,
                confidence=1.5
            )
    
    def test_mapping_to_dict(self):
        """测试股票映射模型转字典"""
        mapping_dict = self.valid_mapping.to_dict()
        
        self.assertEqual(mapping_dict['stock_code'], "000001")
        self.assertEqual(mapping_dict['stock_name'], "平安银行")
        self.assertEqual(mapping_dict['industry_code'], "080000")
        self.assertEqual(mapping_dict['confidence'], 0.95)
        self.assertEqual(mapping_dict['status'], "active")
    
    def test_mapping_from_dict(self):
        """测试从字典创建股票映射模型"""
        mapping_dict = {
            'stock_code': '000002',
            'stock_name': '万科A',
            'industry_code': '110000',
            'industry_name': '房地产',
            'industry_level': 1,
            'status': 'active',
            'confidence': 0.9
        }
        
        mapping = StockIndustryModel.from_dict(mapping_dict)
        self.assertEqual(mapping.stock_code, "000002")
        self.assertEqual(mapping.stock_name, "万科A")
        self.assertEqual(mapping.confidence, 0.9)
        self.assertEqual(mapping.status, MappingStatus.ACTIVE)
    
    def test_confidence_judgment(self):
        """测试置信度判断"""
        high_confidence = StockIndustryModel(
            "000001", "测试股票", "080000", "食品饮料", 1, confidence=0.9
        )
        low_confidence = StockIndustryModel(
            "000002", "测试股票", "080000", "食品饮料", 1, confidence=0.3
        )
        
        self.assertTrue(high_confidence.is_high_confidence())
        self.assertFalse(low_confidence.is_high_confidence())
        self.assertTrue(low_confidence.is_low_confidence())
    
    def test_mapping_string_representation(self):
        """测试股票映射模型字符串表示"""
        mapping_str = str(self.valid_mapping)
        self.assertIn("000001", mapping_str)
        self.assertIn("080000", mapping_str)
        self.assertIn("0.95", mapping_str)


class TestModelIntegration(unittest.TestCase):
    """测试模型集成"""
    
    def test_industry_stock_relationship(self):
        """测试行业和股票的关联关系"""
        industry = IndustryModel("080000", "食品饮料", 1)
        stock = StockIndustryModel(
            "000001", "平安银行", "080000", "食品饮料", 1
        )
        
        # 验证关联关系
        self.assertEqual(stock.industry_code, industry.industry_code)
        self.assertEqual(stock.industry_name, industry.industry_name)
    
    def test_data_consistency(self):
        """测试数据一致性"""
        industries = [
            IndustryModel("010000", "农林牧渔", 1),
            IndustryModel("020000", "采掘", 1),
        ]
        
        mappings = [
            StockIndustryModel("000001", "平安银行", "010000", "农林牧渔", 1),
            StockIndustryModel("000002", "万科A", "020000", "采掘", 1),
        ]
        
        # 验证映射中的行业代码都存在于行业数据中
        industry_codes = {ind.industry_code for ind in industries}
        mapping_industry_codes = {m.industry_code for m in mappings}
        
        self.assertTrue(mapping_industry_codes.issubset(industry_codes))


if __name__ == '__main__':
    unittest.main() 