"""
初始化示例数据
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def init_sample_data():
    """初始化示例数据"""
    try:
        # 导入数据库管理器
        sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
        from database import db_manager
        
        # 示例行业数据
        sample_industries = [
            {
                'industry_code': '010000',
                'industry_name': '农林牧渔',
                'level': 1,
                'parent_code': None,
                'status': 'active'
            },
            {
                'industry_code': '020000',
                'industry_name': '采矿业',
                'level': 1,
                'parent_code': None,
                'status': 'active'
            },
            {
                'industry_code': '030000',
                'industry_name': '制造业',
                'level': 1,
                'parent_code': None,
                'status': 'active'
            },
            {
                'industry_code': '031000',
                'industry_name': '食品饮料',
                'level': 2,
                'parent_code': '030000',
                'status': 'active'
            },
            {
                'industry_code': '032000',
                'industry_name': '纺织服装',
                'level': 2,
                'parent_code': '030000',
                'status': 'active'
            },
            {
                'industry_code': '033000',
                'industry_name': '电子',
                'level': 2,
                'parent_code': '030000',
                'status': 'active'
            },
            {
                'industry_code': '100000',
                'industry_name': '金融业',
                'level': 1,
                'parent_code': None,
                'status': 'active'
            },
            {
                'industry_code': '101000',
                'industry_name': '银行',
                'level': 2,
                'parent_code': '100000',
                'status': 'active'
            }
        ]
        
        # 示例股票数据
        sample_stocks = [
            {
                'stock_code': '000001.SZ',
                'stock_name': '平安银行',
                'industry_code': '101000',
                'industry_name': '银行',
                'mapping_status': 'confirmed',
                'confidence': 0.95
            },
            {
                'stock_code': '000858.SZ',
                'stock_name': '五粮液',
                'industry_code': '031000',
                'industry_name': '食品饮料',
                'mapping_status': 'confirmed',
                'confidence': 0.98
            },
            {
                'stock_code': '002415.SZ',
                'stock_name': '海康威视',
                'industry_code': '033000',
                'industry_name': '电子',
                'mapping_status': 'confirmed',
                'confidence': 0.92
            },
            {
                'stock_code': '600519.SH',
                'stock_name': '贵州茅台',
                'industry_code': '031000',
                'industry_name': '食品饮料',
                'mapping_status': 'confirmed',
                'confidence': 0.99
            }
        ]
        
        # 插入行业数据
        for industry in sample_industries:
            db_manager.insert("wind_industry_classification", industry)
        
        # 插入股票数据
        for stock in sample_stocks:
            db_manager.insert("stock_industry_mapping", stock)
        
        print(f"示例数据添加完成: {len(sample_industries)}个行业, {len(sample_stocks)}只股票")
        return True
        
    except Exception as e:
        print(f"添加示例数据失败: {e}")
        return False

if __name__ == "__main__":
    init_sample_data() 