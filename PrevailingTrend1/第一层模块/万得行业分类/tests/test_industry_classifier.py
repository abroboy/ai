"""
行业分类模块单元测试
测试核心功能的正确性
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime

from ..models.industry_model import IndustryModel, IndustryStatus
from ..models.stock_industry_model import StockIndustryModel, MappingStatus
from ..core.industry_classifier import IndustryClassifier
from ..core.data_validator import DataValidator


class TestIndustryModel(unittest.TestCase):
    """测试行业模型"""
    
    def test_industry_model_creation(self):
        """测试行业模型创建"""
        industry = IndustryModel(
            industry_code="010000",
            industry_name="农林牧渔",
            industry_level=1
        )
        
        self.assertEqual(industry.industry_code, "010000")
        self.assertEqual(industry.industry_name, "农林牧渔")
        self.assertEqual(industry.industry_level, 1)
        self.assertEqual(industry.status, IndustryStatus.ACTIVE)
    
    def test_industry_model_validation(self):
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
    
    def test_industry_model_to_dict(self):
        """测试行业模型转字典"""
        industry = IndustryModel(
            industry_code="010000",
            industry_name="农林牧渔",
            industry_level=1
        )
        
        data = industry.to_dict()
        self.assertEqual(data['industry_code'], "010000")
        self.assertEqual(data['industry_name'], "农林牧渔")
        self.assertEqual(data['industry_level'], 1)
        self.assertEqual(data['status'], "active")


class TestStockIndustryModel(unittest.TestCase):
    """测试股票行业映射模型"""
    
    def test_stock_industry_model_creation(self):
        """测试股票行业映射模型创建"""
        mapping = StockIndustryModel(
            stock_code="000001",
            stock_name="平安银行",
            industry_code="080000",
            industry_name="食品饮料",
            industry_level=1
        )
        
        self.assertEqual(mapping.stock_code, "000001")
        self.assertEqual(mapping.stock_name, "平安银行")
        self.assertEqual(mapping.industry_code, "080000")
        self.assertEqual(mapping.confidence, 1.0)
    
    def test_stock_industry_model_validation(self):
        """测试股票行业映射模型验证"""
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


class TestDataValidator(unittest.TestCase):
    """测试数据验证器"""
    
    def setUp(self):
        """测试前准备"""
        self.validator = DataValidator()
        
        # 创建测试数据
        self.test_industries = [
            IndustryModel("010000", "农林牧渔", 1),
            IndustryModel("020000", "采掘", 1),
            IndustryModel("010100", "农业", 2, parent_code="010000"),
        ]
        
        self.test_mappings = [
            StockIndustryModel("000001", "平安银行", "080000", "食品饮料", 1),
            StockIndustryModel("000002", "万科A", "110000", "房地产", 1),
        ]
    
    def test_validate_industry_data(self):
        """测试行业数据验证"""
        is_valid, issues = self.validator.validate_industry_data(self.test_industries)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
    
    def test_validate_stock_mapping_data(self):
        """测试股票映射数据验证"""
        is_valid, issues = self.validator.validate_stock_mapping_data(self.test_mappings)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
    
    def test_validate_data_consistency(self):
        """测试数据一致性验证"""
        is_consistent, issues = self.validator.validate_data_consistency(
            self.test_industries, self.test_mappings
        )
        
        # 由于测试数据中股票映射的行业代码不在行业数据中，应该有不一致
        self.assertFalse(is_consistent)
        self.assertGreater(len(issues), 0)


class TestIndustryClassifier(unittest.TestCase):
    """测试行业分类器"""
    
    def setUp(self):
        """测试前准备"""
        self.classifier = IndustryClassifier()
    
    @patch('第一层模块.万得行业分类.utils.database.db_manager')
    def test_get_industry_by_code(self, mock_db_manager):
        """测试根据代码获取行业"""
        # 模拟数据库返回结果
        mock_db_manager.execute_query.return_value = [{
            'industry_code': '010000',
            'industry_name': '农林牧渔',
            'industry_level': 1,
            'status': 'active',
            'source': 'wind',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }]
        
        industry = self.classifier.get_industry_by_code("010000")
        
        self.assertIsNotNone(industry)
        self.assertEqual(industry.industry_code, "010000")
        self.assertEqual(industry.industry_name, "农林牧渔")
    
    @patch('第一层模块.万得行业分类.utils.database.db_manager')
    def test_get_industries_by_level(self, mock_db_manager):
        """测试根据层级获取行业列表"""
        # 模拟数据库返回结果
        mock_db_manager.execute_query.return_value = [
            {
                'industry_code': '010000',
                'industry_name': '农林牧渔',
                'industry_level': 1,
                'status': 'active',
                'source': 'wind',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'industry_code': '020000',
                'industry_name': '采掘',
                'industry_level': 1,
                'status': 'active',
                'source': 'wind',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        ]
        
        industries = self.classifier.get_industries_by_level(1)
        
        self.assertEqual(len(industries), 2)
        self.assertEqual(industries[0].industry_code, "010000")
        self.assertEqual(industries[1].industry_code, "020000")
    
    @patch('第一层模块.万得行业分类.utils.database.db_manager')
    def test_search_industries(self, mock_db_manager):
        """测试搜索行业"""
        # 模拟数据库返回结果
        mock_db_manager.execute_query.return_value = [
            {
                'industry_code': '060000',
                'industry_name': '电子',
                'industry_level': 1,
                'status': 'active',
                'source': 'wind',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        ]
        
        results = self.classifier.search_industries("电子")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].industry_name, "电子")
    
    @patch('第一层模块.万得行业分类.utils.database.db_manager')
    def test_get_industry_statistics(self, mock_db_manager):
        """测试获取统计信息"""
        # 模拟数据库返回结果
        mock_db_manager.execute_query.return_value = [
            {'count': 10},
            {'count': 50},
            {'count': 100}
        ]
        
        stats = self.classifier.get_industry_statistics()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('last_update', stats)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        classifier = IndustryClassifier()
        validator = DataValidator()
        
        # 创建测试数据
        test_industries = [
            IndustryModel("010000", "农林牧渔", 1),
            IndustryModel("020000", "采掘", 1),
        ]
        
        test_mappings = [
            StockIndustryModel("000001", "平安银行", "010000", "农林牧渔", 1),
        ]
        
        # 验证数据
        industry_valid, _ = validator.validate_industry_data(test_industries)
        mapping_valid, _ = validator.validate_stock_mapping_data(test_mappings)
        consistency_valid, _ = validator.validate_data_consistency(test_industries, test_mappings)
        
        self.assertTrue(industry_valid)
        self.assertTrue(mapping_valid)
        self.assertTrue(consistency_valid)


if __name__ == '__main__':
    unittest.main() 