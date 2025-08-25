"""
数据库初始化脚本
创建数据库和所有表结构
"""

import sys
import os
import pymysql
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_config import db_config, table_names

def create_database():
    """创建数据库"""
    try:
        # 连接MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=db_config.HOST,
            port=db_config.PORT,
            user=db_config.USERNAME,
            password=db_config.PASSWORD,
            charset=db_config.CHARSET
        )
        
        cursor = connection.cursor()
        
        # 创建数据库
        sql = f"CREATE DATABASE IF NOT EXISTS {db_config.DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        cursor.execute(sql)
        
        print(f"✅ 数据库 {db_config.DATABASE} 创建成功")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        raise

def create_layer1_tables():
    """创建第一层模块表"""
    print("\n创建第一层模块表...")
    
    try:
        connection = pymysql.connect(**db_config.get_connection_config())
        cursor = connection.cursor()
        
        # 万得行业分类表
        wind_industry_sql = """
        CREATE TABLE IF NOT EXISTS l1_wind_industry_classification (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            industry_code VARCHAR(20) NOT NULL COMMENT '行业代码',
            industry_name VARCHAR(100) NOT NULL COMMENT '行业名称',
            industry_level INT NOT NULL COMMENT '行业层级',
            parent_code VARCHAR(20) COMMENT '父级行业代码',
            sw_code VARCHAR(20) COMMENT '申万行业代码',
            csrc_code VARCHAR(20) COMMENT '证监会行业代码',
            status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态',
            industry_desc TEXT COMMENT '行业描述',
            major_companies JSON COMMENT '主要公司列表',
            industry_keywords JSON COMMENT '行业关键词',
            market_cap_total DECIMAL(20,2) COMMENT '行业总市值',
            company_count INT COMMENT '行业公司数量',
            update_date DATETIME COMMENT '数据更新日期',
            source VARCHAR(50) DEFAULT 'wind' COMMENT '数据来源',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            
            UNIQUE KEY uk_industry_code (industry_code),
            KEY idx_industry_level (industry_level),
            KEY idx_parent_code (parent_code),
            KEY idx_status (status),
            KEY idx_source (source),
            KEY idx_update_date (update_date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='万得行业分类表';
        """
        
        stock_industry_sql = """
        CREATE TABLE IF NOT EXISTS l1_wind_stock_industry_mapping (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            stock_code VARCHAR(20) NOT NULL COMMENT '股票代码',
            stock_name VARCHAR(100) NOT NULL COMMENT '股票名称',
            industry_code VARCHAR(20) NOT NULL COMMENT '行业代码',
            industry_name VARCHAR(100) NOT NULL COMMENT '行业名称',
            industry_level INT NOT NULL COMMENT '行业层级',
            mapping_date DATETIME NOT NULL COMMENT '映射日期',
            status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态',
            confidence DECIMAL(3,2) COMMENT '置信度',
            source VARCHAR(50) DEFAULT 'wind' COMMENT '数据来源',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            
            UNIQUE KEY uk_stock_industry (stock_code, industry_code),
            KEY idx_stock_code (stock_code),
            KEY idx_industry_code (industry_code),
            KEY idx_industry_level (industry_level),
            KEY idx_status (status),
            KEY idx_confidence (confidence),
            KEY idx_source (source),
            KEY idx_mapping_date (mapping_date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票行业映射表';
        """
        
        # 公司名字列表表
        company_list_sql = """
        CREATE TABLE IF NOT EXISTS l1_company_list_info (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            company_name VARCHAR(200) NOT NULL COMMENT '公司名称',
            stock_code VARCHAR(20) COMMENT '股票代码',
            market VARCHAR(10) COMMENT '市场类型',
            short_name VARCHAR(100) COMMENT '简称',
            industry_code VARCHAR(20) COMMENT '行业代码',
            list_date DATE COMMENT '上市日期',
            status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态',
            company_type VARCHAR(50) COMMENT '公司类型',
            area VARCHAR(100) COMMENT '地区',
            website VARCHAR(200) COMMENT '网站',
            business_scope TEXT COMMENT '经营范围',
            market_cap DECIMAL(20,2) COMMENT '市值',
            employees INT COMMENT '员工数',
            update_date DATETIME COMMENT '数据更新日期',
            source VARCHAR(50) DEFAULT 'manual' COMMENT '数据来源',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            
            UNIQUE KEY uk_company_stock (company_name, stock_code),
            KEY idx_stock_code (stock_code),
            KEY idx_market (market),
            KEY idx_industry_code (industry_code),
            KEY idx_status (status),
            KEY idx_company_type (company_type),
            KEY idx_area (area),
            KEY idx_source (source),
            KEY idx_update_date (update_date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公司名字列表表';
        """
        
        # 国内热点数据表
        domestic_hotspot_sql = """
        CREATE TABLE IF NOT EXISTS l1_domestic_hotspot_data (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            hotspot_id VARCHAR(100) NOT NULL COMMENT '热点ID',
            title VARCHAR(500) NOT NULL COMMENT '热点标题',
            content TEXT NOT NULL COMMENT '热点内容',
            hotspot_type VARCHAR(20) NOT NULL COMMENT '热点类型',
            hotspot_level VARCHAR(20) NOT NULL DEFAULT 'medium' COMMENT '热点级别',
            status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '热点状态',
            source VARCHAR(100) COMMENT '数据来源',
            url VARCHAR(1000) COMMENT '原始链接',
            publish_time DATETIME COMMENT '发布时间',
            keywords JSON COMMENT '关键词列表',
            related_companies JSON COMMENT '相关公司列表',
            related_industries JSON COMMENT '相关行业列表',
            sentiment_score DECIMAL(3,2) COMMENT '情感得分',
            heat_score DECIMAL(5,2) COMMENT '热度得分',
            update_date DATETIME COMMENT '数据更新日期',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            
            UNIQUE KEY uk_hotspot_id (hotspot_id),
            KEY idx_title (title(100)),
            KEY idx_hotspot_type (hotspot_type),
            KEY idx_hotspot_level (hotspot_level),
            KEY idx_status (status),
            KEY idx_source (source),
            KEY idx_publish_time (publish_time),
            KEY idx_sentiment_score (sentiment_score),
            KEY idx_heat_score (heat_score),
            KEY idx_update_date (update_date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='国内热点数据表';
        """
        
        # 执行SQL
        tables = [
            ('万得行业分类表', wind_industry_sql),
            ('股票行业映射表', stock_industry_sql),
            ('公司名字列表表', company_list_sql),
            ('国内热点数据表', domestic_hotspot_sql)
        ]
        
        for table_name, sql in tables:
            cursor.execute(sql)
            print(f"✅ {table_name} 创建成功")
        
        connection.commit()
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 创建第一层模块表失败: {e}")
        raise

def create_system_tables():
    """创建系统表"""
    print("\n创建系统表...")
    
    try:
        connection = pymysql.connect(**db_config.get_connection_config())
        cursor = connection.cursor()
        
        # 系统日志表
        system_logs_sql = """
        CREATE TABLE IF NOT EXISTS system_logs (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME NOT NULL COMMENT '时间戳',
            level VARCHAR(10) NOT NULL COMMENT '日志级别',
            module VARCHAR(50) NOT NULL COMMENT '模块名称',
            message TEXT NOT NULL COMMENT '日志消息',
            details JSON COMMENT '详细信息',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            
            KEY idx_timestamp (timestamp),
            KEY idx_level (level),
            KEY idx_module (module),
            KEY idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统日志表';
        """
        
        # 数据流向日志表
        data_flow_sql = """
        CREATE TABLE IF NOT EXISTS system_data_flow_logs (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            flow_id VARCHAR(100) NOT NULL COMMENT '流向ID',
            source_layer VARCHAR(20) NOT NULL COMMENT '源层级',
            source_module VARCHAR(50) NOT NULL COMMENT '源模块',
            target_layer VARCHAR(20) NOT NULL COMMENT '目标层级',
            target_module VARCHAR(50) NOT NULL COMMENT '目标模块',
            data_type VARCHAR(50) NOT NULL COMMENT '数据类型',
            record_count INT NOT NULL COMMENT '记录数',
            status VARCHAR(20) NOT NULL COMMENT '状态',
            start_time DATETIME NOT NULL COMMENT '开始时间',
            end_time DATETIME COMMENT '结束时间',
            duration_seconds INT COMMENT '耗时(秒)',
            error_message TEXT COMMENT '错误信息',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            
            UNIQUE KEY uk_flow_id (flow_id),
            KEY idx_source_layer (source_layer),
            KEY idx_source_module (source_module),
            KEY idx_target_layer (target_layer),
            KEY idx_target_module (target_module),
            KEY idx_data_type (data_type),
            KEY idx_status (status),
            KEY idx_start_time (start_time),
            KEY idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据流向日志表';
        """
        
        # 模块状态表
        module_status_sql = """
        CREATE TABLE IF NOT EXISTS system_module_status (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            module_name VARCHAR(100) NOT NULL COMMENT '模块名称',
            layer VARCHAR(20) NOT NULL COMMENT '所属层级',
            status VARCHAR(20) NOT NULL COMMENT '状态',
            last_run_time DATETIME COMMENT '最后运行时间',
            next_run_time DATETIME COMMENT '下次运行时间',
            run_count INT DEFAULT 0 COMMENT '运行次数',
            error_count INT DEFAULT 0 COMMENT '错误次数',
            last_error_message TEXT COMMENT '最后错误信息',
            config JSON COMMENT '配置信息',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            
            UNIQUE KEY uk_module_name (module_name),
            KEY idx_layer (layer),
            KEY idx_status (status),
            KEY idx_last_run_time (last_run_time),
            KEY idx_next_run_time (next_run_time),
            KEY idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='模块状态表';
        """
        
        # 数据质量表
        data_quality_sql = """
        CREATE TABLE IF NOT EXISTS system_data_quality (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            table_name VARCHAR(100) NOT NULL COMMENT '表名',
            layer VARCHAR(20) NOT NULL COMMENT '所属层级',
            module VARCHAR(50) NOT NULL COMMENT '所属模块',
            total_records INT NOT NULL COMMENT '总记录数',
            valid_records INT NOT NULL COMMENT '有效记录数',
            invalid_records INT NOT NULL COMMENT '无效记录数',
            completeness_rate DECIMAL(5,2) NOT NULL COMMENT '完整率',
            accuracy_rate DECIMAL(5,2) NOT NULL COMMENT '准确率',
            timeliness_score DECIMAL(5,2) NOT NULL COMMENT '及时性得分',
            consistency_score DECIMAL(5,2) NOT NULL COMMENT '一致性得分',
            quality_score DECIMAL(5,2) NOT NULL COMMENT '质量总分',
            check_date DATE NOT NULL COMMENT '检查日期',
            details JSON COMMENT '详细信息',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            
            UNIQUE KEY uk_table_date (table_name, check_date),
            KEY idx_layer (layer),
            KEY idx_module (module),
            KEY idx_quality_score (quality_score),
            KEY idx_check_date (check_date),
            KEY idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据质量表';
        """
        
        # 执行SQL
        tables = [
            ('系统日志表', system_logs_sql),
            ('数据流向日志表', data_flow_sql),
            ('模块状态表', module_status_sql),
            ('数据质量表', data_quality_sql)
        ]
        
        for table_name, sql in tables:
            cursor.execute(sql)
            print(f"✅ {table_name} 创建成功")
        
        connection.commit()
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 创建系统表失败: {e}")
        raise

def insert_sample_data():
    """插入示例数据"""
    print("\n插入示例数据...")
    
    try:
        connection = pymysql.connect(**db_config.get_connection_config())
        cursor = connection.cursor()
        
        # 插入示例行业数据
        industry_data = [
            ('801010', '农林牧渔', 1, None, '801010', 'A01', 'active', '农业、林业、畜牧业、渔业', '["牧原股份", "温氏股份"]', '["农业", "养殖", "种植"]', 1000000000.0, 50, datetime.now(), 'wind'),
            ('801020', '采掘', 1, None, '801020', 'B01', 'active', '煤炭、石油、天然气开采', '["中国石油", "中国石化"]', '["能源", "采掘", "石油"]', 2000000000.0, 30, datetime.now(), 'wind'),
            ('801030', '化工', 1, None, '801030', 'C01', 'active', '化学原料及化学制品制造业', '["万华化学", "恒力石化"]', '["化工", "化学", "材料"]', 1500000000.0, 80, datetime.now(), 'wind')
        ]
        
        industry_sql = """
        INSERT IGNORE INTO l1_wind_industry_classification 
        (industry_code, industry_name, industry_level, parent_code, sw_code, csrc_code, status, industry_desc, major_companies, industry_keywords, market_cap_total, company_count, update_date, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(industry_sql, industry_data)
        print(f"✅ 插入 {len(industry_data)} 条行业数据")
        
        # 插入示例公司数据
        company_data = [
            ('中国石油天然气股份有限公司', '601857', 'SH', '中国石油', '801020', '2007-11-05', 'active', 'main_board', '北京', 'http://www.petrochina.com.cn', '石油天然气勘探开发', 100000000000.0, 50000, datetime.now(), 'manual'),
            ('平安银行股份有限公司', '000001', 'SZ', '平安银行', '801080', '1991-04-03', 'active', 'main_board', '深圳', 'http://www.bank.pingan.com', '银行业务', 50000000000.0, 30000, datetime.now(), 'manual'),
            ('万科企业股份有限公司', '000002', 'SZ', '万科A', '801030', '1991-01-29', 'active', 'main_board', '深圳', 'http://www.vanke.com', '房地产开发', 30000000000.0, 20000, datetime.now(), 'manual')
        ]
        
        company_sql = """
        INSERT IGNORE INTO l1_company_list_info 
        (company_name, stock_code, market, short_name, industry_code, list_date, status, company_type, area, website, business_scope, market_cap, employees, update_date, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(company_sql, company_data)
        print(f"✅ 插入 {len(company_data)} 条公司数据")
        
        # 插入示例模块状态数据
        module_status_data = [
            ('万得行业分类', 'LAYER1', 'running', datetime.now(), datetime.now(), 10, 0, None, '{"interval": 3600}', datetime.now()),
            ('公司名字列表', 'LAYER1', 'running', datetime.now(), datetime.now(), 8, 1, '数据源连接失败', '{"interval": 7200}', datetime.now()),
            ('国内热点数据', 'LAYER1', 'stopped', None, datetime.now(), 0, 0, None, '{"interval": 1800}', datetime.now())
        ]
        
        module_status_sql = """
        INSERT IGNORE INTO system_module_status 
        (module_name, layer, status, last_run_time, next_run_time, run_count, error_count, last_error_message, config, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(module_status_sql, module_status_data)
        print(f"✅ 插入 {len(module_status_data)} 条模块状态数据")
        
        connection.commit()
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 插入示例数据失败: {e}")
        raise

def main():
    """主函数"""
    print("=" * 60)
    print("数据库初始化脚本")
    print("=" * 60)
    print(f"数据库配置:")
    print(f"  主机: {db_config.HOST}")
    print(f"  端口: {db_config.PORT}")
    print(f"  用户名: {db_config.USERNAME}")
    print(f"  数据库: {db_config.DATABASE}")
    print("=" * 60)
    
    try:
        # 1. 创建数据库
        create_database()
        
        # 2. 创建第一层模块表
        create_layer1_tables()
        
        # 3. 创建系统表
        create_system_tables()
        
        # 4. 插入示例数据
        insert_sample_data()
        
        print("\n" + "=" * 60)
        print("✅ 数据库初始化完成！")
        print("=" * 60)
        print("已创建的表:")
        print("  第一层模块:")
        print("    - l1_wind_industry_classification (万得行业分类)")
        print("    - l1_wind_stock_industry_mapping (股票行业映射)")
        print("    - l1_company_list_info (公司名字列表)")
        print("    - l1_domestic_hotspot_data (国内热点数据)")
        print("  系统表:")
        print("    - system_logs (系统日志)")
        print("    - system_data_flow_logs (数据流向日志)")
        print("    - system_module_status (模块状态)")
        print("    - system_data_quality (数据质量)")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 数据库初始化失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 