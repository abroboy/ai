package com.windindustry.util;

import java.sql.*;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

/**
 * 扩展股票数据生成工具
 * 快速生成200+只股票数据
 * 
 * @author 大势所趋风险框架团队
 * @version 1.0
 */
public class StockDataGenerator {
    
    // 数据库配置
    private static final String DB_HOST = "localhost";
    private static final int DB_PORT = 3306;
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "rr1234RR";
    private static final String DB_DATABASE = "pt";
    
    private static final String JDBC_URL = String.format(
        "jdbc:mysql://%s:%d/%s?characterEncoding=utf8mb4&useSSL=false&allowMultiQueries=true&serverTimezone=Asia/Shanghai",
        DB_HOST, DB_PORT, DB_DATABASE
    );
    
    /**
     * 主方法 - 执行股票数据生成
     */
    public static void main(String[] args) {
        System.out.println("=".repeat(60));
        System.out.println("万得行业分类模块 - 扩展股票数据生成");
        System.out.println("=".repeat(60));
        
        StockDataGenerator generator = new StockDataGenerator();
        boolean success = generator.generateMoreStocks();
        
        if (success) {
            System.out.println("\n✅ 股票数据扩展完成！");
            System.out.println("\n接下来可以:");
            System.out.println("1. 启动API服务器: java RealTimeDataService");
            System.out.println("2. 测试数据接口: http://localhost:5001/api/stock-mappings");
        } else {
            System.out.println("✗ 股票数据扩展失败");
        }
    }
    
    /**
     * 获取数据库连接
     */
    private Connection getDbConnection() throws SQLException {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            return DriverManager.getConnection(JDBC_URL, DB_USER, DB_PASSWORD);
        } catch (ClassNotFoundException e) {
            throw new SQLException("MySQL驱动未找到", e);
        }
    }
    
    /**
     * 生成200+只股票数据
     */
    public boolean generateMoreStocks() {
        System.out.println("开始生成200+只股票数据...");
        
        try (Connection connection = getDbConnection()) {
            
            // 清理现有数据
            try (Statement stmt = connection.createStatement()) {
                stmt.execute("DELETE FROM l1_wind_stock_mapping");
                stmt.execute("ALTER TABLE l1_wind_stock_mapping AUTO_INCREMENT = 1");
            }
            
            // 生成股票数据
            List<StockData> stockDataList = generateStockDataList();
            
            // 插入数据
            insertStockData(connection, stockDataList);
            
            // 显示统计信息
            showStatistics(connection);
            
            return true;
            
        } catch (SQLException e) {
            System.err.println("✗ 生成股票数据失败: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }
    
    /**
     * 生成股票数据列表
     */
    private List<StockData> generateStockDataList() {
        List<StockData> stockDataList = new ArrayList<>();
        
        // 行业映射
        Industry[] industries = {
            new Industry("480100", "银行"),
            new Industry("610300", "白酒"),
            new Industry("360100", "半导体"),
            new Industry("420000", "交通运输"),
            new Industry("430100", "房地产开发"),
            new Industry("610000", "食品饮料"),
            new Industry("270200", "通用机械"),
            new Industry("280100", "电机"),
            new Industry("330100", "白色家电"),
            new Industry("490000", "非银金融"),
            new Industry("240000", "建筑材料"),
            new Industry("230000", "基础化工"),
            new Industry("210000", "有色金属"),
            new Industry("410100", "电力"),
            new Industry("620000", "纺织服装"),
            new Industry("460000", "休闲服务"),
            new Industry("720000", "传媒"),
            new Industry("450000", "商业贸易")
        };
        
        // 股票前缀
        String[] prefixes = {"000", "002", "300", "600", "601", "603", "688", "301"};
        
        // 基础股票数据
        BaseStock[] baseStocks = {
            new BaseStock("000001", "平安银行", "480100", "银行"),
            new BaseStock("000002", "万科A", "430100", "房地产开发"),
            new BaseStock("000858", "五粮液", "610300", "白酒"),
            new BaseStock("002415", "海康威视", "360100", "半导体"),
            new BaseStock("300059", "东方财富", "490000", "非银金融"),
            new BaseStock("600519", "贵州茅台", "610300", "白酒"),
            new BaseStock("600036", "招商银行", "480100", "银行"),
            new BaseStock("000725", "京东方A", "360100", "半导体"),
            new BaseStock("002594", "比亚迪", "420000", "交通运输"),
            new BaseStock("300750", "宁德时代", "280100", "电机")
        };
        
        Set<String> usedCodes = new HashSet<>();
        
        // 添加基础股票
        for (BaseStock baseStock : baseStocks) {
            usedCodes.add(baseStock.stockCode);
            StockData stockData = createStockData(baseStock.stockCode, baseStock.stockName, 
                                                baseStock.industryCode, baseStock.industryName);
            stockDataList.add(stockData);
        }
        
        // 生成190只额外股票
        Random random = new Random();
        String[] companyPrefixes = {"华为", "中兴", "海尔", "美的", "格力", "万科", "招商", "平安", "工商", "建设", "中国", "北京", "上海", "深圳", "广州", "杭州", "苏州", "南京", "青岛", "大连"};
        String[] companySuffixes = {"科技", "股份", "集团", "有限", "控股", "实业", "发展", "投资", "电子", "材料", "制造", "能源", "环保", "生物", "医药", "食品", "服装", "贸易", "地产", "银行"};
        
        for (int i = 0; i < 190; i++) {
            // 生成唯一的股票代码
            String stockCode;
            do {
                String prefix = prefixes[random.nextInt(prefixes.length)];
                int number = random.nextInt(900) + 100;
                stockCode = prefix + String.format("%03d", number);
            } while (usedCodes.contains(stockCode));
            
            usedCodes.add(stockCode);
            
            // 随机选择行业
            Industry industry = industries[random.nextInt(industries.length)];
            
            // 生成股票名称
            String stockName = companyPrefixes[random.nextInt(companyPrefixes.length)] + 
                             companySuffixes[random.nextInt(companySuffixes.length)];
            
            StockData stockData = createStockData(stockCode, stockName, industry.code, industry.name);
            stockDataList.add(stockData);
        }
        
        return stockDataList;
    }
    
    /**
     * 创建股票数据对象
     */
    private StockData createStockData(String stockCode, String stockName, String industryCode, String industryName) {
        ThreadLocalRandom random = ThreadLocalRandom.current();
        
        // 确定市场类型
        String marketType;
        if (stockCode.startsWith("688") || stockCode.startsWith("301")) {
            marketType = "科创板";
        } else {
            marketType = "A股";
        }
        
        // 生成随机财务数据
        double totalMarketValue = random.nextDouble(30000, 1500000);
        double dailyNetInflow = random.nextDouble(-40000, 40000);
        double netInflowRatio = random.nextDouble(-4.0, 5.0);
        double recentVolatility = random.nextDouble(0.01, 0.08);
        double latest7dInflow = dailyNetInflow * 7 + random.nextDouble(-80000, 80000);
        
        return new StockData(
            stockCode, stockName, marketType, industryCode, industryName, "已映射",
            Math.round(totalMarketValue), Math.round(dailyNetInflow * 100.0) / 100.0,
            Math.round(netInflowRatio * 100.0) / 100.0, Math.round(recentVolatility * 10000.0) / 10000.0,
            Math.round(latest7dInflow * 100.0) / 100.0, "正常"
        );
    }
    
    /**
     * 插入股票数据
     */
    private void insertStockData(Connection connection, List<StockData> stockDataList) throws SQLException {
        String insertSql = """
            INSERT INTO l1_wind_stock_mapping 
            (stock_code, stock_name, market_type, industry_code, industry_name, mapping_status, 
             total_market_value, daily_net_inflow, net_inflow_ratio, recent_volatility, 
             latest_7d_inflow, operation_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """;
        
        try (PreparedStatement pstmt = connection.prepareStatement(insertSql)) {
            for (StockData stock : stockDataList) {
                pstmt.setString(1, stock.stockCode);
                pstmt.setString(2, stock.stockName);
                pstmt.setString(3, stock.marketType);
                pstmt.setString(4, stock.industryCode);
                pstmt.setString(5, stock.industryName);
                pstmt.setString(6, stock.mappingStatus);
                pstmt.setDouble(7, stock.totalMarketValue);
                pstmt.setDouble(8, stock.dailyNetInflow);
                pstmt.setDouble(9, stock.netInflowRatio);
                pstmt.setDouble(10, stock.recentVolatility);
                pstmt.setDouble(11, stock.latest7dInflow);
                pstmt.setString(12, stock.operationStatus);
                pstmt.addBatch();
            }
            
            pstmt.executeBatch();
            connection.commit();
            
            System.out.println("✅ 成功生成 " + stockDataList.size() + " 只股票数据");
        }
    }
    
    /**
     * 显示统计信息
     */
    private void showStatistics(Connection connection) throws SQLException {
        // 市场分布统计
        String marketSql = "SELECT market_type, COUNT(*) FROM l1_wind_stock_mapping GROUP BY market_type";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(marketSql)) {
            
            while (rs.next()) {
                String market = rs.getString(1);
                int count = rs.getInt(2);
                System.out.println("  " + market + ": " + count + " 只股票");
            }
        }
        
        // 行业分布统计
        String industrySql = "SELECT industry_name, COUNT(*) FROM l1_wind_stock_mapping GROUP BY industry_name ORDER BY COUNT(*) DESC LIMIT 10";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(industrySql)) {
            
            System.out.println("\n热门行业 (前10):");
            while (rs.next()) {
                String industry = rs.getString(1);
                int count = rs.getInt(2);
                System.out.println("  " + industry + ": " + count + " 只股票");
            }
        }
    }
    
    /**
     * 行业数据类
     */
    private static class Industry {
        public final String code;
        public final String name;
        
        public Industry(String code, String name) {
            this.code = code;
            this.name = name;
        }
    }
    
    /**
     * 基础股票数据类
     */
    private static class BaseStock {
        public final String stockCode;
        public final String stockName;
        public final String industryCode;
        public final String industryName;
        
        public BaseStock(String stockCode, String stockName, String industryCode, String industryName) {
            this.stockCode = stockCode;
            this.stockName = stockName;
            this.industryCode = industryCode;
            this.industryName = industryName;
        }
    }
    
    /**
     * 股票数据类
     */
    private static class StockData {
        public final String stockCode;
        public final String stockName;
        public final String marketType;
        public final String industryCode;
        public final String industryName;
        public final String mappingStatus;
        public final double totalMarketValue;
        public final double dailyNetInflow;
        public final double netInflowRatio;
        public final double recentVolatility;
        public final double latest7dInflow;
        public final String operationStatus;
        
        public StockData(String stockCode, String stockName, String marketType, String industryCode, 
                        String industryName, String mappingStatus, double totalMarketValue, 
                        double dailyNetInflow, double netInflowRatio, double recentVolatility, 
                        double latest7dInflow, String operationStatus) {
            this.stockCode = stockCode;
            this.stockName = stockName;
            this.marketType = marketType;
            this.industryCode = industryCode;
            this.industryName = industryName;
            this.mappingStatus = mappingStatus;
            this.totalMarketValue = totalMarketValue;
            this.dailyNetInflow = dailyNetInflow;
            this.netInflowRatio = netInflowRatio;
            this.recentVolatility = recentVolatility;
            this.latest7dInflow = latest7dInflow;
            this.operationStatus = operationStatus;
        }
    }
}