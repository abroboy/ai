package com.windindustry.api;

import com.windindustry.service.RealTimeDataService;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.text.SimpleDateFormat;

public class ApiWebServer {
    
    public static void main(String[] args) throws Exception {
        System.out.println("========================================");
        System.out.println("万得行业分类API服务器启动中...");
        System.out.println("Java版本: " + System.getProperty("java.version"));
        System.out.println("========================================");
        
        HttpServer server = HttpServer.create(new InetSocketAddress(5001), 0);
        
        // 主页
        server.createContext("/", new HomeHandler());
        // 股票映射页面
        server.createContext("/stock-mappings", new PageHandler("src/main/resources/templates/stock-mappings.html"));
        // 数据分析页面
        server.createContext("/data-analysis", new PageHandler("src/main/resources/templates/data-analysis.html"));
        
        // API端点
        server.createContext("/api/stock-mappings", new StockMappingsHandler());
        server.createContext("/api/stock-mappings/stats", new StockStatsHandler());
        server.createContext("/api/stock-mappings/refresh", new RefreshDataHandler());
        server.createContext("/api/wind-industries", new IndustriesHandler());
        server.createContext("/api/market/distribution", new MarketDistributionHandler());
        server.createContext("/api/industry/distribution", new IndustryDistributionHandler());
        server.createContext("/api/capital-flow/trend", new CapitalFlowTrendHandler());
        server.createContext("/api/capital-flow/stats", new CapitalFlowStatsHandler());
        
        server.setExecutor(null);
        server.start();
        
        System.out.println("✅ API服务器启动成功！");
        System.out.println("访问地址: http://localhost:5001");
        System.out.println("股票映射管理: http://localhost:5001/stock-mappings");
        System.out.println("数据分析: http://localhost:5001/data-analysis");
        System.out.println("========================================");
    }
    
    static class HomeHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>万得行业分类仪表盘</title>
                <meta charset="UTF-8">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container mt-5">
                    <div class="row">
                        <div class="col-12">
                            <h1 class="text-center mb-4">万得行业分类仪表盘</h1>
                            <div class="alert alert-success text-center">
                                <h4>✅ API服务已启动！</h4>
                                <p>端口: 5001 | 状态: 运行中 | 所有API端点已可用</p>
                            </div>
                            
                            <div class="row mt-4">
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-body text-center">
                                            <h5 class="card-title">📊 股票映射管理</h5>
                                            <p class="card-text">管理股票与万得行业分类的映射关系</p>
                                            <a href="/stock-mappings" class="btn btn-primary">进入管理</a>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-body text-center">
                                            <h5 class="card-title">📈 数据分析</h5>
                                            <p class="card-text">查看股票资金流向和行业分析</p>
                                            <a href="/data-analysis" class="btn btn-info">查看分析</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mt-4">
                                <div class="alert alert-info">
                                    <h6>可用的API端点:</h6>
                                    <ul>
                                        <li><a href="/api/stock-mappings">/api/stock-mappings</a> - 股票映射数据</li>
                                        <li><a href="/api/stock-mappings/stats">/api/stock-mappings/stats</a> - 股票统计</li>
                                        <li><a href="/api/wind-industries">/api/wind-industries</a> - 行业分类</li>
                                        <li><a href="/api/market/distribution">/api/market/distribution</a> - 市场分布</li>
                                        <li><a href="/api/industry/distribution">/api/industry/distribution</a> - 行业分布</li>
                                        <li><a href="/api/capital-flow/trend">/api/capital-flow/trend</a> - 资金流向趋势</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """;
            
            sendResponse(exchange, 200, response, "text/html");
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
    
    static class StockMappingsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                // 从实时数据服务获取股票数据
                List<Map<String, Object>> stockData = RealTimeDataService.getStockMappingData();
                
                // 处理分页参数
                String query = exchange.getRequestURI().getQuery();
                int page = 0;
                int size = 20;
                
                if (query != null) {
                    String[] params = query.split("&");
                    for (String param : params) {
                        String[] kv = param.split("=");
                        if (kv.length == 2) {
                            if ("page".equals(kv[0])) {
                                page = Integer.parseInt(kv[1]);
                            } else if ("size".equals(kv[0])) {
                                size = Integer.parseInt(kv[1]);
                            }
                        }
                    }
                }
                
                int start = page * size;
                int end = Math.min(start + size, stockData.size());
                List<Map<String, Object>> pageData = stockData.subList(start, end);
                
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
                jsonBuilder.append("\"totalElements\": ").append(stockData.size()).append(",");
                jsonBuilder.append("\"totalPages\": ").append((int) Math.ceil((double) stockData.size() / size)).append(",");
                jsonBuilder.append("\"currentPage\": ").append(page).append(",");
                jsonBuilder.append("\"size\": ").append(size).append(",");
                jsonBuilder.append("\"numberOfElements\": ").append(pageData.size()).append(",");
                jsonBuilder.append("\"hasNext\": ").append(end < stockData.size()).append(",");
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
    
    static class StockStatsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                // 从实时数据服务获取统计数据
                Map<String, Object> stats = RealTimeDataService.getStatsData();
                
                StringBuilder jsonBuilder = new StringBuilder();
                jsonBuilder.append("{");
                jsonBuilder.append("\"success\": true,");
                jsonBuilder.append("\"data\": {");
                jsonBuilder.append("\"total_stocks\": ").append(stats.get("total_stocks")).append(",");
                jsonBuilder.append("\"mapped_count\": ").append(stats.get("mapped_count")).append(",");
                jsonBuilder.append("\"unmapped_count\": ").append(stats.get("unmapped_count")).append(",");
                jsonBuilder.append("\"a_stock_count\": ").append(stats.get("a_stock_count")).append(",");
                jsonBuilder.append("\"kc_stock_count\": ").append(stats.get("kc_stock_count"));
                jsonBuilder.append("}");
                jsonBuilder.append("}");
                
                sendResponse(exchange, 200, jsonBuilder.toString(), "application/json");
                
            } catch (Exception e) {
                String errorResponse = "{\"success\": false, \"error\": \"" + e.getMessage() + "\"}";
                sendResponse(exchange, 500, errorResponse, "application/json");
            }
        }
    }
    
    static class IndustriesHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                // 从实时数据服务获取行业数据
                List<Map<String, Object>> industryData = RealTimeDataService.getIndustryData();
                
                StringBuilder jsonBuilder = new StringBuilder();
                jsonBuilder.append("{");
                jsonBuilder.append("\"success\": true,");
                jsonBuilder.append("\"data\": [");
                
                for (int i = 0; i < industryData.size(); i++) {
                    if (i > 0) jsonBuilder.append(",");
                    Map<String, Object> industry = industryData.get(i);
                    jsonBuilder.append("{");
                    jsonBuilder.append("\"industryCode\": \"").append(industry.get("industryCode")).append("\",");
                    jsonBuilder.append("\"industryName\": \"").append(industry.get("industryName")).append("\",");
                    jsonBuilder.append("\"industryLevel\": ").append(industry.get("industryLevel"));
                    jsonBuilder.append("}");
                }
                
                jsonBuilder.append("],");
                jsonBuilder.append("\"total\": ").append(industryData.size());
                jsonBuilder.append("}");
                
                sendResponse(exchange, 200, jsonBuilder.toString(), "application/json");
                
            } catch (Exception e) {
                String errorResponse = "{\"success\": false, \"error\": \"" + e.getMessage() + "\"}";
                sendResponse(exchange, 500, errorResponse, "application/json");
            }
        }
    }
    
    static class MarketDistributionHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
            {
                "success": true,
                "data": [
                    {"market_type": "A股", "count": 19},
                    {"market_type": "科创板", "count": 2}
                ]
            }
            """;
            
            sendResponse(exchange, 200, response, "application/json");
        }
    }
    
    static class IndustryDistributionHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
            {
                "success": true,
                "data": [
                    {"industry_name": "银行", "count": 8},
                    {"industry_name": "证券", "count": 5},
                    {"industry_name": "房地产", "count": 4},
                    {"industry_name": "白酒", "count": 2},
                    {"industry_name": "医药", "count": 2}
                ]
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
                    {"date": "2025-01-02", "net_inflow": 12580, "total_inflow": 245680, "total_outflow": 233100},
                    {"date": "2025-01-03", "net_inflow": -8960, "total_inflow": 189750, "total_outflow": 198710},
                    {"date": "2025-01-06", "net_inflow": 25400, "total_inflow": 312560, "total_outflow": 287160},
                    {"date": "2025-01-07", "net_inflow": 18200, "total_inflow": 276540, "total_outflow": 258340},
                    {"date": "2025-01-08", "net_inflow": 32100, "total_inflow": 368900, "total_outflow": 336800}
                ]
            }
            """;
            
            sendResponse(exchange, 200, response, "application/json");
        }
    }
    
    static class CapitalFlowStatsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
            {
                "success": true,
                "data": {
                    "total_daily_inflow": 79320,
                    "total_weekly_inflow": 555440,
                    "positive_flow_count": 15,
                    "negative_flow_count": 6,
                    "total_stocks": 21,
                    "average_daily_inflow": 3777.14
                }
            }
            """;
            
            sendResponse(exchange, 200, response, "application/json");
        }
    }
    
    static class RefreshDataHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                if ("POST".equals(exchange.getRequestMethod())) {
                    // 手动刷新数据
                    RealTimeDataService.manualRefresh();
                    
                    String response = "{\"success\": true, \"message\": \"数据刷新成功\"}";
                    sendResponse(exchange, 200, response, "application/json");
                } else {
                    // 返回最后更新时间
                    long lastUpdateTime = RealTimeDataService.getLastUpdateTime();
                    String response = "{\"success\": true, \"lastUpdateTime\": " + lastUpdateTime + "}";
                    sendResponse(exchange, 200, response, "application/json");
                }
            } catch (Exception e) {
                String errorResponse = "{\"success\": false, \"error\": \"" + e.getMessage() + "\"}";
                sendResponse(exchange, 500, errorResponse, "application/json");
            }
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