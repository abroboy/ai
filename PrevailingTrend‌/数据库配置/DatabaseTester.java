package com.prevailingtrend.database;

import com.prevailingtrend.config.DatabaseConfig;
import com.prevailingtrend.config.TableNames;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * 数据库连接测试工具
 * 测试数据库连接和基本操作
 * 
 * @author 大势所趋风险框架团队
 * @version 1.0
 */
public class DatabaseTester {
    
    private DatabaseConfig config;
    private static final String MYSQL_DRIVER = "com.mysql.cj.jdbc.Driver";
    
    public DatabaseTester() {
        this.config = DatabaseConfig.getInstance();
    }
    
    /**
     * 主方法 - 执行数据库测试
     */
    public static void main(String[] args) {
        DatabaseTester tester = new DatabaseTester();
        
        System.out.println("=" .repeat(60));
        System.out.println("数据库连接测试");
        System.out.println("=" .repeat(60));
        System.out.println("数据库配置:");
        System.out.println("  主机: " + tester.config.getHost());
        System.out.println("  端口: " + tester.config.getPort());
        System.out.println("  用户名: " + tester.config.getUsername());
        System.out.println("  数据库: " + tester.config.getDatabase());
        System.out.println("=" .repeat(60));
        
        List<Boolean> testResults = new ArrayList<>();
        
        try {
            // 加载MySQL驱动
            Class.forName(MYSQL_DRIVER);
            
            // 运行测试
            testResults.add(tester.testConnection());
            testResults.add(tester.testTables());
            testResults.add(tester.testData());
            testResults.add(tester.testTableNames());
            
        } catch (ClassNotFoundException e) {
            System.err.println("❌ MySQL驱动未找到: " + e.getMessage());
            testResults.add(false);
        }
        
        // 输出结果
        System.out.println("\n" + "=" .repeat(60));
        System.out.println("测试结果汇总:");
        long passed = testResults.stream().mapToInt(b -> b ? 1 : 0).sum();
        int total = testResults.size();
        System.out.println("通过: " + passed + "/" + total);
        
        if (passed == total) {
            System.out.println("🎉 所有测试通过！数据库配置正确！");
            System.out.println("\n数据库状态:");
            System.out.println("✅ 连接正常");
            System.out.println("✅ 表结构完整");
            System.out.println("✅ 数据可查询");
            System.out.println("✅ 配置正确");
        } else {
            System.out.println("⚠️  有 " + (total - passed) + " 项测试失败");
        }
        
        System.exit(passed == total ? 0 : 1);
    }
    
    /**
     * 测试数据库连接
     */
    private boolean testConnection() {
        System.out.println("测试数据库连接...");
        
        try (Connection connection = DriverManager.getConnection(config.getJdbcUrl(), config.getUsername(), config.getPassword());
             Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT VERSION()")) {
            
            if (rs.next()) {
                String version = rs.getString(1);
                System.out.println("✅ 数据库连接成功，MySQL版本: " + version);
                return true;
            }
            
        } catch (SQLException e) {
            System.err.println("❌ 数据库连接失败: " + e.getMessage());
        }
        
        return false;
    }
    
    /**
     * 测试表是否存在
     */
    private boolean testTables() {
        System.out.println("\n测试表结构...");
        
        try (Connection connection = DriverManager.getConnection(config.getJdbcUrl(), config.getUsername(), config.getPassword())) {
            
            // 检查第一层模块表
            String[] layer1Tables = {
                TableNames.Layer1.WIND_INDUSTRY_CLASSIFICATION,
                TableNames.Layer1.WIND_STOCK_INDUSTRY_MAPPING,
                TableNames.Layer1.COMPANY_LIST_INFO,
                TableNames.Layer1.DOMESTIC_HOTSPOT_DATA
            };
            
            boolean allTablesExist = true;
            
            for (String tableName : layer1Tables) {
                if (tableExists(connection, tableName)) {
                    System.out.println("✅ 表 " + tableName + " 存在");
                } else {
                    System.out.println("❌ 表 " + tableName + " 不存在");
                    allTablesExist = false;
                }
            }
            
            // 检查系统表
            String[] systemTables = {
                TableNames.System.SYSTEM_LOGS,
                TableNames.System.DATA_FLOW_LOGS,
                TableNames.System.MODULE_STATUS,
                TableNames.System.DATA_QUALITY
            };
            
            for (String tableName : systemTables) {
                if (tableExists(connection, tableName)) {
                    System.out.println("✅ 表 " + tableName + " 存在");
                } else {
                    System.out.println("❌ 表 " + tableName + " 不存在");
                    allTablesExist = false;
                }
            }
            
            return allTablesExist;
            
        } catch (SQLException e) {
            System.err.println("❌ 测试表结构失败: " + e.getMessage());
            return false;
        }
    }
    
    /**
     * 检查表是否存在
     */
    private boolean tableExists(Connection connection, String tableName) throws SQLException {
        String sql = "SHOW TABLES LIKE ?";
        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            pstmt.setString(1, tableName);
            try (ResultSet rs = pstmt.executeQuery()) {
                return rs.next();
            }
        }
    }
    
    /**
     * 测试数据查询
     */
    private boolean testData() {
        System.out.println("\n测试数据查询...");
        
        try (Connection connection = DriverManager.getConnection(config.getJdbcUrl(), config.getUsername(), config.getPassword())) {
            
            // 查询行业数据
            String sql = "SELECT COUNT(*) as count FROM " + TableNames.Layer1.WIND_INDUSTRY_CLASSIFICATION;
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    int count = rs.getInt("count");
                    System.out.println("✅ 行业分类表有 " + count + " 条记录");
                }
            }
            
            // 查询公司数据
            sql = "SELECT COUNT(*) as count FROM " + TableNames.Layer1.COMPANY_LIST_INFO;
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    int count = rs.getInt("count");
                    System.out.println("✅ 公司列表表有 " + count + " 条记录");
                }
            }
            
            // 查询模块状态
            sql = "SELECT COUNT(*) as count FROM " + TableNames.System.MODULE_STATUS;
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    int count = rs.getInt("count");
                    System.out.println("✅ 模块状态表有 " + count + " 条记录");
                }
            }
            
            // 显示示例数据
            showSampleData(connection);
            
            return true;
            
        } catch (SQLException e) {
            System.err.println("❌ 测试数据查询失败: " + e.getMessage());
            return false;
        }
    }
    
    /**
     * 显示示例数据
     */
    private void showSampleData(Connection connection) throws SQLException {
        System.out.println("\n示例行业数据:");
        String sql = "SELECT industry_code, industry_name, industry_level FROM " + 
                    TableNames.Layer1.WIND_INDUSTRY_CLASSIFICATION + " LIMIT 3";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                String code = rs.getString("industry_code");
                String name = rs.getString("industry_name");
                int level = rs.getInt("industry_level");
                System.out.println("  " + code + " - " + name + " (L" + level + ")");
            }
        }
        
        System.out.println("\n示例公司数据:");
        sql = "SELECT company_name, stock_code, market FROM " + 
              TableNames.Layer1.COMPANY_LIST_INFO + " LIMIT 3";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                String companyName = rs.getString("company_name");
                String stockCode = rs.getString("stock_code");
                String market = rs.getString("market");
                System.out.println("  " + companyName + " (" + stockCode + ") - " + market);
            }
        }
    }
    
    /**
     * 测试表名配置
     */
    private boolean testTableNames() {
        System.out.println("\n测试表名配置...");
        
        try {
            // 测试表名获取
            String industryTable = TableNames.getTableName("LAYER1", "wind_industry", "industry_classification");
            System.out.println("✅ 行业分类表名: " + industryTable);
            
            String companyTable = TableNames.getTableName("LAYER1", "company_list", "company_info");
            System.out.println("✅ 公司信息表名: " + companyTable);
            
            // 显示所有表名配置
            System.out.println("\n所有表名配置:");
            Map<String, Map<String, String>> allTables = TableNames.getAllTables();
            for (Map.Entry<String, Map<String, String>> layerEntry : allTables.entrySet()) {
                String layer = layerEntry.getKey();
                Map<String, String> tables = layerEntry.getValue();
                System.out.println("  " + layer + ":");
                for (Map.Entry<String, String> tableEntry : tables.entrySet()) {
                    String tableName = tableEntry.getKey();
                    String tableId = tableEntry.getValue();
                    System.out.println("    " + tableName + ": " + tableId);
                }
            }
            
            return true;
            
        } catch (Exception e) {
            System.err.println("❌ 测试表名配置失败: " + e.getMessage());
            return false;
        }
    }
    
    /**
     * 获取数据库连接信息
     */
    public void printConnectionInfo() {
        System.out.println("数据库连接信息:");
        System.out.println("  JDBC URL: " + config.getJdbcUrl());
        System.out.println("  最大连接数: " + config.getMaxConnections());
        System.out.println("  最小连接数: " + config.getMinConnections());
        System.out.println("  连接超时: " + config.getConnectionTimeout() + "秒");
        
        Map<String, Object> connectionConfig = config.getConnectionConfig();
        System.out.println("  完整配置: " + connectionConfig);
    }
    
    /**
     * 测试数据库性能
     */
    public boolean performanceTest() {
        System.out.println("\n执行性能测试...");
        
        try (Connection connection = DriverManager.getConnection(config.getJdbcUrl(), config.getUsername(), config.getPassword())) {
            
            // 测试连接创建时间
            long startTime = System.currentTimeMillis();
            for (int i = 0; i < 10; i++) {
                try (Connection testConn = DriverManager.getConnection(config.getJdbcUrl(), config.getUsername(), config.getPassword())) {
                    // 简单查询
                    try (Statement stmt = testConn.createStatement();
                         ResultSet rs = stmt.executeQuery("SELECT 1")) {
                        rs.next();
                    }
                }
            }
            long endTime = System.currentTimeMillis();
            
            double avgTime = (endTime - startTime) / 10.0;
            System.out.println("✅ 平均连接时间: " + avgTime + "ms");
            
            if (avgTime < 1000) {
                System.out.println("✅ 连接性能良好");
                return true;
            } else {
                System.out.println("⚠️ 连接性能较慢");
                return false;
            }
            
        } catch (SQLException e) {
            System.err.println("❌ 性能测试失败: " + e.getMessage());
            return false;
        }
    }
}