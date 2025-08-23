"""
数据库配置文件
统一管理所有模块的数据库配置
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class DatabaseConfig:
    """数据库配置类"""
    
    # 基础配置
    HOST = os.getenv('DB_HOST', 'localhost')
    PORT = int(os.getenv('DB_PORT', 3306))
    USERNAME = os.getenv('DB_USERNAME', 'root')
    PASSWORD = os.getenv('DB_PASSWORD', 'rr1234RR')
    DATABASE = os.getenv('DB_DATABASE', 'pt')
    CHARSET = os.getenv('DB_CHARSET', 'utf8mb4')
    
    # 连接池配置
    MAX_CONNECTIONS = int(os.getenv('DB_MAX_CONNECTIONS', 20))
    MIN_CONNECTIONS = int(os.getenv('DB_MIN_CONNECTIONS', 5))
    CONNECTION_TIMEOUT = int(os.getenv('DB_CONNECTION_TIMEOUT', 30))
    
    @classmethod
    def get_connection_config(cls) -> Dict[str, Any]:
        """获取数据库连接配置"""
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'user': cls.USERNAME,
            'password': cls.PASSWORD,
            'database': cls.DATABASE,
            'charset': cls.CHARSET,
            'autocommit': True
        }
    
    @classmethod
    def get_connection_string(cls) -> str:
        """获取数据库连接字符串"""
        return f"mysql+pymysql://{cls.USERNAME}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DATABASE}?charset={cls.CHARSET}"

# 表名配置 - 按层级和模块组织
class TableNames:
    """表名配置类"""
    
    # 第一层模块 - 数据采集层
    LAYER1 = {
        # 万得行业分类
        'wind_industry': {
            'industry_classification': 'l1_wind_industry_classification',
            'stock_industry_mapping': 'l1_wind_stock_industry_mapping'
        },
        # 公司名字列表
        'company_list': {
            'company_info': 'l1_company_list_info',
            'market_classification': 'l1_company_market_classification'
        },
        # 国内热点数据
        'domestic_hotspot': {
            'hotspot_data': 'l1_domestic_hotspot_data',
            'hotspot_analysis': 'l1_domestic_hotspot_analysis'
        },
        # 国外热点数据
        'foreign_hotspot': {
            'hotspot_data': 'l1_foreign_hotspot_data',
            'hotspot_analysis': 'l1_foreign_hotspot_analysis'
        },
        # 腾讯济安指数
        'tencent_index': {
            'index_data': 'l1_tencent_index_data',
            'index_history': 'l1_tencent_index_history'
        },
        # 雪球等论坛热点数据
        'forum_hotspot': {
            'forum_data': 'l1_forum_hotspot_data',
            'topic_analysis': 'l1_forum_topic_analysis'
        },
        # 其他互联网信息
        'internet_info': {
            'info_data': 'l1_internet_info_data',
            'info_analysis': 'l1_internet_info_analysis'
        }
    }
    
    # 第二层模块 - 数据处理层
    LAYER2 = {
        'company_attributes': {
            'company_attributes': 'l2_company_attributes',
            'attribute_analysis': 'l2_company_attribute_analysis'
        },
        'hotspot_data': {
            'hotspot_summary': 'l2_hotspot_data_summary',
            'hotspot_trends': 'l2_hotspot_trends'
        }
    }
    
    # 第三层模块 - 数据整合层
    LAYER3 = {
        'qcc_data': {
            'company_qcc_data': 'l3_qcc_company_data',
            'qcc_analysis': 'l3_qcc_analysis'
        },
        'tax_bank_report': {
            'tax_data': 'l3_tax_bank_report_data',
            'tax_analysis': 'l3_tax_analysis'
        },
        'financial_statements': {
            'balance_sheet': 'l3_financial_balance_sheet',
            'income_statement': 'l3_financial_income_statement',
            'cash_flow': 'l3_financial_cash_flow'
        },
        'forum_data': {
            'forum_summary': 'l3_forum_data_summary',
            'sentiment_analysis': 'l3_forum_sentiment_analysis'
        }
    }
    
    # 第四层模块 - 数据评分层
    LAYER4 = {
        'company_score': {
            'company_score': 'l4_company_score',
            'score_history': 'l4_company_score_history'
        },
        'industry_score': {
            'industry_score': 'l4_industry_score',
            'score_history': 'l4_industry_score_history'
        },
        'industry_company_score': {
            'industry_company_score': 'l4_industry_company_score',
            'score_history': 'l4_industry_company_score_history'
        }
    }
    
    # 第五层模块 - 权重配置层
    LAYER5 = {
        'factor_weights': {
            'factor_weights': 'l5_factor_weights',
            'weight_history': 'l5_factor_weight_history'
        }
    }
    
    # 第六层模块 - 预测分析层
    LAYER6 = {
        'curve_prediction': {
            'prediction_data': 'l6_curve_prediction_data',
            'prediction_analysis': 'l6_curve_prediction_analysis'
        }
    }
    
    # 系统表
    SYSTEM = {
        'system_logs': 'system_logs',
        'data_flow_logs': 'system_data_flow_logs',
        'module_status': 'system_module_status',
        'data_quality': 'system_data_quality'
    }
    
    @classmethod
    def get_table_name(cls, layer: str, module: str, table: str) -> str:
        """获取表名"""
        layer_tables = getattr(cls, layer.upper(), {})
        module_tables = layer_tables.get(module, {})
        return module_tables.get(table, f"{layer}_{module}_{table}")
    
    @classmethod
    def get_all_tables(cls) -> Dict[str, Dict[str, str]]:
        """获取所有表名"""
        return {
            'LAYER1': cls.LAYER1,
            'LAYER2': cls.LAYER2,
            'LAYER3': cls.LAYER3,
            'LAYER4': cls.LAYER4,
            'LAYER5': cls.LAYER5,
            'LAYER6': cls.LAYER6,
            'SYSTEM': cls.SYSTEM
        }

# 创建全局配置实例
db_config = DatabaseConfig()
table_names = TableNames() 