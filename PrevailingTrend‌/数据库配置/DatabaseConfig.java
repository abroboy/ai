package com.prevailingtrend.config;

import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

/**
 * 数据库配置类
 * 统一管理所有模块的数据库配置
 * 
 * @author 大势所趋风险框架团队
 * @version 1.0
 */
public class DatabaseConfig {
    
    private static DatabaseConfig instance;
    private Properties properties;
    
    // 基础配置常量
    public static final String DEFAULT_HOST = "localhost";
    public static final int DEFAULT_PORT = 3306;
    public static final String DEFAULT_USERNAME = "root";
    public static final String DEFAULT_PASSWORD = "rr1234RR";
    public static final String DEFAULT_DATABASE = "pt";
    public static final String DEFAULT_CHARSET = "utf8mb4";
    
    // 连接池配置常量
    public static final int DEFAULT_MAX_CONNECTIONS = 20;
    public static final int DEFAULT_MIN_CONNECTIONS = 5;
    public static final int DEFAULT_CONNECTION_TIMEOUT = 30;
    
    private DatabaseConfig() {
        loadProperties();
    }
    
    /**
     * 获取单例实例
     */
    public static DatabaseConfig getInstance() {
        if (instance == null) {
            synchronized (DatabaseConfig.class) {
                if (instance == null) {
                    instance = new DatabaseConfig();
                }
            }
        }
        return instance;
    }
    
    /**
     * 加载配置文件
     */
    private void loadProperties() {
        properties = new Properties();
        
        // 尝试加载配置文件
        try (InputStream is = getClass().getClassLoader().getResourceAsStream("database.properties")) {
            if (is != null) {
                properties.load(is);
            }
        } catch (IOException e) {
            System.err.println("警告：无法加载database.properties文件，使用默认配置");
        }
    }
    
    /**
     * 获取数据库主机地址
     */
    public String getHost() {
        return properties.getProperty("db.host", DEFAULT_HOST);
    }
    
    /**
     * 获取数据库端口
     */
    public int getPort() {
        return Integer.parseInt(properties.getProperty("db.port", String.valueOf(DEFAULT_PORT)));
    }
    
    /**
     * 获取数据库用户名
     */
    public String getUsername() {
        return properties.getProperty("db.username", DEFAULT_USERNAME);
    }
    
    /**
     * 获取数据库密码
     */
    public String getPassword() {
        return properties.getProperty("db.password", DEFAULT_PASSWORD);
    }
    
    /**
     * 获取数据库名称
     */
    public String getDatabase() {
        return properties.getProperty("db.database", DEFAULT_DATABASE);
    }
    
    /**
     * 获取字符集
     */
    public String getCharset() {
        return properties.getProperty("db.charset", DEFAULT_CHARSET);
    }
    
    /**
     * 获取最大连接数
     */
    public int getMaxConnections() {
        return Integer.parseInt(properties.getProperty("db.max.connections", String.valueOf(DEFAULT_MAX_CONNECTIONS)));
    }
    
    /**
     * 获取最小连接数
     */
    public int getMinConnections() {
        return Integer.parseInt(properties.getProperty("db.min.connections", String.valueOf(DEFAULT_MIN_CONNECTIONS)));
    }
    
    /**
     * 获取连接超时时间
     */
    public int getConnectionTimeout() {
        return Integer.parseInt(properties.getProperty("db.connection.timeout", String.valueOf(DEFAULT_CONNECTION_TIMEOUT)));
    }
    
    /**
     * 获取JDBC连接URL
     */
    public String getJdbcUrl() {
        return String.format("jdbc:mysql://%s:%d/%s?characterEncoding=%s&useSSL=false&allowMultiQueries=true&serverTimezone=Asia/Shanghai",
                getHost(), getPort(), getDatabase(), getCharset());
    }
    
    /**
     * 获取连接配置映射
     */
    public Map<String, Object> getConnectionConfig() {
        Map<String, Object> config = new HashMap<>();
        config.put("host", getHost());
        config.put("port", getPort());
        config.put("username", getUsername());
        config.put("password", getPassword());
        config.put("database", getDatabase());
        config.put("charset", getCharset());
        config.put("jdbcUrl", getJdbcUrl());
        config.put("maxConnections", getMaxConnections());
        config.put("minConnections", getMinConnections());
        config.put("connectionTimeout", getConnectionTimeout());
        return config;
    }
}

/**
 * 表名配置类
 * 按层级和模块组织表名
 */
class TableNames {
    
    // 第一层模块 - 数据采集层
    public static class Layer1 {
        // 万得行业分类
        public static final String WIND_INDUSTRY_CLASSIFICATION = "l1_wind_industry_classification";
        public static final String WIND_STOCK_INDUSTRY_MAPPING = "l1_wind_stock_industry_mapping";
        
        // 公司名字列表
        public static final String COMPANY_LIST_INFO = "l1_company_list_info";
        public static final String COMPANY_MARKET_CLASSIFICATION = "l1_company_market_classification";
        
        // 国内热点数据
        public static final String DOMESTIC_HOTSPOT_DATA = "l1_domestic_hotspot_data";
        public static final String DOMESTIC_HOTSPOT_ANALYSIS = "l1_domestic_hotspot_analysis";
        
        // 国外热点数据
        public static final String FOREIGN_HOTSPOT_DATA = "l1_foreign_hotspot_data";
        public static final String FOREIGN_HOTSPOT_ANALYSIS = "l1_foreign_hotspot_analysis";
        
        // 腾讯济安指数
        public static final String TENCENT_INDEX_DATA = "l1_tencent_index_data";
        public static final String TENCENT_INDEX_HISTORY = "l1_tencent_index_history";
        
        // 雪球等论坛热点数据
        public static final String FORUM_HOTSPOT_DATA = "l1_forum_hotspot_data";
        public static final String FORUM_TOPIC_ANALYSIS = "l1_forum_topic_analysis";
        
        // 其他互联网信息
        public static final String INTERNET_INFO_DATA = "l1_internet_info_data";
        public static final String INTERNET_INFO_ANALYSIS = "l1_internet_info_analysis";
    }
    
    // 第二层模块 - 数据处理层
    public static class Layer2 {
        public static final String COMPANY_ATTRIBUTES = "l2_company_attributes";
        public static final String COMPANY_ATTRIBUTE_ANALYSIS = "l2_company_attribute_analysis";
        public static final String HOTSPOT_DATA_SUMMARY = "l2_hotspot_data_summary";
        public static final String HOTSPOT_TRENDS = "l2_hotspot_trends";
    }
    
    // 第三层模块 - 数据整合层
    public static class Layer3 {
        public static final String QCC_COMPANY_DATA = "l3_qcc_company_data";
        public static final String QCC_ANALYSIS = "l3_qcc_analysis";
        public static final String TAX_BANK_REPORT_DATA = "l3_tax_bank_report_data";
        public static final String TAX_ANALYSIS = "l3_tax_analysis";
        public static final String FINANCIAL_BALANCE_SHEET = "l3_financial_balance_sheet";
        public static final String FINANCIAL_INCOME_STATEMENT = "l3_financial_income_statement";
        public static final String FINANCIAL_CASH_FLOW = "l3_financial_cash_flow";
        public static final String FORUM_DATA_SUMMARY = "l3_forum_data_summary";
        public static final String FORUM_SENTIMENT_ANALYSIS = "l3_forum_sentiment_analysis";
    }
    
    // 第四层模块 - 数据评分层
    public static class Layer4 {
        public static final String COMPANY_SCORE = "l4_company_score";
        public static final String COMPANY_SCORE_HISTORY = "l4_company_score_history";
        public static final String INDUSTRY_SCORE = "l4_industry_score";
        public static final String INDUSTRY_SCORE_HISTORY = "l4_industry_score_history";
        public static final String INDUSTRY_COMPANY_SCORE = "l4_industry_company_score";
        public static final String INDUSTRY_COMPANY_SCORE_HISTORY = "l4_industry_company_score_history";
    }
    
    // 第五层模块 - 权重配置层
    public static class Layer5 {
        public static final String FACTOR_WEIGHTS = "l5_factor_weights";
        public static final String FACTOR_WEIGHT_HISTORY = "l5_factor_weight_history";
    }
    
    // 第六层模块 - 预测分析层
    public static class Layer6 {
        public static final String CURVE_PREDICTION_DATA = "l6_curve_prediction_data";
        public static final String CURVE_PREDICTION_ANALYSIS = "l6_curve_prediction_analysis";
    }
    
    // 系统表
    public static class System {
        public static final String SYSTEM_LOGS = "system_logs";
        public static final String DATA_FLOW_LOGS = "system_data_flow_logs";
        public static final String MODULE_STATUS = "system_module_status";
        public static final String DATA_QUALITY = "system_data_quality";
    }
    
    /**
     * 获取表名
     * @param layer 层级
     * @param module 模块
     * @param table 表名
     * @return 完整表名
     */
    public static String getTableName(String layer, String module, String table) {
        return String.format("%s_%s_%s", layer.toLowerCase(), module.toLowerCase(), table.toLowerCase());
    }
    
    /**
     * 获取所有表名的映射
     */
    public static Map<String, Map<String, String>> getAllTables() {
        Map<String, Map<String, String>> allTables = new HashMap<>();
        
        // 这里可以通过反射获取所有静态字段，但为简化起见，手动添加主要表
        Map<String, String> layer1Tables = new HashMap<>();
        layer1Tables.put("wind_industry_classification", Layer1.WIND_INDUSTRY_CLASSIFICATION);
        layer1Tables.put("company_list_info", Layer1.COMPANY_LIST_INFO);
        layer1Tables.put("domestic_hotspot_data", Layer1.DOMESTIC_HOTSPOT_DATA);
        
        Map<String, String> systemTables = new HashMap<>();
        systemTables.put("system_logs", System.SYSTEM_LOGS);
        systemTables.put("module_status", System.MODULE_STATUS);
        
        allTables.put("LAYER1", layer1Tables);
        allTables.put("SYSTEM", systemTables);
        
        return allTables;
    }
}