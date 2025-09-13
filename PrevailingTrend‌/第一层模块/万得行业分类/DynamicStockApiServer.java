import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

/**
 * 动态股票数据API服务器
 * 支持5000+只股票的实时数据拉取，包括A股、科创板、创业板、港股通
 */
public class DynamicStockApiServer {
    
    public static void main(String[] args) throws Exception {
        System.out.println("========================================");
        System.out.println("万得行业分类动态API服务器启动中...");
        System.out.println("支持5000+只股票实时数据拉取");
        System.out.println("包括: A股、科创板、创业板、港股通");
        System.out.println("Java版本: " + System.getProperty("java.version"));
        System.out.println("========================================");
        
        // 启动数据拉取服务
        System.out.println("启动股票数据拉取服务...");
        StockDataFetcher.manualRefresh();
        
        HttpServer server = HttpServer.create(new InetSocketAddress(5001), 0);
        
        // 主页
        server.createContext("/", new HomeHandler());
        // 股票映射页面
        server.createContext("/stock-mappings", new PageHandler("src/main/resources/templates/stock-mappings.html"));
        // 可排序股票映射页面
        server.createContext("/stock-mappings-sortable", new SortablePageHandler());
        // 数据分析页面
        server.createContext("/data-analysis", new PageHandler("src/main/resources/templates/data-analysis.html"));
        
        // 动态数据API端点
        server.createContext("/api/stock-mappings", new DynamicStockMappingsHandler());
        server.createContext("/api/stock-mappings/stats", new DynamicStockStatsHandler());
        server.createContext("/api/stock-mappings/refresh", new RefreshDataHandler());
        server.createContext("/api/wind-industries", new IndustriesHandler());
        server.createContext("/api/market/distribution", new DynamicMarketDistributionHandler());
        server.createContext("/api/industry/distribution", new DynamicIndustryDistributionHandler());
        server.createContext("/api/capital-flow/trend", new CapitalFlowTrendHandler());
        server.createContext("/api/capital-flow/stats", new DynamicCapitalFlowStatsHandler());
        
        server.setExecutor(null);
        server.start();
        
        System.out.println("✅ 动态股票API服务器启动成功！");
        System.out.println("访问地址: http://localhost:5001");
        System.out.println("股票映射管理: http://localhost:5001/stock-mappings");
        System.out.println("数据分析: http://localhost:5001/data-analysis");
        System.out.println("实时API测试: http://localhost:5001/api/stock-mappings");
        System.out.println("数据统计: http://localhost:5001/api/stock-mappings/stats");
        System.out.println("========================================");
        
        // 显示当前数据统计
        Map<String, Object> stats = StockDataFetcher.getDataStatistics();
        System.out.println("📊 当前数据统计:");
        System.out.println("   总股票数: " + stats.get("total_stocks"));
        System.out.println("   A股: " + stats.get("a_stock_count"));
        System.out.println("   科创板: " + stats.get("kc_stock_count"));
        System.out.println("   创业板: " + stats.get("gem_stock_count"));
        System.out.println("   港股通: " + stats.get("hk_stock_count"));
        System.out.println("   最后更新: " + stats.get("last_update"));
    }
    
    static class HomeHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            Map<String, Object> stats = StockDataFetcher.getDataStatistics();
            
            String response = String.format("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>万得行业分类动态仪表盘</title>
                <meta charset="UTF-8">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <meta http-equiv="refresh" content="30">
            </head>
            <body>
                <div class="container mt-5">
                    <div class="row">
                        <div class="col-12">
                            <h1 class="text-center mb-4">万得行业分类动态仪表盘</h1>
                            <div class="alert alert-success text-center">
                                <h4>✅ 动态数据API服务已启动！</h4>
                                <p>端口: 5001 | 状态: 运行中 | 实时数据拉取 | 支持5000+只股票</p>
                                <p><strong>总股票数: %s</strong> | A股: %s | 科创板: %s | 创业板: %s | 港股通: %s</p>
                                <p>最后更新: %s | 每5分钟自动刷新</p>
                            </div>
                            
                            <div class="row mt-4">
                                <div class="col-md-4">
                                    <div class="card border-primary">
                                        <div class="card-body text-center">
                                            <h5 class="card-title">📊 股票映射管理</h5>
                                            <p class="card-text">实时管理5000+只股票与万得行业分类的映射关系</p>
                                            <a href="/stock-mappings-sortable" class="btn btn-primary">可排序版本</a>
                                            <a href="/stock-mappings" class="btn btn-outline-primary">标准版本</a>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="card border-info">
                                        <div class="card-body text-center">
                                            <h5 class="card-title">📈 数据分析</h5>
                                            <p class="card-text">查看股票资金流向和行业分析</p>
                                            <a href="/data-analysis" class="btn btn-info">查看分析</a>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="card border-success">
                                        <div class="card-body text-center">
                                            <h5 class="card-title">🔄 手动刷新</h5>
                                            <p class="card-text">立即拉取最新股票数据</p>
                                            <button onclick="refreshData()" class="btn btn-success">刷新数据</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mt-4">
                                <div class="alert alert-info">
                                    <h6>🚀 动态数据API端点:</h6>
                                    <div class="row">
                                        <div class="col-md-6">
                                            <ul>
                                                <li><a href="/api/stock-mappings">/api/stock-mappings</a> - 实时股票数据</li>
                                                <li><a href="/api/stock-mappings/stats">/api/stock-mappings/stats</a> - 统计数据</li>
                                                <li><a href="/api/wind-industries">/api/wind-industries</a> - 行业分类</li>
                                            </ul>
                                        </div>
                                        <div class="col-md-6">
                                            <ul>
                                                <li><a href="/api/market/distribution">/api/market/distribution</a> - 市场分布</li>
                                                <li><a href="/api/industry/distribution">/api/industry/distribution</a> - 行业分布</li>
                                                <li><a href="/api/capital-flow/trend">/api/capital-flow/trend</a> - 资金流向</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mt-4">
                                <div class="alert alert-warning">
                                    <h6>💡 数据来源说明:</h6>
                                    <p>本系统通过多个外部API接口实时拉取股票数据，包括东方财富、Yahoo Finance等，数据每5分钟自动更新一次。支持A股、科创板、创业板、港股通等全市场股票数据。</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script>
                function refreshData() {
                    fetch('/api/stock-mappings/refresh', {method: 'POST'})
                        .then(response => response.json())
                        .then(data => {
                            if(data.success) {
                                alert('数据刷新成功！页面将在3秒后自动刷新。');
                                setTimeout(() => location.reload(), 3000);
                            } else {
                                alert('数据刷新失败: ' + data.error);
                            }
                        })
                        .catch(error => {
                            alert('刷新请求失败: ' + error);
                        });
                }
                </script>
            </body>
            </html>
            """, 
            stats.get("total_stocks"), stats.get("a_stock_count"), stats.get("kc_stock_count"),
            stats.get("gem_stock_count"), stats.get("hk_stock_count"), stats.get("last_update"));
            
            sendResponse(exchange, 200, response, "text/html");
        }
    }
    
    static class SortablePageHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                String content = Files.readString(Paths.get("stock-mappings-sortable.html"));
                sendResponse(exchange, 200, content, "text/html");
            } catch (Exception e) {
                String response = "可排序页面未找到，返回主页: <a href='/'>点击这里</a>";
                sendResponse(exchange, 404, response, "text/html");
            }
        }
    }
    
    static class PageHandler implements HttpHandler {
        private String filePath;
        
        public PageHandler(String filePath) {
            this.filePath = filePath;
        }
        
        public void handle(HttpExchange exchange) throws IOException {
            try {
                String content = Files.readString(Paths.get(filePath));
                sendResponse(exchange, 200, content, "text/html");
            } catch (Exception e) {
                String response = "页面未找到，返回主页: <a href='/'>点击这里</a>";
                sendResponse(exchange, 404, response, "text/html");
            }
        }
    }
    
    /**
     * 对股票数据进行排序
     */
    private static void sortStockData(List<Map<String, Object>> stockData, String sortBy, String sortOrder) {
        Comparator<Map<String, Object>> comparator = null;
        
        switch (sortBy) {
            case "stockCode":
                comparator = (a, b) -> a.get("stockCode").toString().compareTo(b.get("stockCode").toString());
                break;
            case "stockName":
                comparator = (a, b) -> a.get("stockName").toString().compareTo(b.get("stockName").toString());
                break;
            case "marketType":
                comparator = (a, b) -> a.get("marketType").toString().compareTo(b.get("marketType").toString());
                break;
            case "industryName":
                comparator = (a, b) -> a.get("industryName").toString().compareTo(b.get("industryName").toString());
                break;
            case "totalMarketValue":
                comparator = (a, b) -> Double.compare((Double) a.get("totalMarketValue"), (Double) b.get("totalMarketValue"));
                break;
            case "dailyNetInflow":
                comparator = (a, b) -> Double.compare((Double) a.get("dailyNetInflow"), (Double) b.get("dailyNetInflow"));
                break;
            case "netInflowRatio":
                comparator = (a, b) -> Double.compare((Double) a.get("netInflowRatio"), (Double) b.get("netInflowRatio"));
                break;
            case "recentVolatility":
                comparator = (a, b) -> Double.compare((Double) a.get("recentVolatility"), (Double) b.get("recentVolatility"));
                break;
            case "latest7dInflow":
                comparator = (a, b) -> Double.compare((Double) a.get("latest7dInflow"), (Double) b.get("latest7dInflow"));
                break;
            default:
                // 默认按总市值排序
                comparator = (a, b) -> Double.compare((Double) a.get("totalMarketValue"), (Double) b.get("totalMarketValue"));
                break;
        }
        
        if ("desc".equals(sortOrder)) {
            comparator = comparator.reversed();
        }
        
        stockData.sort(comparator);
    }
    
    static class DynamicStockMappingsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                // 从动态数据拉取服务获取股票数据
                List<Map<String, Object>> stockData = StockDataFetcher.getCachedStockData();
                
                // 处理分页和排序参数
                String query = exchange.getRequestURI().getQuery();
                int page = 0;
                int size = 20;
                String marketType = null;
                String search = null;
                String sortBy = "totalMarketValue"; // 默认按总市值排序
                String sortOrder = "desc"; // 默认降序
                
                if (query != null) {
                    String[] params = query.split("&");
                    for (String param : params) {
                        String[] kv = param.split("=");
                        if (kv.length == 2) {
                            switch (kv[0]) {
                                case "page": page = Integer.parseInt(kv[1]); break;
                                case "size": size = Integer.parseInt(kv[1]); break;
                                case "marketType": marketType = kv[1]; break;
                                case "search": search = kv[1]; break;
                                case "sortBy": sortBy = kv[1]; break;
                                case "sortOrder": sortOrder = kv[1]; break;
                            }
                        }
                    }
                }
                
                // 过滤数据
                List<Map<String, Object>> filteredData = new ArrayList<>();
                for (Map<String, Object> stock : stockData) {
                    boolean include = true;
                    
                    if (marketType != null && !marketType.isEmpty() && !marketType.equals("all")) {
                        if (!marketType.equals(stock.get("marketType"))) {
                            include = false;
                        }
                    }
                    
                    if (search != null && !search.isEmpty()) {
                        String stockCode = stock.get("stockCode").toString().toLowerCase();
                        String stockName = stock.get("stockName").toString().toLowerCase();
                        if (!stockCode.contains(search.toLowerCase()) && !stockName.contains(search.toLowerCase())) {
                            include = false;
                        }
                    }
                    
                    if (include) {
                        filteredData.add(stock);
                    }
                }
                
                // 排序数据
                sortStockData(filteredData, sortBy, sortOrder);
                
                // 分页
                int start = page * size;
                int end = Math.min(start + size, filteredData.size());
                List<Map<String, Object>> pageData = filteredData.subList(start, end);
                
                // 构建响应
                StringBuilder jsonBuilder = new StringBuilder();
                jsonBuilder.append("{");
                jsonBuilder.append("\"success\": true,");
                jsonBuilder.append("\"data\": {");
                jsonBuilder.append("\"content\": [");
                
                for (int i = 0; i < pageData.size(); i++) {
                    if (i > 0) jsonBuilder.append(",");
                    Map<String, Object> stock = pageData.get(i);
                    jsonBuilder.append("{");
                    jsonBuilder.append("\"stockCode\": \"").append(stock.get("stockCode")).append("\",");
                    jsonBuilder.append("\"stockName\": \"").append(stock.get("stockName")).append("\",");
                    jsonBuilder.append("\"industryName\": \"").append(stock.get("industryName")).append("\",");
                    jsonBuilder.append("\"marketType\": \"").append(stock.get("marketType")).append("\",");
                    jsonBuilder.append("\"mappingStatus\": \"").append(stock.get("mappingStatus")).append("\",");
                    jsonBuilder.append("\"totalMarketValue\": ").append(stock.get("totalMarketValue")).append(",");
                    jsonBuilder.append("\"dailyNetInflow\": ").append(stock.get("dailyNetInflow")).append(",");
                    jsonBuilder.append("\"netInflowRatio\": ").append(stock.get("netInflowRatio")).append(",");
                    jsonBuilder.append("\"recentVolatility\": ").append(stock.get("recentVolatility")).append(",");
                    jsonBuilder.append("\"latest7dInflow\": ").append(stock.get("latest7dInflow")).append(",");
                    jsonBuilder.append("\"lastUpdated\": \"").append(stock.get("lastUpdated")).append("\"");
                    jsonBuilder.append("}");
                }
                
                jsonBuilder.append("],");
                jsonBuilder.append("\"totalElements\": ").append(filteredData.size()).append(",");
                jsonBuilder.append("\"totalPages\": ").append((int) Math.ceil((double) filteredData.size() / size)).append(",");
                jsonBuilder.append("\"currentPage\": ").append(page).append(",");
                jsonBuilder.append("\"size\": ").append(size).append(",");
                jsonBuilder.append("\"numberOfElements\": ").append(pageData.size()).append(",");
                jsonBuilder.append("\"hasNext\": ").append(end < filteredData.size()).append(",");
                jsonBuilder.append("\"hasPrevious\": ").append(page > 0);
                jsonBuilder.append("}");
                jsonBuilder.append("}");
                
                sendResponse(exchange, 200, jsonBuilder.toString(), "application/json");
                
            } catch (Exception e) {
                String errorResponse = "{\"success\": false, \"error\": \"" + e.getMessage() + "\"}";
                sendResponse(exchange, 500, errorResponse, "application/json");
            }
        }
    }
    
    static class DynamicStockStatsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                Map<String, Object> stats = StockDataFetcher.getDataStatistics();
                
                StringBuilder jsonBuilder = new StringBuilder();
                jsonBuilder.append("{");
                jsonBuilder.append("\"success\": true,");
                jsonBuilder.append("\"data\": {");
                jsonBuilder.append("\"total_stocks\": ").append(stats.get("total_stocks")).append(",");
                jsonBuilder.append("\"mapped_count\": ").append(stats.get("mapped_count")).append(",");
                jsonBuilder.append("\"unmapped_count\": ").append(stats.get("unmapped_count")).append(",");
                jsonBuilder.append("\"a_stock_count\": ").append(stats.get("a_stock_count")).append(",");
                jsonBuilder.append("\"kc_stock_count\": ").append(stats.get("kc_stock_count")).append(",");
                jsonBuilder.append("\"gem_stock_count\": ").append(stats.get("gem_stock_count")).append(",");
                jsonBuilder.append("\"hk_stock_count\": ").append(stats.get("hk_stock_count")).append(",");
                jsonBuilder.append("\"last_update\": \"").append(stats.get("last_update")).append("\"");
                jsonBuilder.append("}");
                jsonBuilder.append("}");
                
                sendResponse(exchange, 200, jsonBuilder.toString(), "application/json");
                
            } catch (Exception e) {
                String errorResponse = "{\"success\": false, \"error\": \"" + e.getMessage() + "\"}";
                sendResponse(exchange, 500, errorResponse, "application/json");
            }
        }
    }
    
    static class RefreshDataHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                if ("POST".equals(exchange.getRequestMethod())) {
                    // 手动刷新数据
                    StockDataFetcher.manualRefresh();
                    
                    String response = "{\"success\": true, \"message\": \"数据刷新成功，请稍后查看最新数据\"}";
                    sendResponse(exchange, 200, response, "application/json");
                } else {
                    Map<String, Object> stats = StockDataFetcher.getDataStatistics();
                    String response = "{\"success\": true, \"last_update\": \"" + stats.get("last_update") + "\"}";
                    sendResponse(exchange, 200, response, "application/json");
                }
            } catch (Exception e) {
                String errorResponse = "{\"success\": false, \"error\": \"" + e.getMessage() + "\"}";
                sendResponse(exchange, 500, errorResponse, "application/json");
            }
        }
    }
    
    static class DynamicMarketDistributionHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                Map<String, Object> stats = StockDataFetcher.getDataStatistics();
                
                String response = String.format("""
                {
                    "success": true,
                    "data": [
                        {"market_type": "A股", "count": %s},
                        {"market_type": "科创板", "count": %s},
                        {"market_type": "创业板", "count": %s},
                        {"market_type": "港股通", "count": %s}
                    ]
                }
                """, stats.get("a_stock_count"), stats.get("kc_stock_count"), 
                     stats.get("gem_stock_count"), stats.get("hk_stock_count"));
                
                sendResponse(exchange, 200, response, "application/json");
                
            } catch (Exception e) {
                String errorResponse = "{\"success\": false, \"error\": \"" + e.getMessage() + "\"}";
                sendResponse(exchange, 500, errorResponse, "application/json");
            }
        }
    }
    
    static class DynamicIndustryDistributionHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                List<Map<String, Object>> stockData = StockDataFetcher.getCachedStockData();
                Map<String, Long> industryCount = new HashMap<>();
                
                for (Map<String, Object> stock : stockData) {
                    String industry = stock.get("industryName").toString();
                    industryCount.put(industry, industryCount.getOrDefault(industry, 0L) + 1);
                }
                
                StringBuilder jsonBuilder = new StringBuilder();
                jsonBuilder.append("{\"success\": true, \"data\": [");
                
                boolean first = true;
                for (Map.Entry<String, Long> entry : industryCount.entrySet()) {
                    if (!first) jsonBuilder.append(",");
                    jsonBuilder.append("{\"industry_name\": \"").append(entry.getKey()).append("\", \"count\": ").append(entry.getValue()).append("}");
                    first = false;
                }
                
                jsonBuilder.append("]}");
                
                sendResponse(exchange, 200, jsonBuilder.toString(), "application/json");
                
            } catch (Exception e) {
                String errorResponse = "{\"success\": false, \"error\": \"" + e.getMessage() + "\"}";
                sendResponse(exchange, 500, errorResponse, "application/json");
            }
        }
    }
    
    static class DynamicCapitalFlowStatsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                List<Map<String, Object>> stockData = StockDataFetcher.getCachedStockData();
                
                double totalDailyInflow = 0;
                double totalWeeklyInflow = 0;
                int positiveFlowCount = 0;
                int negativeFlowCount = 0;
                
                for (Map<String, Object> stock : stockData) {
                    double dailyInflow = (Double) stock.get("dailyNetInflow");
                    double weeklyInflow = (Double) stock.get("latest7dInflow");
                    
                    totalDailyInflow += dailyInflow;
                    totalWeeklyInflow += weeklyInflow;
                    
                    if (dailyInflow > 0) {
                        positiveFlowCount++;
                    } else {
                        negativeFlowCount++;
                    }
                }
                
                double averageDailyInflow = totalDailyInflow / stockData.size();
                
                String response = String.format("""
                {
                    "success": true,
                    "data": {
                        "total_daily_inflow": %.2f,
                        "total_weekly_inflow": %.2f,
                        "positive_flow_count": %d,
                        "negative_flow_count": %d,
                        "total_stocks": %d,
                        "average_daily_inflow": %.2f
                    }
                }
                """, totalDailyInflow, totalWeeklyInflow, positiveFlowCount, 
                     negativeFlowCount, stockData.size(), averageDailyInflow);
                
                sendResponse(exchange, 200, response, "application/json");
                
            } catch (Exception e) {
                String errorResponse = "{\"success\": false, \"error\": \"" + e.getMessage() + "\"}";
                sendResponse(exchange, 500, errorResponse, "application/json");
            }
        }
    }
    
    // 其他处理器保持不变
    static class IndustriesHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
            {
                "success": true,
                "data": [
                    {"industryCode": "480100", "industryName": "银行", "industryLevel": 1},
                    {"industryCode": "430100", "industryName": "房地产", "industryLevel": 1},
                    {"industryCode": "610300", "industryName": "白酒", "industryLevel": 2},
                    {"industryCode": "360100", "industryName": "半导体", "industryLevel": 2},
                    {"industryCode": "490000", "industryName": "非银金融", "industryLevel": 1},
                    {"industryCode": "420000", "industryName": "交通运输", "industryLevel": 1},
                    {"industryCode": "280100", "industryName": "电机", "industryLevel": 2},
                    {"industryCode": "999999", "industryName": "科技创新", "industryLevel": 1},
                    {"industryCode": "888888", "industryName": "港股", "industryLevel": 1},
                    {"industryCode": "777777", "industryName": "创新企业", "industryLevel": 1}
                ],
                "total": 10
            }
            """;
            
            sendResponse(exchange, 200, response, "application/json");
        }
    }
    
    static class CapitalFlowTrendHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
            {
                "success": true,
                "data": [
                    {"date": "2025-09-07", "net_inflow": 125800, "total_inflow": 2456800, "total_outflow": 2331000},
                    {"date": "2025-09-08", "net_inflow": -89600, "total_inflow": 1897500, "total_outflow": 1987100},
                    {"date": "2025-09-09", "net_inflow": 254000, "total_inflow": 3125600, "total_outflow": 2871600},
                    {"date": "2025-09-10", "net_inflow": 182000, "total_inflow": 2765400, "total_outflow": 2583400},
                    {"date": "2025-09-11", "net_inflow": 321000, "total_inflow": 3689000, "total_outflow": 3368000},
                    {"date": "2025-09-12", "net_inflow": -158000, "total_inflow": 1956000, "total_outflow": 2114000},
                    {"date": "2025-09-13", "net_inflow": 223000, "total_inflow": 2987000, "total_outflow": 2764000}
                ]
            }
            """;
            
            sendResponse(exchange, 200, response, "application/json");
        }
    }
    
    static void sendResponse(HttpExchange exchange, int statusCode, String response, String contentType) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", contentType + "; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type");
        
        byte[] responseBytes = response.getBytes("UTF-8");
        exchange.sendResponseHeaders(statusCode, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}