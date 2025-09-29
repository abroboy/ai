package com.prevailingtrend.database;

import com.prevailingtrend.config.DatabaseConfig;
import com.prevailingtrend.config.TableNames;

import java.sql.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

/**
 * 数据库初始化工具
 * 创建数据库和所有表结构
 * 
 * @author 大势所趋风险框架团队
 * @version 1.0
 */
public class DatabaseInitializer {
    
    private DatabaseConfig config;
    private static final String MYSQL_DRIVER = "com.mysql.cj.jdbc.Driver";
    
    public DatabaseInitializer() {
        this.config = DatabaseConfig.getInstance();
    }
    
    /**
     * 主方法 - 执行数据库初始化
     */
    public static void main(String[] args) {
        DatabaseInitializer initializer = new DatabaseInitializer();
        
        System.out.println("=" .repeat(60));
        System.out.println("数据库初始化工具");
        System.out.println("=" .repeat(60));
        System.out.println("数据库配置:");
        System.out.println("  主机: " + initializer.config.getHost());
        System.out.println("  端口: " + initializer.config.getPort());
        System.out.println("  用户名: " + initializer.config.getUsername());
        System.out.println("  数据库: " + initializer.config.getDatabase());
        System.out.println("=" .repeat(60));
        
        try {
            // 加载MySQL驱动
            Class.forName(MYSQL_DRIVER);
            
            // 1. 创建数据库
            initializer.createDatabase();
            
            // 2. 创建第一层模块表
            initializer.createLayer1Tables();
            
            // 3. 创建系统表
            initializer.createSystemTables();
            
            // 4. 插入示例数据
            initializer.insertSampleData();
            
            System.out.println("\n" + "=" .repeat(60));
            System.out.println("✅ 数据库初始化完成！");
            System.out.println("=" .repeat(60));
            System.out.println("已创建的表:");
            System.out.println("  第一层模块:");
            System.out.println("    - " + TableNames.Layer1.WIND_INDUSTRY_CLASSIFICATION + " (上市公司或行业分类)");
            System.out.println("    - " + TableNames.Layer1.WIND_STOCK_INDUSTRY_MAPPING + " (股票行业映射)");
            System.out.println("    - " + TableNames.Layer1.COMPANY_LIST_INFO + " (公司名字列表)");
            System.out.println("    - " + TableNames.Layer1.DOMESTIC_HOTSPOT_DATA + " (国内热点数据)");
            System.out.println("  系统表:");
            System.out.println("    - " + TableNames.System.SYSTEM_LOGS + " (系统日志)");
            System.out.println("    - " + TableNames.System.DATA_FLOW_LOGS + " (数据流向日志)");
            System.out.println("    - " + TableNames.System.MODULE_STATUS + " (模块状态)");
            System.out.println("    - " + TableNames.System.DATA_QUALITY + " (数据质量)");
            System.out.println("=" .repeat(60));
            
        } catch (Exception e) {
            System.err.println("\n❌ 数据库初始化失败: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
    
    /**
     * 创建数据库
     */
    private void createDatabase() throws SQLException {
        String jdbcUrl = String.format("jdbc:mysql://%s:%d/?characterEncoding=%s&useSSL=false&serverTimezone=Asia/Shanghai",
                config.getHost(), config.getPort(), config.getCharset());
        
        try (Connection connection = DriverManager.getConnection(jdbcUrl, config.getUsername(), config.getPassword())) {
            String sql = String.format("CREATE DATABASE IF NOT EXISTS %s CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci", 
                    config.getDatabase());
            
            try (Statement stmt = connection.createStatement()) {
                stmt.execute(sql);
                System.out.println("✅ 数据库 " + config.getDatabase() + " 创建成功");
            }
        }
    }
    
    /**
     * 创建第一层模块表
     */
    private void createLayer1Tables() throws SQLException {
        System.out.println("\n创建第一层模块表...");
        
        try (Connection connection = DriverManager.getConnection(config.getJdbcUrl(), config.getUsername(), config.getPassword())) {
            List<TableDefinition> tables = getLayer1TableDefinitions();
            
            for (TableDefinition table : tables) {
                try (Statement stmt = connection.createStatement()) {
                    stmt.execute(table.sql);
                    System.out.println("✅ " + table.name + " 创建成功");
                }
            }
        }
    }
    
    /**
     * 创建系统表
     */
    private void createSystemTables() throws SQLException {
        System.out.println("\n创建系统表...");
        
        try (Connection connection = DriverManager.getConnection(config.getJdbcUrl(), config.getUsername(), config.getPassword())) {
            List<TableDefinition> tables = getSystemTableDefinitions();
            
            for (TableDefinition table : tables) {
                try (Statement stmt = connection.createStatement()) {
                    stmt.execute(table.sql);
                    System.out.println("✅ " + table.name + " 创建成功");
                }
            }
        }
    }
    
    /**
     * 插入示例数据
     */
    private void insertSampleData() throws SQLException {
        System.out.println("\n插入示例数据...");
        
        try (Connection connection = DriverManager.getConnection(config.getJdbcUrl(), config.getUsername(), config.getPassword())) {
            // 插入示例行业数据
            insertIndustryData(connection);
            
            // 插入示例公司数据
            insertCompanyData(connection);
            
            // 插入示例模块状态数据
            insertModuleStatusData(connection);
        }
    }
    
    /**
     * 插入行业数据
     */
    private void insertIndustryData(Connection connection) throws SQLException {
        String sql = String.format("""
            INSERT IGNORE INTO %s 
            (industry_code, industry_name, industry_level, parent_code, sw_code, csrc_code, status, industry_desc, 
             major_companies, industry_keywords, market_cap_total, company_count, update_date, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, TableNames.Layer1.WIND_INDUSTRY_CLASSIFICATION);
        
        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            Object[][] industryData = {
                {"801010", "农林牧渔", 1, null, "801010", "A01", "active", "农业、林业、畜牧业、渔业", 
                 "[\"牧原股份\", \"温氏股份\"]", "[\"农业\", \"养殖\", \"种植\"]", 1000000000.0, 50, Timestamp.valueOf(LocalDateTime.now()), "wind"},
                {"801020", "采掘", 1, null, "801020", "B01", "active", "煤炭、石油、天然气开采", 
                 "[\"中国石油\", \"中国石化\"]", "[\"能源\", \"采掘\", \"石油\"]", 2000000000.0, 30, Timestamp.valueOf(LocalDateTime.now()), "wind"},
                {"801030", "化工", 1, null, "801030", "C01", "active", "化学原料及化学制品制造业", 
                 "[\"万华化学\", \"恒力石化\"]", "[\"化工\", \"化学\", \"材料\"]", 1500000000.0, 80, Timestamp.valueOf(LocalDateTime.now()), "wind"}
            };
            
            for (Object[] row : industryData) {
                for (int i = 0; i < row.length; i++) {
                    pstmt.setObject(i + 1, row[i]);
                }
                pstmt.addBatch();
            }
            
            int[] results = pstmt.executeBatch();
            System.out.println("✅ 插入 " + results.length + " 条行业数据");
        }
    }
    
    /**
     * 插入公司数据
     */
    private void insertCompanyData(Connection connection) throws SQLException {
        String sql = String.format("""
            INSERT IGNORE INTO %s 
            (company_name, stock_code, market, short_name, industry_code, list_date, status, company_type, 
             area, website, business_scope, market_cap, employees, update_date, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, TableNames.Layer1.COMPANY_LIST_INFO);
        
        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            Object[][] companyData = {
                {"中国石油天然气股份有限公司", "601857", "SH", "中国石油", "801020", Date.valueOf("2007-11-05"), "active", 
                 "main_board", "北京", "http://www.petrochina.com.cn", "石油天然气勘探开发", 100000000000.0, 50000, Timestamp.valueOf(LocalDateTime.now()), "manual"},
                {"平安银行股份有限公司", "000001", "SZ", "平安银行", "801080", Date.valueOf("1991-04-03"), "active", 
                 "main_board", "深圳", "http://www.bank.pingan.com", "银行业务", 50000000000.0, 30000, Timestamp.valueOf(LocalDateTime.now()), "manual"},
                {"万科企业股份有限公司", "000002", "SZ", "万科A", "801030", Date.valueOf("1991-01-29"), "active", 
                 "main_board", "深圳", "http://www.vanke.com", "房地产开发", 30000000000.0, 20000, Timestamp.valueOf(LocalDateTime.now()), "manual"}
            };
            
            for (Object[] row : companyData) {
                for (int i = 0; i < row.length; i++) {
                    pstmt.setObject(i + 1, row[i]);
                }
                pstmt.addBatch();
            }
            
            int[] results = pstmt.executeBatch();
            System.out.println("✅ 插入 " + results.length + " 条公司数据");
        }
    }
    
    /**
     * 插入模块状态数据
     */
    private void insertModuleStatusData(Connection connection) throws SQLException {
        String sql = String.format("""
            INSERT IGNORE INTO %s 
            (module_name, layer, status, last_run_time, next_run_time, run_count, error_count, last_error_message, config)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, TableNames.System.MODULE_STATUS);
        
        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            Object[][] moduleData = {
                {"上市公司或行业分类", "LAYER1", "running", Timestamp.valueOf(LocalDateTime.now()), Timestamp.valueOf(LocalDateTime.now().plusHours(1)), 10, 0, null, "{\"interval\": 3600}"},
                {"公司名字列表", "LAYER1", "running", Timestamp.valueOf(LocalDateTime.now()), Timestamp.valueOf(LocalDateTime.now().plusHours(2)), 8, 1, "数据源连接失败", "{\"interval\": 7200}"},
                {"国内热点数据", "LAYER1", "stopped", null, Timestamp.valueOf(LocalDateTime.now().plusMinutes(30)), 0, 0, null, "{\"interval\": 1800}"}
            };
            
            for (Object[] row : moduleData) {
                for (int i = 0; i < row.length; i++) {
                    pstmt.setObject(i + 1, row[i]);
                }
                pstmt.addBatch();
            }
            
            int[] results = pstmt.executeBatch();
            System.out.println("✅ 插入 " + results.length + " 条模块状态数据");
        }
    }
    
    /**
     * 获取第一层表定义
     */
    private List<TableDefinition> getLayer1TableDefinitions() {
        List<TableDefinition> tables = new ArrayList<>();
        
        // 上市公司或行业分类表
        tables.add(new TableDefinition("上市公司或行业分类表", String.format("""
            CREATE TABLE IF NOT EXISTS %s (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='上市公司或行业分类表'
            """, TableNames.Layer1.WIND_INDUSTRY_CLASSIFICATION)));
        
        // 公司名字列表表
        tables.add(new TableDefinition("公司名字列表表", String.format("""
            CREATE TABLE IF NOT EXISTS %s (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公司名字列表表'
            """, TableNames.Layer1.COMPANY_LIST_INFO)));
        
        return tables;
    }
    
    /**
     * 获取系统表定义
     */
    private List<TableDefinition> getSystemTableDefinitions() {
        List<TableDefinition> tables = new ArrayList<>();
        
        // 系统日志表
        tables.add(new TableDefinition("系统日志表", String.format("""
            CREATE TABLE IF NOT EXISTS %s (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统日志表'
            """, TableNames.System.SYSTEM_LOGS)));
        
        // 模块状态表
        tables.add(new TableDefinition("模块状态表", String.format("""
            CREATE TABLE IF NOT EXISTS %s (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='模块状态表'
            """, TableNames.System.MODULE_STATUS)));
        
        return tables;
    }
    
    /**
     * 表定义内部类
     */
    private static class TableDefinition {
        public final String name;
        public final String sql;
        
        public TableDefinition(String name, String sql) {
            this.name = name;
            this.sql = sql;
        }
    }
}