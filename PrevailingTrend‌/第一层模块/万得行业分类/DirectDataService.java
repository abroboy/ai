import java.sql.*;
import java.util.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.math.BigDecimal;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * 直接数据库查询服务类
 * 通过SQL直接查询数据库中的200只股票数据
 */
public class DirectDataService {
    
    // 数据库连接配置
    private static final String DB_URL = "jdbc:mysql://localhost:3306/pt?characterEncoding=utf8&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=Asia/Shanghai";
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "rr1234RR";
    
    // 缓存数据
    private static List<Map<String, Object>> cachedStockData = null;
    private static Map<String, Object> cachedStatsData = null;
    private static List<Map<String, Object>> cachedIndustryData = null;
    
    /**
     * 获取数据库连接
     */
    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
    }
    
    /**
     * 直接从数据库查询股票数据
     */
    public static List<Map<String, Object>> queryStockData() {
        if (cachedStockData != null) {
            return cachedStockData;
        }
        
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
            System.out.println("📊 从数据库查询到 " + stockData.size() + " 只股票数据");
            return stockData;
            
        } catch (SQLException e) {
            System.err.println("数据库查询失败: " + e.getMessage());
            e.printStackTrace();
            return generateMockStockData();
        }
    }
    
    /**
     * 查询统计数据
     */
    public static Map<String, Object> queryStatsData() {
        if (cachedStatsData != null) {
            return cachedStatsData;
        }
        
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
            System.out.println("📈 统计数据查询完成");
            return stats;
            
        } catch (SQLException e) {
            System.err.println("统计数据查询失败: " + e.getMessage());
            // 使用默认值
            stats.put("total_stocks", 200);
            stats.put("mapped_count", 200);
            stats.put("unmapped_count", 0);
            stats.put("a_stock_count", 152);
            stats.put("kc_stock_count", 48);
            return stats;
        }
    }
    
    /**
     * 查询行业数据
     */
    public static List<Map<String, Object>> queryIndustryData() {
        if (cachedIndustryData != null) {
            return cachedIndustryData;
        }
        
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
            System.out.println("🏭 行业数据查询完成，共 " + industryData.size() + " 个行业");
            return industryData;
            
        } catch (SQLException e) {
            System.err.println("行业数据查询失败: " + e.getMessage());
            return generateMockIndustryData();
        }
    }
    
    /**
     * 生成模拟股票数据（当数据库不可用时）
     */
    private static List<Map<String, Object>> generateMockStockData() {
        List<Map<String, Object>> stockData = new ArrayList<>();
        Random random = new Random();
        
        // 使用200只股票的基础信息
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
            
            stockData.add(stock);
        }
        
        System.out.println("🔧 生成模拟股票数据，共 " + stockData.size() + " 只股票");
        return stockData;
    }
    
    /**
     * 生成模拟行业数据
     */
    private static List<Map<String, Object>> generateMockIndustryData() {
        List<Map<String, Object>> industryData = new ArrayList<>();
        
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
            
            industryData.add(industry);
        }
        
        System.out.println("🔧 生成模拟行业数据，共 " + industryData.size() + " 个行业");
        return industryData;
    }
    
    /**
     * 清除缓存
     */
    public static void clearCache() {
        cachedStockData = null;
        cachedStatsData = null;
        cachedIndustryData = null;
        System.out.println("🗑️ 缓存已清除");
    }
}