#!/usr/bin/env python3
"""
万得行业分类模块数据库初始化脚本
包含行业分类数据和股票映射数据的创建和初始化
"""

import pymysql
from datetime import datetime
import sys
import os

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rr1234RR',
    'database': 'pt',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def create_industry_classification_table():
    """创建万得行业分类表"""
    print("创建万得行业分类表...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # 创建行业分类表
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS l1_wind_industry_classification (
            industry_code VARCHAR(50) PRIMARY KEY COMMENT '行业代码',
            industry_name VARCHAR(200) NOT NULL COMMENT '行业名称',
            industry_level INT DEFAULT 1 COMMENT '行业级别',
            parent_industry_code VARCHAR(50) DEFAULT NULL COMMENT '父行业代码',
            industry_description TEXT COMMENT '行业描述',
            is_active BOOLEAN DEFAULT TRUE COMMENT '是否活跃',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            INDEX idx_industry_level (industry_level),
            INDEX idx_parent_code (parent_industry_code),
            INDEX idx_is_active (is_active)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='万得行业分类表'
        """
        cursor.execute(create_table_sql)
        print("✓ 万得行业分类表创建成功")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"✗ 创建万得行业分类表失败: {e}")
        return False

def create_listed_company_table():
    """创建上市公司信息表"""
    print("创建上市公司信息表...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS l1_listed_company_info (
            stock_code VARCHAR(20) PRIMARY KEY COMMENT '股票代码',
            company_name VARCHAR(200) NOT NULL COMMENT '公司名称',
            stock_name VARCHAR(100) NOT NULL COMMENT '股票名称',
            market_type VARCHAR(20) DEFAULT 'A股' COMMENT '市场类型',
            exchange_code VARCHAR(10) COMMENT '交易所代码',
            industry_code VARCHAR(50) COMMENT '行业代码',
            industry_name VARCHAR(200) COMMENT '行业名称',
            sector_code VARCHAR(50) COMMENT '板块代码',
            sector_name VARCHAR(200) COMMENT '板块名称',
            listing_date DATE COMMENT '上市日期',
            total_share_capital DECIMAL(20,2) COMMENT '总股本(万股)',
            circulating_share_capital DECIMAL(20,2) COMMENT '流通股本(万股)',
            total_market_value DECIMAL(20,2) COMMENT '总市值(万元)',
            circulating_market_value DECIMAL(20,2) COMMENT '流通市值(万元)',
            latest_price DECIMAL(10,3) COMMENT '最新价格',
            pe_ratio DECIMAL(8,2) COMMENT '市盈率',
            pb_ratio DECIMAL(8,2) COMMENT '市净率',
            eps DECIMAL(8,3) COMMENT '每股收益',
            bps DECIMAL(8,3) COMMENT '每股净资产',
            roe DECIMAL(8,4) COMMENT '净资产收益率',
            roa DECIMAL(8,4) COMMENT '资产收益率',
            dividend_yield DECIMAL(8,4) COMMENT '股息率',
            is_st BOOLEAN DEFAULT FALSE COMMENT '是否ST股票',
            is_suspended BOOLEAN DEFAULT FALSE COMMENT '是否停牌',
            is_active BOOLEAN DEFAULT TRUE COMMENT '是否活跃',
            business_scope TEXT COMMENT '经营范围',
            company_address VARCHAR(500) COMMENT '公司地址',
            registered_capital DECIMAL(20,2) COMMENT '注册资本(万元)',
            employee_count INT COMMENT '员工人数',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            INDEX idx_market_type (market_type),
            INDEX idx_industry_code (industry_code),
            INDEX idx_is_active (is_active)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='上市公司信息表'
        """
        cursor.execute(create_table_sql)
        print("✓ 上市公司信息表创建成功")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"✗ 创建上市公司信息表失败: {e}")
        return False

def create_hk_connect_table():
    """创建港股通表"""
    print("创建港股通表...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS l1_hk_connect_stock (
            stock_code VARCHAR(20) PRIMARY KEY COMMENT '港股代码',
            stock_name_cn VARCHAR(200) COMMENT '中文名称',
            stock_name_en VARCHAR(200) COMMENT '英文名称',
            connect_type VARCHAR(20) COMMENT '港股通类型',
            inclusion_date DATE COMMENT '纳入日期',
            market_type VARCHAR(20) DEFAULT '港股' COMMENT '市场类型',
            board_type VARCHAR(20) COMMENT '板块类型',
            industry_code VARCHAR(50) COMMENT '行业代码',
            industry_name VARCHAR(200) COMMENT '行业名称',
            sector_code VARCHAR(50) COMMENT '板块代码',
            sector_name VARCHAR(200) COMMENT '板块名称',
            listing_date DATE COMMENT '上市日期',
            total_shares DECIMAL(20,2) COMMENT '总股本(万股)',
            circulating_shares DECIMAL(20,2) COMMENT '流通股本(万股)',
            latest_price_hkd DECIMAL(10,3) COMMENT '最新价格(港币)',
            latest_price_rmb DECIMAL(10,3) COMMENT '最新价格(人民币)',
            market_value_hkd DECIMAL(20,2) COMMENT '市值(港币万元)',
            market_value_rmb DECIMAL(20,2) COMMENT '市值(人民币万元)',
            pe_ratio DECIMAL(8,2) COMMENT '市盈率',
            pb_ratio DECIMAL(8,2) COMMENT '市净率',
            dividend_yield DECIMAL(8,4) COMMENT '股息率',
            northbound_net_inflow DECIMAL(20,2) COMMENT '北向资金净流入(万元)',
            northbound_holding_ratio DECIMAL(8,4) COMMENT '北向持股比例',
            daily_turnover_hkd DECIMAL(20,2) COMMENT '日成交额(港币万元)',
            daily_turnover_rmb DECIMAL(20,2) COMMENT '日成交额(人民币万元)',
            daily_quota_usage DECIMAL(8,4) COMMENT '每日额度使用率',
            exchange_rate_hkd_rmb DECIMAL(8,4) COMMENT '港币人民币汇率',
            is_active BOOLEAN DEFAULT TRUE COMMENT '是否在港股通名单中',
            is_suspended BOOLEAN DEFAULT FALSE COMMENT '是否停牌',
            risk_warning VARCHAR(200) COMMENT '风险警示',
            trading_currency VARCHAR(10) DEFAULT 'HKD' COMMENT '交易货币',
            lot_size INT COMMENT '每手股数',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            INDEX idx_connect_type (connect_type),
            INDEX idx_industry_code (industry_code),
            INDEX idx_is_active (is_active)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='港股通股票信息表'
        """
        cursor.execute(create_table_sql)
        print("✓ 港股通表创建成功")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"✗ 创建港股通表失败: {e}")
        return False

def create_capital_flow_table():
    """创建股票资金流向表"""
    print("创建股票资金流向表...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS l1_stock_capital_flow (
            stock_code VARCHAR(20) NOT NULL COMMENT '股票代码',
            trade_date DATE NOT NULL COMMENT '交易日期',
            stock_name VARCHAR(100) COMMENT '股票名称',
            market_type VARCHAR(20) COMMENT '市场类型',
            close_price DECIMAL(10,3) COMMENT '收盘价',
            price_change DECIMAL(10,3) COMMENT '涨跌额',
            price_change_ratio DECIMAL(8,4) COMMENT '涨跌幅',
            turnover_amount DECIMAL(20,2) COMMENT '成交额(万元)',
            turnover_volume DECIMAL(20,2) COMMENT '成交量(万股)',
            main_net_inflow DECIMAL(20,2) COMMENT '主力净流入(万元)',
            main_net_inflow_ratio DECIMAL(8,4) COMMENT '主力净流入占比',
            super_large_net_inflow DECIMAL(20,2) COMMENT '超大单净流入(万元)',
            large_net_inflow DECIMAL(20,2) COMMENT '大单净流入(万元)',
            medium_net_inflow DECIMAL(20,2) COMMENT '中单净流入(万元)',
            small_net_inflow DECIMAL(20,2) COMMENT '小单净流入(万元)',
            super_large_inflow DECIMAL(20,2) COMMENT '超大单流入(万元)',
            super_large_outflow DECIMAL(20,2) COMMENT '超大单流出(万元)',
            large_inflow DECIMAL(20,2) COMMENT '大单流入(万元)',
            large_outflow DECIMAL(20,2) COMMENT '大单流出(万元)',
            medium_inflow DECIMAL(20,2) COMMENT '中单流入(万元)',
            medium_outflow DECIMAL(20,2) COMMENT '中单流出(万元)',
            small_inflow DECIMAL(20,2) COMMENT '小单流入(万元)',
            small_outflow DECIMAL(20,2) COMMENT '小单流出(万元)',
            institutional_net_inflow DECIMAL(20,2) COMMENT '机构净流入(万元)',
            retail_net_inflow DECIMAL(20,2) COMMENT '散户净流入(万元)',
            northbound_net_inflow DECIMAL(20,2) COMMENT '北向资金净流入(万元)',
            southbound_net_inflow DECIMAL(20,2) COMMENT '南向资金净流入(万元)',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            PRIMARY KEY (stock_code, trade_date),
            INDEX idx_trade_date (trade_date),
            INDEX idx_market_type (market_type),
            INDEX idx_main_net_inflow (main_net_inflow)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票资金流向数据表'
        """
        cursor.execute(create_table_sql)
        print("✓ 股票资金流向表创建成功")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"✗ 创建股票资金流向表失败: {e}")
        return False

def create_stock_mapping_table():
    """创建股票映射表"""
    print("创建股票映射表...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # 创建股票映射表
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS l1_wind_stock_mapping (
            id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
            stock_code VARCHAR(20) NOT NULL COMMENT '股票代码',
            stock_name VARCHAR(100) NOT NULL COMMENT '股票名称',
            market_type VARCHAR(20) DEFAULT 'A股' COMMENT '市场类型',
            industry_code VARCHAR(50) COMMENT '所属行业代码',
            industry_name VARCHAR(200) COMMENT '所属行业名称',
            mapping_status VARCHAR(20) DEFAULT '已映射' COMMENT '映射状态',
            total_market_value DECIMAL(20,2) COMMENT '总市值(万)',
            daily_net_inflow DECIMAL(20,2) COMMENT '日资金净流入(万)',
            net_inflow_ratio DECIMAL(8,4) COMMENT '流入比例(%)',
            recent_volatility DECIMAL(8,4) COMMENT '最近波动率',
            latest_7d_inflow DECIMAL(20,2) COMMENT '最近7日流入(万)',
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
            operation_status VARCHAR(20) DEFAULT '正常' COMMENT '操作状态',
            is_active BOOLEAN DEFAULT TRUE COMMENT '是否活跃',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            UNIQUE KEY uk_stock_code (stock_code),
            KEY idx_industry_code (industry_code),
            KEY idx_market_type (market_type),
            KEY idx_mapping_status (mapping_status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='万得股票映射管理表'
        """
        cursor.execute(create_table_sql)
        print("✓ 股票映射表创建成功")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"✗ 创建股票映射表失败: {e}")
        return False

def init_industry_data():
    """初始化行业分类数据"""
    print("初始化万得行业分类数据...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # 检查是否已有数据
        cursor.execute("SELECT COUNT(*) FROM l1_wind_industry_classification")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"✓ 行业分类数据已存在 ({count} 条记录)")
            cursor.close()
            connection.close()
            return True
        
        # 一级行业分类数据
        level1_industries = [
            ('110000', '石油石化', 1, None, '一级行业: 石油石化'),
            ('210000', '有色金属', 1, None, '一级行业: 有色金属'),
            ('220000', '钢铁', 1, None, '一级行业: 钢铁'),
            ('230000', '基础化工', 1, None, '一级行业: 基础化工'),
            ('240000', '建筑材料', 1, None, '一级行业: 建筑材料'),
            ('270000', '机械设备', 1, None, '一级行业: 机械设备'),
            ('280000', '电力设备', 1, None, '一级行业: 电力设备'),
            ('330000', '家用电器', 1, None, '一级行业: 家用电器'),
            ('350000', '计算机', 1, None, '一级行业: 计算机'),
            ('360000', '电子', 1, None, '一级行业: 电子'),
            ('370000', '通信', 1, None, '一级行业: 通信'),
            ('410000', '电力及公用事业', 1, None, '一级行业: 电力及公用事业'),
            ('420000', '交通运输', 1, None, '一级行业: 交通运输'),
            ('430000', '房地产', 1, None, '一级行业: 房地产'),
            ('450000', '商业贸易', 1, None, '一级行业: 商业贸易'),
            ('460000', '休闲服务', 1, None, '一级行业: 休闲服务'),
            ('480000', '银行', 1, None, '一级行业: 银行'),
            ('490000', '非银金融', 1, None, '一级行业: 非银金融'),
            ('510000', '综合', 1, None, '一级行业: 综合'),
            ('610000', '食品饮料', 1, None, '一级行业: 食品饮料'),
            ('620000', '纺织服装', 1, None, '一级行业: 纺织服装'),
            ('630000', '轻工制造', 1, None, '一级行业: 轻工制造'),
            ('640000', '金融服务', 1, None, '一级行业: 金融服务'),
            ('710000', '社服', 1, None, '一级行业: 社服'),
            ('720000', '传媒', 1, None, '一级行业: 传媒'),
        ]
        
        # 二级行业分类数据
        level2_industries = [
            ('110100', '石油开采', 2, '110000', '二级行业: 石油开采'),
            ('110200', '石油加工', 2, '110000', '二级行业: 石油加工'),
            ('110300', '化学原料', 2, '110000', '二级行业: 化学原料'),
            ('210100', '黄金', 2, '210000', '二级行业: 黄金'),
            ('210200', '铜', 2, '210000', '二级行业: 铜'),
            ('210300', '铝', 2, '210000', '二级行业: 铝'),
            ('220100', '钢铁', 2, '220000', '二级行业: 钢铁'),
            ('270100', '机械基础件', 2, '270000', '二级行业: 机械基础件'),
            ('270200', '通用机械', 2, '270000', '二级行业: 通用机械'),
            ('280100', '电机', 2, '280000', '二级行业: 电机'),
            ('330100', '白色家电', 2, '330000', '二级行业: 白色家电'),
            ('350100', '计算机设备', 2, '350000', '二级行业: 计算机设备'),
            ('360100', '半导体', 2, '360000', '二级行业: 半导体'),
            ('370100', '通信设备', 2, '370000', '二级行业: 通信设备'),
            ('410100', '电力', 2, '410000', '二级行业: 电力'),
            ('430100', '房地产开发', 2, '430000', '二级行业: 房地产开发'),
            ('480100', '银行', 2, '480000', '二级行业: 银行'),
            ('610100', '食品加工', 2, '610000', '二级行业: 食品加工'),
            ('610200', '饮料制造', 2, '610000', '二级行业: 饮料制造'),
            ('610300', '白酒', 2, '610000', '二级行业: 白酒'),
        ]
        
        # 合并所有数据
        all_industries = level1_industries + level2_industries
        
        # 插入数据
        insert_sql = """
        INSERT INTO l1_wind_industry_classification 
        (industry_code, industry_name, industry_level, parent_industry_code, industry_description, is_active)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        for industry in all_industries:
            cursor.execute(insert_sql, industry + (True,))
        
        connection.commit()
        print(f"✓ 成功插入 {len(all_industries)} 条行业分类数据")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"✗ 初始化行业分类数据失败: {e}")
        return False

def init_stock_mapping_data():
    """初始化股票映射数据"""
    print("初始化股票映射数据...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # 检查是否已有数据
        cursor.execute("SELECT COUNT(*) FROM l1_wind_stock_mapping")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"清理现有股票映射数据 ({count} 条记录)")
            cursor.execute("DELETE FROM l1_wind_stock_mapping")
            cursor.execute("ALTER TABLE l1_wind_stock_mapping AUTO_INCREMENT = 1")
            connection.commit()
        
        # 股票映射测试数据 - 扩展到200+只股票
        import random
        
        stock_data = [
            # 银行股 (15只)
            ('000001', '平安银行', 'A股', '480100', '银行', '已映射', 285050, 12500.30, 3.25, 0.0285, 87500.50, '正常'),
            ('600036', '招商银行', 'A股', '480100', '银行', '已映射', 852080, -8900.20, -2.15, 0.0195, -62300.40, '正常'),
            ('601398', '工商银行', 'A股', '480100', '银行', '已映射', 1852060, 15600.80, 1.85, 0.0165, 109200.60, '正常'),
            ('600000', '浦发银行', 'A股', '480100', '银行', '已映射', 195060, -2800.30, -1.85, 0.0325, -19600.90, '正常'),
            ('601988', '中国银行', 'A股', '480100', '银行', '已映射', 1625400, 8950.20, 2.15, 0.0225, 62600.40, '正常'),
            ('601939', '建设银行', 'A股', '480100', '银行', '已映射', 2145600, 12850.60, 1.95, 0.0185, 89900.20, '正常'),
            ('600016', '民生银行', 'A股', '480100', '银行', '已映射', 156200, -5600.40, -2.85, 0.0385, -39200.80, '正常'),
            ('002142', '宁波银行', 'A股', '480100', '银行', '已映射', 325800, 18950.30, 4.25, 0.0345, 132600.10, '正常'),
            ('600015', '华夏银行', 'A股', '480100', '银行', '已映射', 89500, -3250.60, -1.95, 0.0295, -22750.20, '正常'),
            ('000783', '长江证券', 'A股', '490000', '非银金融', '已映射', 45600, 2850.40, 2.65, 0.0425, 19950.80, '正常'),
            ('600919', '江苏银行', 'A股', '480100', '银行', '已映射', 125800, 6950.20, 3.15, 0.0285, 48650.40, '正常'),
            ('601818', '光大银行', 'A股', '480100', '银行', '已映射', 185600, -4250.30, -1.65, 0.0315, -29750.10, '正常'),
            ('002807', '江阴银行', 'A股', '480100', '银行', '已映射', 12500, 850.60, 3.85, 0.0495, 5950.20, '正常'),
            ('600926', '杭州银行', 'A股', '480100', '银行', '已映射', 65400, 3250.80, 2.95, 0.0365, 22750.60, '正常'),
            ('002936', '郑州银行', 'A股', '480100', '银行', '已映射', 18900, -1250.40, -2.15, 0.0445, -8750.80, '正常'),
            
            # 白酒股 (12只)
            ('600519', '贵州茅台', 'A股', '610300', '白酒', '已映射', 2580090, 32500.60, 4.85, 0.0385, 227500.20, '正常'),
            ('000858', '五粮液', 'A股', '610300', '白酒', '已映射', 890040, -5200.30, -1.95, 0.0295, -36400.90, '正常'),
            ('000596', '古井贡酒', 'A股', '610300', '白酒', '已映射', 185020, 3600.40, 2.65, 0.0445, 25200.80, '正常'),
            ('000568', '泸州老窖', 'A股', '610300', '白酒', '已映射', 425600, 18950.80, 3.95, 0.0355, 132600.60, '正常'),
            ('002304', '洋河股份', 'A股', '610300', '白酒', '已映射', 325800, -8600.20, -2.35, 0.0325, -60200.40, '正常'),
            ('600809', '山西汾酒', 'A股', '610300', '白酒', '已映射', 285600, 12850.40, 3.25, 0.0385, 89950.80, '正常'),
            ('000799', '酒鬼酒', 'A股', '610300', '白酒', '已映射', 95400, 4250.60, 4.15, 0.0465, 29750.20, '正常'),
            ('600702', '舍得酒业', 'A股', '610300', '白酒', '已映射', 45800, -2150.30, -3.25, 0.0485, -15050.10, '正常'),
            ('000860', '顺鑫农业', 'A股', '610300', '白酒', '已映射', 65200, 1850.40, 2.15, 0.0415, 12950.80, '正常'),
            ('603589', '口子窖', 'A股', '610300', '白酒', '已映射', 125600, 6850.20, 3.85, 0.0395, 47950.40, '正常'),
            ('000752', '西藏发展', 'A股', '610300', '白酒', '已映射', 25400, -1350.60, -2.95, 0.0455, -9450.20, '正常'),
            ('600559', '老白干酒', 'A股', '610300', '白酒', '已映射', 35800, 2450.80, 3.45, 0.0425, 17150.60, '正常'),
            
            # 科技股 (20只)
            ('000725', '京东方A', 'A股', '360100', '半导体', '已映射', 195030, -2800.50, -3.15, 0.0525, -19600.50, '正常'),
            ('002415', '海康威视', 'A股', '360100', '半导体', '已映射', 325080, 8900.20, 3.85, 0.0385, 62300.40, '正常'),
            ('300015', '爱尔眼科', 'A股', '640000', '金融服务', '已映射', 210050, -1200.30, -1.25, 0.0355, -8400.90, '正常'),
            ('000063', '中兴通讯', 'A股', '370100', '通信设备', '已映射', 285600, 15850.40, 4.25, 0.0395, 110950.80, '正常'),
            ('002230', '科大讯飞', 'A股', '350100', '计算机设备', '已映射', 165400, 9250.60, 3.65, 0.0445, 64750.20, '正常'),
            ('300059', '东方财富', 'A股', '490000', '非银金融', '已映射', 1564000, 3250.80, 2.29, 0.0352, 18900.60, '正常'),
            ('002475', '立讯精密', 'A股', '360100', '半导体', '已映射', 285900, 12650.40, 3.95, 0.0365, 88550.80, '正常'),
            ('300750', '宁德时代', 'A股', '280100', '电机', '已映射', 1258600, 45850.60, 5.85, 0.0485, 320950.20, '正常'),
            ('300033', '同花顺', 'A股', '350100', '计算机设备', '已映射', 185600, 8950.20, 3.25, 0.0425, 62650.40, '正常'),
            ('002714', '牧原股份', 'A股', '610000', '食品饮料', '已映射', 325800, -18950.60, -4.25, 0.0565, -132650.20, '正常'),
            ('600584', '长电科技', 'A股', '360100', '半导体', '已映射', 95400, 4250.80, 2.85, 0.0445, 29750.60, '正常'),
            ('000776', '广发证券', 'A股', '490000', '非银金融', '已映射', 285600, -6850.40, -2.35, 0.0385, -47950.80, '正常'),
            ('300003', '乐普医疗', 'A股', '610000', '食品饮料', '已映射', 125800, 5650.20, 3.45, 0.0415, 39550.40, '正常'),
            ('300142', '沃森生物', 'A股', '610000', '食品饮料', '已映射', 85600, -3250.60, -2.85, 0.0485, -22750.20, '正常'),
            ('002371', '北方华创', 'A股', '360100', '半导体', '已映射', 385600, 25850.40, 5.25, 0.0445, 180950.80, '正常'),
            ('688981', '中芯国际', '科创板', '360100', '半导体', '已映射', 1285600, 35650.80, 4.85, 0.0525, 249550.60, '正常'),
            ('002049', '紫光国微', 'A股', '360100', '半导体', '已映射', 195400, 8950.60, 3.65, 0.0465, 62650.20, '正常'),
            ('300496', '中科创达', 'A股', '350100', '计算机设备', '已映射', 125600, 6850.40, 4.15, 0.0485, 47950.80, '正常'),
            ('300782', '卓胜微', 'A股', '360100', '半导体', '已映射', 285600, 12850.60, 3.95, 0.0425, 89950.20, '正常'),
            ('603986', '兆易创新', 'A股', '360100', '半导体', '已映射', 165400, 7850.20, 3.25, 0.0445, 54950.40, '正常'),
            
            # 新能源汽车 (15只)
            ('002594', '比亚迪', 'A股', '420000', '交通运输', '已映射', 785060, 25800.90, 5.65, 0.0485, 180600.30, '正常'),
            ('600104', '上汽集团', 'A股', '420000', '交通运输', '已映射', 295040, -3600.20, -2.85, 0.0425, -25200.40, '正常'),
            ('000625', '长安汽车', 'A股', '420000', '交通运输', '已映射', 165080, 4500.60, 3.95, 0.0535, 31500.20, '正常'),
            ('600066', '宇通客车', 'A股', '420000', '交通运输', '已映射', 125600, 3850.40, 2.85, 0.0445, 26950.80, '正常'),
            ('000868', '安凯客车', 'A股', '420000', '交通运输', '已映射', 25400, -1250.60, -3.25, 0.0565, -8750.20, '正常'),
            ('002460', '赣锋锂业', 'A股', '210000', '有色金属', '已映射', 385600, 18950.80, 4.25, 0.0485, 132650.60, '正常'),
            ('300014', '亿纬锂能', 'A股', '280100', '电机', '已映射', 285600, 12850.40, 3.65, 0.0425, 89950.80, '正常'),
            ('002812', '恩捷股份', 'A股', '230000', '基础化工', '已映射', 195400, 8950.60, 3.85, 0.0465, 62650.20, '正常'),
            ('300073', '当升科技', 'A股', '230000', '基础化工', '已映射', 125600, 5850.20, 4.15, 0.0485, 40950.40, '正常'),
            ('002050', '三花智控', 'A股', '270100', '机械基础件', '已映射', 165400, 7850.40, 3.25, 0.0415, 54950.80, '正常'),
            ('000951', '中国重汽', 'A股', '420000', '交通运输', '已映射', 85600, -2850.60, -2.65, 0.0445, -19950.20, '正常'),
            ('601633', '长城汽车', 'A股', '420000', '交通运输', '已映射', 235600, 9850.40, 3.55, 0.0455, 68950.80, '正常'),
            ('000550', '江铃汽车', 'A股', '420000', '交通运输', '已映射', 95400, 3250.80, 2.95, 0.0435, 22750.60, '正常'),
            ('600213', '亚星客车', 'A股', '420000', '交通运输', '已映射', 35800, -1650.40, -3.85, 0.0585, -11550.80, '正常'),
            ('000957', '中通客车', 'A股', '420000', '交通运输', '已映射', 45600, 1850.60, 3.15, 0.0525, 12950.20, '正常'),
            
            # 房地产 (10只)
            ('000002', '万科A', 'A股', '430100', '房地产开发', '已映射', 285090, -5600.40, -2.95, 0.0395, -39200.80, '正常'),
            ('600048', '保利发展', 'A股', '430100', '房地产开发', '已映射', 225030, -1900.50, -1.45, 0.0285, -13300.50, '正常'),
            ('001979', '招商蛇口', 'A股', '430100', '房地产开发', '已映射', 165400, -3850.60, -2.85, 0.0415, -26950.20, '正常'),
            ('600383', '金地集团', 'A股', '430100', '房地产开发', '已映射', 125600, -2650.40, -1.95, 0.0355, -18550.80, '正常'),
            ('000069', '华侨城A', 'A股', '430100', '房地产开发', '已映射', 95400, -1850.20, -1.65, 0.0325, -12950.40, '正常'),
            ('600340', '华夏幸福', 'A股', '430100', '房地产开发', '已映射', 65200, -4250.80, -3.25, 0.0485, -29750.60, '正常'),
            ('000671', '阳光城', 'A股', '430100', '房地产开发', '已映射', 45800, -2850.60, -2.65, 0.0455, -19950.20, '正常'),
            ('600606', '绿地控股', 'A股', '430100', '房地产开发', '已映射', 85600, -3650.40, -3.15, 0.0425, -25550.80, '正常'),
            ('600663', '陆家嘴', 'A股', '430100', '房地产开发', '已映射', 125600, -1950.20, -1.25, 0.0295, -13650.40, '正常'),
            ('000656', '金科股份', 'A股', '430100', '房地产开发', '已映射', 75400, -2250.60, -2.15, 0.0385, -15750.20, '正常'),
            
            # 医药股 (18只)
            ('000661', '长春高新', 'A股', '610000', '食品饮料', '已映射', 158040, 6800.20, 4.25, 0.0445, 47600.40, '正常'),
            ('600276', '恒瑞医药', 'A股', '610000', '食品饮料', '已映射', 425080, -3200.60, -2.15, 0.0375, -22400.20, '正常'),
            ('300760', '迈瑞医疗', 'A股', '610000', '食品饮料', '已映射', 515090, 8900.40, 3.85, 0.0355, 62300.80, '正常'),
            ('000538', '云南白药', 'A股', '610000', '食品饮料', '已映射', 285600, 9850.60, 3.25, 0.0395, 68950.20, '正常'),
            ('002821', '凯莱英', 'A股', '610000', '食品饮料', '已映射', 125600, 5650.40, 4.15, 0.0465, 39550.80, '正常'),
            ('300122', '智飞生物', 'A股', '610000', '食品饮料', '已映射', 195400, 8950.60, 3.85, 0.0425, 62650.20, '正常'),
            ('600521', '华海药业', 'A股', '610000', '食品饮料', '已映射', 85600, -2850.40, -2.65, 0.0455, -19950.80, '正常'),
            ('300347', '泰格医药', 'A股', '610000', '食品饮料', '已映射', 165400, 7850.20, 3.45, 0.0485, 54950.40, '正常'),
            ('002422', '科伦药业', 'A股', '610000', '食品饮料', '已映射', 95400, 3250.60, 2.85, 0.0415, 22750.20, '正常'),
            ('600867', '通化东宝', 'A股', '610000', '食品饮料', '已映射', 125600, 4850.40, 3.65, 0.0445, 33950.80, '正常'),
            ('002007', '华兰生物', 'A股', '610000', '食品饮料', '已映射', 165400, 6850.20, 3.25, 0.0395, 47950.40, '正常'),
            ('300529', '健帆生物', 'A股', '610000', '食品饮料', '已映射', 125600, 5650.40, 4.15, 0.0465, 39550.80, '正常'),
            ('600085', '同仁堂', 'A股', '610000', '食品饮料', '已映射', 285600, 9850.60, 3.45, 0.0415, 68950.20, '正常'),
            ('002038', '双鹭药业', 'A股', '610000', '食品饮料', '已映射', 85600, -2650.40, -2.35, 0.0445, -18550.80, '正常'),
            ('000739', '普洛药业', 'A股', '610000', '食品饮料', '已映射', 125600, 4850.20, 3.15, 0.0425, 33950.40, '正常'),
            ('002030', '达安基因', 'A股', '610000', '食品饮料', '已映射', 95400, 3650.60, 2.95, 0.0455, 25550.20, '正常'),
            ('300702', '天宇股份', 'A股', '610000', '食品饮料', '已映射', 65200, 2850.40, 3.85, 0.0485, 19950.80, '正常'),
            ('300601', '康徘药业', 'A股', '610000', '食品饮料', '已映射', 185600, 8950.20, 3.65, 0.0425, 62650.40, '正常'),
            
            # 白酒股
            ('600519', '贵州茅台', 'A股', '610300', '白酒', '已映射', 2580090, 32500.60, 4.85, 0.0385, 227500.20, '正常'),
            ('000858', '五粮液', 'A股', '610300', '白酒', '已映射', 8900.40, -5200.30, -1.95, 0.0295, -36400.90, '正常'),
            ('000596', '古井贡酒', 'A股', '610300', '白酒', '已映射', 1850.20, 3600.40, 2.65, 0.0445, 25200.80, '正常'),
            
            # 科技股
            ('000725', '京东方A', 'A股', '360100', '半导体', '已映射', 1950.30, -2800.50, -3.15, 0.0525, -19600.50, '正常'),
            ('002415', '海康威视', 'A股', '360100', '半导体', '已映射', 3250.80, 8900.20, 3.85, 0.0385, 62300.40, '正常'),
            ('300015', '爱尔眼科', 'A股', '640000', '金融服务', '已映射', 2100.50, -1200.30, -1.25, 0.0355, -8400.90, '正常'),
            
            # 新能源汽车
            ('002594', '比亚迪', 'A股', '420000', '交通运输', '已映射', 7850.60, 25800.90, 5.65, 0.0485, 180600.30, '正常'),
            ('600104', '上汽集团', 'A股', '420000', '交通运输', '已映射', 2950.40, -3600.20, -2.85, 0.0425, -25200.40, '正常'),
            ('000625', '长安汽车', 'A股', '420000', '交通运输', '已映射', 1650.80, 4500.60, 3.95, 0.0535, 31500.20, '正常'),
            
            # 房地产
            ('000002', '万科A', 'A股', '430100', '房地产开发', '已映射', 2850.90, -5600.40, -2.95, 0.0395, -39200.80, '正常'),
            ('600000', '浦发银行', 'A股', '480100', '银行', '已映射', 1950.60, -2800.30, -1.85, 0.0325, -19600.90, '正常'),
            ('600048', '保利发展', 'A股', '430100', '房地产开发', '已映射', 2250.30, -1900.50, -1.45, 0.0285, -13300.50, '正常'),
            
            # 医药股
            ('000661', '长春高新', 'A股', '610000', '食品饮料', '已映射', 1580.40, 6800.20, 4.25, 0.0445, 47600.40, '正常'),
            ('600276', '恒瑞医药', 'A股', '610000', '食品饮料', '已映射', 4250.80, -3200.60, -2.15, 0.0375, -22400.20, '正常'),
            ('300760', '迈瑞医疗', 'A股', '610000', '食品饮料', '已映射', 5150.90, 8900.40, 3.85, 0.0355, 62300.80, '正常'),
            
            # 未分类股票
            ('688001', '华兴源创', '科创板', None, '未分类', '未映射', 850.20, -500.30, -0.95, 0.0625, -3500.90, '待处理'),
            ('689009', '九号公司', '科创板', None, '未分类', '未映射', 650.80, 300.50, 1.25, 0.0545, 2100.50, '待处理'),
            ('300999', '金龙鱼', 'A股', None, '未分类', '未映射', 2950.60, -1800.40, -1.65, 0.0425, -12600.80, '待处理')
        ]
        
        # 插入数据
        insert_sql = """
        INSERT INTO l1_wind_stock_mapping 
        (stock_code, stock_name, market_type, industry_code, industry_name, mapping_status, 
         total_market_value, daily_net_inflow, net_inflow_ratio, recent_volatility, 
         latest_7d_inflow, operation_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_sql, stock_data)
        
        connection.commit()
        print(f"✓ 成功插入 {len(stock_data)} 条股票映射数据")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"✗ 初始化股票映射数据失败: {e}")
        return False

def show_statistics():
    """显示数据统计信息"""
    print("\n" + "="*50)
    print("数据库初始化完成，统计信息如下：")
    print("="*50)
    
    connection = get_db_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        # 行业分类统计
        cursor.execute("SELECT COUNT(*) FROM l1_wind_industry_classification")
        industry_count = cursor.fetchone()[0]
        print(f"万得行业分类数据: {industry_count} 条")
        
        cursor.execute("SELECT industry_level, COUNT(*) FROM l1_wind_industry_classification GROUP BY industry_level")
        level_stats = cursor.fetchall()
        for level, count in level_stats:
            print(f"  {level}级行业: {count} 个")
        
        # 股票映射统计
        cursor.execute("SELECT COUNT(*) FROM l1_wind_stock_mapping")
        stock_count = cursor.fetchone()[0]
        print(f"股票映射数据: {stock_count} 条")
        
        cursor.execute("SELECT mapping_status, COUNT(*) FROM l1_wind_stock_mapping GROUP BY mapping_status")
        status_stats = cursor.fetchall()
        for status, count in status_stats:
            print(f"  {status}: {count} 只股票")
        
        cursor.execute("SELECT market_type, COUNT(*) FROM l1_wind_stock_mapping GROUP BY market_type")
        market_stats = cursor.fetchall()
        for market, count in market_stats:
            print(f"  {market}: {count} 只股票")
            
        # 上市公司统计
        cursor.execute("SELECT COUNT(*) FROM l1_listed_company_info")
        company_count = cursor.fetchone()[0]
        print(f"上市公司数据: {company_count} 条")
        
        if company_count > 0:
            cursor.execute("SELECT market_type, COUNT(*) FROM l1_listed_company_info GROUP BY market_type")
            company_market_stats = cursor.fetchall()
            for market, count in company_market_stats:
                print(f"  {market}: {count} 家公司")
        
        # 港股通统计
        cursor.execute("SELECT COUNT(*) FROM l1_hk_connect_stock")
        hk_count = cursor.fetchone()[0]
        print(f"港股通数据: {hk_count} 条")
        
        if hk_count > 0:
            cursor.execute("SELECT connect_type, COUNT(*) FROM l1_hk_connect_stock GROUP BY connect_type")
            connect_stats = cursor.fetchall()
            for connect_type, count in connect_stats:
                print(f"  {connect_type}: {count} 只股票")
        
        # 资金流向统计
        cursor.execute("SELECT COUNT(*) FROM l1_stock_capital_flow")
        flow_count = cursor.fetchone()[0]
        print(f"资金流向数据: {flow_count} 条")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"获取统计信息失败: {e}")

def main():
    """主函数"""
    print("="*60)
    print("万得行业分类模块 - 数据库初始化脚本")
    print("="*60)
    
    # 测试数据库连接
    print("测试数据库连接...")
    connection = get_db_connection()
    if not connection:
        print("✗ 数据库连接失败，请检查配置")
        sys.exit(1)
    connection.close()
    print("✓ 数据库连接成功")
    
    # 创建表
    success = True
    success &= create_industry_classification_table()
    success &= create_stock_mapping_table()
    success &= create_listed_company_table()
    success &= create_hk_connect_table()
    success &= create_capital_flow_table()
    
    if not success:
        print("✗ 创建表失败，初始化中断")
        sys.exit(1)
    
    # 初始化数据
    success &= init_industry_data()
    success &= init_stock_mapping_data()
    
    if success:
        show_statistics()
        print("\n✓ 万得行业分类模块数据库初始化完成！")
        print("\n接下来可以:")
        print("1. 启动Java服务: mvn spring-boot:run")
        print("2. 访问系统: http://localhost:5001")
        print("3. 访问管理台: http://localhost:8080")
    else:
        print("✗ 数据初始化失败")
        sys.exit(1)

if __name__ == "__main__":
    main()