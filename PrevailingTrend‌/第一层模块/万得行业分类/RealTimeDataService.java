import java.sql.*;
import java.util.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.math.BigDecimal;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * 实时数据服务类
 * 从数据库实时拉取股票映射数据和资金流向数据
 */
public class RealTimeDataService {
    
    // 数据库连接配置
    private static final String DB_URL = "jdbc:mysql://localhost:3306/pt?characterEncoding=utf8&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=Asia/Shanghai";
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "rr1234RR";
    
    // 定时刷新执行器
    private static final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
    
    // 缓存数据
    private static List<Map<String, Object>> cachedStockData = new ArrayList<>();
    private static Map<String, Object> cachedStatsData = new HashMap<>();
    private static List<Map<String, Object>> cachedIndustryData = new ArrayList<>();
    private static long lastUpdateTime = 0;
    
    static {
        // 启动时立即加载数据
        refreshAllData();
        
        // 每30秒刷新一次数据
        scheduler.scheduleAtFixedRate(() -> {
            try {
                refreshAllData();
                System.out.println("✅ 数据刷新完成: " + LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            } catch (Exception e) {
                System.err.println("❌ 数据刷新失败: " + e.getMessage());
            }
        }, 30, 30, TimeUnit.SECONDS);
    }
    
    /**
     * 获取数据库连接
     */
    private static Connection getConnection() throws SQLException {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            return DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
        } catch (ClassNotFoundException e) {
            throw new SQLException("MySQL驱动未找到", e);
        }
    }
    
    /**
     * 刷新所有数据
     */
    public static void refreshAllData() {
        try {
            refreshStockMappingData();
            refreshStatsData();
            refreshIndustryData();
            lastUpdateTime = System.currentTimeMillis();
        } catch (Exception e) {
            System.err.println("刷新数据失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * 从数据库实时拉取股票映射数据
     */
    private static void refreshStockMappingData() {
        List<Map<String, Object>> stockData = new ArrayList<>();
        
        String sql = """
            SELECT 
                stock_code,
                stock_name,
                market_type,
                industry_code,
                industry_name,
                mapping_status,
                total_market_value,
                daily_net_inflow,
                net_inflow_ratio,
                recent_volatility,
                latest_7d_inflow,
                last_updated,
                operation_status
            FROM l1_wind_stock_mapping 
            WHERE is_active = TRUE 
            ORDER BY total_market_value DESC 
            LIMIT 200
            """;
        
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                Map<String, Object> stock = new HashMap<>();
                stock.put("stockCode", rs.getString("stock_code"));
                stock.put("stockName", rs.getString("stock_name"));
                stock.put("marketType", rs.getString("market_type"));
                stock.put("industryCode", rs.getString("industry_code"));
                stock.put("industryName", rs.getString("industry_name"));
                stock.put("mappingStatus", rs.getString("mapping_status"));
                stock.put("totalMarketValue", rs.getBigDecimal("total_market_value"));
                stock.put("dailyNetInflow", rs.getBigDecimal("daily_net_inflow"));
                stock.put("netInflowRatio", rs.getBigDecimal("net_inflow_ratio"));
                stock.put("recentVolatility", rs.getBigDecimal("recent_volatility"));
                stock.put("latest7dInflow", rs.getBigDecimal("latest_7d_inflow"));
                stock.put("lastUpdated", rs.getTimestamp("last_updated"));
                stock.put("operationStatus", rs.getString("operation_status"));
                
                stockData.add(stock);
            }
            
            cachedStockData = stockData;
            System.out.println("📊 股票数据刷新完成，共 " + stockData.size() + " 只股票");
            
        } catch (SQLException e) {
            System.err.println("获取股票数据失败: " + e.getMessage());
            // 如果数据库查询失败，生成模拟数据
            if (cachedStockData.isEmpty()) {
                generateMockStockData();
            }
        }
    }
    
    /**
     * 刷新统计数据
     */
    private static void refreshStatsData() {
        Map<String, Object> stats = new HashMap<>();
        
        try (Connection conn = getConnection()) {
            // 总股票数
            try (PreparedStatement stmt = conn.prepareStatement("SELECT COUNT(*) FROM l1_wind_stock_mapping WHERE is_active = TRUE")) {
                ResultSet rs = stmt.executeQuery();
                if (rs.next()) {
                    stats.put("total_stocks", rs.getInt(1));
                }
            }
            
            // 已映射股票数
            try (PreparedStatement stmt = conn.prepareStatement("SELECT COUNT(*) FROM l1_wind_stock_mapping WHERE mapping_status = '已映射'")) {
                ResultSet rs = stmt.executeQuery();
                if (rs.next()) {
                    stats.put("mapped_count", rs.getInt(1));
                }
            }
            
            // 未映射股票数
            try (PreparedStatement stmt = conn.prepareStatement("SELECT COUNT(*) FROM l1_wind_stock_mapping WHERE mapping_status = '未映射'")) {
                ResultSet rs = stmt.executeQuery();
                if (rs.next()) {
                    stats.put("unmapped_count", rs.getInt(1));
                }
            }
            
            // A股数量
            try (PreparedStatement stmt = conn.prepareStatement("SELECT COUNT(*) FROM l1_wind_stock_mapping WHERE market_type = 'A股'")) {
                ResultSet rs = stmt.executeQuery();
                if (rs.next()) {
                    stats.put("a_stock_count", rs.getInt(1));
                }
            }
            
            // 科创板数量
            try (PreparedStatement stmt = conn.prepareStatement("SELECT COUNT(*) FROM l1_wind_stock_mapping WHERE market_type = '科创板'")) {
                ResultSet rs = stmt.executeQuery();
                if (rs.next()) {
                    stats.put("kc_stock_count", rs.getInt(1));
                }
            }
            
            cachedStatsData = stats;
            System.out.println("📈 统计数据刷新完成");
            
        } catch (SQLException e) {
            System.err.println("获取统计数据失败: " + e.getMessage());
            // 使用默认值
            if (cachedStatsData.isEmpty()) {
                cachedStatsData.put("total_stocks", 200);
                cachedStatsData.put("mapped_count", 180);
                cachedStatsData.put("unmapped_count", 20);
                cachedStatsData.put("a_stock_count", 185);
                cachedStatsData.put("kc_stock_count", 15);
            }
        }
    }
    
    /**
     * 刷新行业数据
     */
    private static void refreshIndustryData() {
        List<Map<String, Object>> industryData = new ArrayList<>();
        
        String sql = """
            SELECT 
                industry_code,
                industry_name,
                industry_level,
                parent_industry_code,
                industry_description
            FROM l1_wind_industry_classification 
            WHERE is_active = TRUE 
            ORDER BY industry_level, industry_code
            """;
        
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                Map<String, Object> industry = new HashMap<>();
                industry.put("industryCode", rs.getString("industry_code"));
                industry.put("industryName", rs.getString("industry_name"));
                industry.put("industryLevel", rs.getInt("industry_level"));
                industry.put("parentIndustryCode", rs.getString("parent_industry_code"));
                industry.put("industryDescription", rs.getString("industry_description"));
                
                industryData.add(industry);
            }
            
            cachedIndustryData = industryData;
            System.out.println("🏭 行业数据刷新完成，共 " + industryData.size() + " 个行业");
            
        } catch (SQLException e) {
            System.err.println("获取行业数据失败: " + e.getMessage());
            // 使用默认行业数据
            if (cachedIndustryData.isEmpty()) {
                generateMockIndustryData();
            }
        }
    }
    
    /**
     * 生成模拟股票数据（当数据库不可用时）
     */
    private static void generateMockStockData() {
        cachedStockData = new ArrayList<>();
        Random random = new Random();
        
        String[][] stockInfo = {
            {"000001", "平安银行", "银行"},
            {"000002", "万科A", "房地产"},
            {"000858", "五粮液", "白酒"},
            {"002415", "海康威视", "安防"},
            {"300059", "东方财富", "证券"},
            {"600519", "贵州茅台", "白酒"},
            {"600036", "招商银行", "银行"},
            {"000725", "京东方A", "半导体"},
            {"002594", "比亚迪", "新能源汽车"},
            {"300750", "宁德时代", "新能源"}
        };
        
        for (String[] info : stockInfo) {
            Map<String, Object> stock = new HashMap<>();
            stock.put("stockCode", info[0]);
            stock.put("stockName", info[1]);
            stock.put("industryName", info[2]);
            stock.put("marketType", "A股");
            stock.put("mappingStatus", "已映射");
            stock.put("totalMarketValue", 50000 + random.nextInt(500000));
            stock.put("dailyNetInflow", -10000 + random.nextInt(20000));
            stock.put("netInflowRatio", -0.05 + random.nextDouble() * 0.1);
            stock.put("recentVolatility", 0.01 + random.nextDouble() * 0.05);
            stock.put("latest7dInflow", -50000 + random.nextInt(100000));
            stock.put("lastUpdated", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            cachedStockData.add(stock);
        }
        
        System.out.println("🔧 生成模拟股票数据，共 " + cachedStockData.size() + " 只股票");
    }
    
    /**
     * 生成模拟行业数据
     */
    private static void generateMockIndustryData() {
        cachedIndustryData = new ArrayList<>();
        
        String[][] industryInfo = {
            {"480100", "银行", "1"},
            {"430100", "房地产开发", "1"},
            {"610300", "白酒", "2"},
            {"360100", "半导体", "2"},
            {"490000", "非银金融", "1"},
            {"420000", "交通运输", "1"},
            {"280100", "电机", "2"}
        };
        
        for (String[] info : industryInfo) {
            Map<String, Object> industry = new HashMap<>();
            industry.put("industryCode", info[0]);
            industry.put("industryName", info[1]);
            industry.put("industryLevel", Integer.parseInt(info[2]));
            
            cachedIndustryData.add(industry);
        }
        
        System.out.println("🔧 生成模拟行业数据，共 " + cachedIndustryData.size() + " 个行业");
    }
    
    /**
     * 获取股票映射数据
     */
    public static List<Map<String, Object>> getStockMappingData() {
        return new ArrayList<>(cachedStockData);
    }
    
    /**
     * 获取统计数据
     */
    public static Map<String, Object> getStatsData() {
        return new HashMap<>(cachedStatsData);
    }
    
    /**
     * 获取行业数据
     */
    public static List<Map<String, Object>> getIndustryData() {
        return new ArrayList<>(cachedIndustryData);
    }
    
    /**
     * 获取最后更新时间
     */
    public static long getLastUpdateTime() {
        return lastUpdateTime;
    }
    
    /**
     * 手动刷新数据
     */
    public static void manualRefresh() {
        System.out.println("🔄 手动刷新数据...");
        refreshAllData();
    }
}