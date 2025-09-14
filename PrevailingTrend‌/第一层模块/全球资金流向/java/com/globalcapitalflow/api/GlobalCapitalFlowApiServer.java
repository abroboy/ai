package com.globalcapitalflow.api;

import com.globalcapitalflow.service.GlobalCapitalFlowDataService;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

/**
 * 全球资金流向数据API服务器
 * 监控全球主要市场的资金流向趋势，包括美股、欧股、亚太等市场
 */
public class GlobalCapitalFlowApiServer {
    
    public static void main(String[] args) throws Exception {
        System.out.println("========================================");
        System.out.println("全球资金流向监控服务器启动中...");
        System.out.println("覆盖: 美股、欧股、亚太、新兴市场");
        System.out.println("实时监控全球资金流向趋势");
        System.out.println("Java版本: " + System.getProperty("java.version"));
        System.out.println("========================================");
        
        // 启动数据拉取服务
        System.out.println("启动全球资金流向数据拉取服务...");
        GlobalCapitalFlowDataService.initialize();
        
        HttpServer server = HttpServer.create(new InetSocketAddress(5002), 0);
        
        // 主页
        server.createContext("/", new HomeHandler());
        // 全球资金流向管理页面
        server.createContext("/global-capital-flow", new PageHandler("resources/templates/global-capital-flow.html"));
        // 市场对比分析页面
        server.createContext("/market-comparison", new PageHandler("resources/templates/market-comparison.html"));
        
        // API端点
        server.createContext("/api/global-capital-flow", new GlobalCapitalFlowHandler());
        server.createContext("/api/global-capital-flow/stats", new GlobalCapitalFlowStatsHandler());
        server.createContext("/api/global-capital-flow/refresh", new RefreshDataHandler());
        server.createContext("/api/market-regions", new MarketRegionsHandler());
        server.createContext("/api/regional-flow/trend", new RegionalFlowTrendHandler());
        server.createContext("/api/currency-flow/stats", new CurrencyFlowStatsHandler());
        
        server.setExecutor(null);
        server.start();
        
        System.out.println("✅ 全球资金流向API服务器启动成功！");
        System.out.println("访问地址: http://localhost:5002");
        System.out.println("全球资金流向: http://localhost:5002/global-capital-flow");
        System.out.println("市场对比分析: http://localhost:5002/market-comparison");
        System.out.println("实时API测试: http://localhost:5002/api/global-capital-flow");
        System.out.println("数据统计: http://localhost:5002/api/global-capital-flow/stats");
        System.out.println("========================================");
        
        // 显示当前数据统计
        Map<String, Object> stats = GlobalCapitalFlowDataService.getDataStatistics();
        System.out.println("📊 当前数据统计:");
        System.out.println("   监控市场数: " + stats.get("total_markets"));
        System.out.println("   美股资金流向: " + stats.get("us_market_flow"));
        System.out.println("   欧股资金流向: " + stats.get("europe_market_flow"));
        System.out.println("   亚太资金流向: " + stats.get("asia_market_flow"));
        System.out.println("   最后更新: " + stats.get("last_update"));
    }
    
    static class HomeHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            Map<String, Object> stats = GlobalCapitalFlowDataService.getDataStatistics();
            
            String response = String.format("""
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>全球资金流向监控平台 - 盛行趋势科技</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">
                <style>
                    .sidebar {
                        min-height: 100vh;
                        background: linear-gradient(180deg, #2d5016 0%%, #4a7c59 100%%);
                        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
                    }
                    .sidebar .nav-link {
                        color: rgba(255,255,255,0.8);
                        padding: 12px 20px;
                        margin: 2px 0;
                        border-radius: 8px;
                        transition: all 0.3s ease;
                    }
                    .sidebar .nav-link:hover {
                        background-color: rgba(255,255,255,0.1);
                        color: white;
                        transform: translateX(5px);
                    }
                    .sidebar .nav-link.active {
                        background-color: rgba(255,255,255,0.2);
                        color: white;
                        font-weight: 600;
                    }
                    .company-logo {
                        background: rgba(255,255,255,0.1);
                        border-radius: 15px;
                        padding: 20px;
                        margin-bottom: 30px;
                        text-align: center;
                        border: 2px solid rgba(255,255,255,0.2);
                    }
                    .main-content {
                        background: #f8f9fa;
                        min-height: 100vh;
                    }
                    .header-banner {
                        background: linear-gradient(135deg, #2d5016 0%%, #4a7c59 100%%);
                        color: white;
                        padding: 30px 0;
                        margin-bottom: 30px;
                        border-radius: 0 0 20px 20px;
                    }
                    .stats-card {
                        background: white;
                        border-radius: 15px;
                        padding: 25px;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                        border: none;
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                        height: 100%%;
                    }
                    .stats-card:hover {
                        transform: translateY(-5px);
                        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
                    }
                    .feature-card {
                        background: white;
                        border-radius: 15px;
                        padding: 30px;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                        border: none;
                        text-align: center;
                        transition: all 0.3s ease;
                        height: 100%%;
                    }
                    .feature-card:hover {
                        transform: translateY(-5px);
                        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
                    }
                    .feature-icon {
                        font-size: 3rem;
                        margin-bottom: 20px;
                        background: linear-gradient(45deg, #2d5016, #4a7c59);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                    }
                    .status-indicator {
                        display: inline-block;
                        width: 12px;
                        height: 12px;
                        background: #28a745;
                        border-radius: 50%%;
                        margin-right: 8px;
                        animation: pulse 2s infinite;
                    }
                    @keyframes pulse {
                        0%% { opacity: 1; }
                        50%% { opacity: 0.5; }
                        100%% { opacity: 1; }
                    }
                    .refresh-btn {
                        background: linear-gradient(45deg, #28a745, #20c997);
                        border: none;
                        border-radius: 25px;
                        padding: 12px 30px;
                        font-weight: 600;
                        transition: all 0.3s ease;
                    }
                    .refresh-btn:hover {
                        transform: scale(1.05);
                        box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3);
                    }
                </style>
            </head>
            <body>
                <div class="container-fluid">
                    <div class="row">
                        <!-- 左侧导航栏 -->
                        <div class="col-lg-3 col-md-4 sidebar p-0">
                            <div class="p-4">
                                <!-- 公司Logo和信息 -->
                                <div class="company-logo">
                                    <h4 class="text-white mb-2">
                                        <i class="bi bi-globe-americas"></i> 盛行趋势科技
                                    </h4>
                                    <p class="text-white-50 mb-0 small">PrevailingTrend Technology</p>
                                    <p class="text-white-50 mb-0 small">全球资金流向监控平台</p>
                                </div>
                                
                                <!-- 导航菜单 -->
                                <nav class="nav flex-column">
                                    <a class="nav-link active" href="/">
                                        <i class="bi bi-house-door me-2"></i> 监控中心首页
                                    </a>
                                    <a class="nav-link" href="/global-capital-flow">
                                        <i class="bi bi-graph-up-arrow me-2"></i> 全球资金流向
                                    </a>
                                    <a class="nav-link" href="/market-comparison">
                                        <i class="bi bi-bar-chart-line me-2"></i> 市场对比分析
                                    </a>
                                    
                                    <hr class="text-white-50 my-3">
                                    
                                    <h6 class="text-white-50 small text-uppercase mb-3">API服务</h6>
                                    <a class="nav-link" href="/api/global-capital-flow">
                                        <i class="bi bi-database me-2"></i> 资金流向API
                                    </a>
                                    <a class="nav-link" href="/api/global-capital-flow/stats">
                                        <i class="bi bi-bar-chart me-2"></i> 统计数据API
                                    </a>
                                    <a class="nav-link" href="/api/market-regions">
                                        <i class="bi bi-geo me-2"></i> 市场区域API
                                    </a>
                                    
                                    <hr class="text-white-50 my-3">
                                    
                                    <h6 class="text-white-50 small text-uppercase mb-3">系统信息</h6>
                                    <div class="text-white-50 small">
                                        <p class="mb-1"><i class="bi bi-server me-2"></i> 服务端口: 5002</p>
                                        <p class="mb-1"><i class="bi bi-clock me-2"></i> 运行时间: 24/7</p>
                                        <p class="mb-1"><i class="bi bi-shield-check me-2"></i> 安全状态: 正常</p>
                                    </div>
                                </nav>
                            </div>
                        </div>
                        
                        <!-- 主要内容区域 -->
                        <div class="col-lg-9 col-md-8 main-content p-0">
                            <!-- 顶部横幅 -->
                            <div class="header-banner">
                                <div class="container-fluid px-4">
                                    <div class="row align-items-center">
                                        <div class="col-md-8">
                                            <h2 class="mb-1">
                                                <span class="status-indicator"></span>
                                                全球资金流向监控平台
                                            </h2>
                                            <p class="mb-0 opacity-75">实时监控全球主要市场 | 美股·欧股·亚太·新兴市场 | 智能分析·实时预警</p>
                                        </div>
                                        <div class="col-md-4 text-end">
                                            <button onclick="refreshData()" class="btn refresh-btn text-white">
                                                <i class="bi bi-arrow-clockwise me-2"></i> 刷新数据
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="container-fluid px-4">
                                <!-- 统计数据卡片 -->
                                <div class="row mb-4">
                                    <div class="col-xl-3 col-md-6 mb-3">
                                        <div class="stats-card text-center">
                                            <h3 class="text-primary mb-1">%s</h3>
                                            <p class="text-muted small mb-0">监控市场数</p>
                                        </div>
                                    </div>
                                    <div class="col-xl-3 col-md-6 mb-3">
                                        <div class="stats-card text-center">
                                            <h3 class="text-success mb-1">%s</h3>
                                            <p class="text-muted small mb-0">美股流向</p>
                                        </div>
                                    </div>
                                    <div class="col-xl-3 col-md-6 mb-3">
                                        <div class="stats-card text-center">
                                            <h3 class="text-info mb-1">%s</h3>
                                            <p class="text-muted small mb-0">欧股流向</p>
                                        </div>
                                    </div>
                                    <div class="col-xl-3 col-md-6 mb-3">
                                        <div class="stats-card text-center">
                                            <h3 class="text-warning mb-1">%s</h3>
                                            <p class="text-muted small mb-0">亚太流向</p>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- 功能模块 -->
                                <div class="row mb-4">
                                    <div class="col-lg-6 col-md-12 mb-4">
                                        <div class="feature-card">
                                            <div class="feature-icon">
                                                <i class="bi bi-globe-americas"></i>
                                            </div>
                                            <h5 class="mb-3">全球资金流向监控</h5>
                                            <p class="text-muted mb-3">实时监控全球主要市场的资金流向，包括美股、欧股、亚太等区域，提供详细的流向分析和趋势预测</p>
                                            <a href="/global-capital-flow" class="btn btn-primary">进入监控 <i class="bi bi-arrow-right"></i></a>
                                        </div>
                                    </div>
                                    <div class="col-lg-6 col-md-12 mb-4">
                                        <div class="feature-card">
                                            <div class="feature-icon">
                                                <i class="bi bi-bar-chart-line"></i>
                                            </div>
                                            <h5 class="mb-3">市场对比分析</h5>
                                            <p class="text-muted mb-3">提供多市场横向对比分析，帮助投资者了解不同区域市场的资金配置偏好和投资机会</p>
                                            <a href="/market-comparison" class="btn btn-info">查看分析 <i class="bi bi-arrow-right"></i></a>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- 底部信息 -->
                                <div class="row mt-4 mb-4">
                                    <div class="col-12">
                                        <div class="text-center text-muted small">
                                            <p class="mb-1">© 2025 盛行趋势科技 (PrevailingTrend Technology) - 全球资金流向监控平台</p>
                                            <p class="mb-0">数据来源: Bloomberg、Reuters等 | 更新频率: 每5分钟 | 技术支持: Java 17 + HTTP服务器</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
                <script>
                function refreshData() {
                    const btn = event.target;
                    const originalHtml = btn.innerHTML;
                    btn.innerHTML = '<i class="bi bi-arrow-clockwise spin me-2"></i> 刷新中...';
                    btn.disabled = true;
                    
                    fetch('/api/global-capital-flow/refresh', {method: 'POST'})
                        .then(response => response.json())
                        .then(data => {
                            if(data.success) {
                                btn.innerHTML = '<i class="bi bi-check-circle me-2"></i> 刷新成功!';
                                btn.className = 'btn btn-success text-white';
                                setTimeout(() => {
                                    location.reload();
                                }, 2000);
                            } else {
                                btn.innerHTML = '<i class="bi bi-x-circle me-2"></i> 刷新失败';
                                btn.className = 'btn btn-danger text-white';
                            }
                        })
                        .catch(error => {
                            btn.innerHTML = '<i class="bi bi-x-circle me-2"></i> 网络错误';
                            btn.className = 'btn btn-danger text-white';
                        })
                        .finally(() => {
                            setTimeout(() => {
                                btn.innerHTML = originalHtml;
                                btn.className = 'btn refresh-btn text-white';
                                btn.disabled = false;
                            }, 3000);
                        });
                }
                </script>
            </body>
            </html>
            """, 
            stats.get("total_markets"), stats.get("us_market_flow"), 
            stats.get("europe_market_flow"), stats.get("asia_market_flow"));
            
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
    
    static class GlobalCapitalFlowHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                List<Map<String, Object>> flowData = GlobalCapitalFlowDataService.getGlobalFlowData();
                
                StringBuilder jsonBuilder = new StringBuilder();
                jsonBuilder.append("{\"success\": true, \"data\": [");
                
                for (int i = 0; i < flowData.size(); i++) {
                    if (i > 0) jsonBuilder.append(",");
                    Map<String, Object> flow = flowData.get(i);
                    jsonBuilder.append("{");
                    jsonBuilder.append("\"region\": \"").append(flow.get("region")).append("\",");
                    jsonBuilder.append("\"market\": \"").append(flow.get("market")).append("\",");
                    jsonBuilder.append("\"inflow\": ").append(flow.get("inflow")).append(",");
                    jsonBuilder.append("\"outflow\": ").append(flow.get("outflow")).append(",");
                    jsonBuilder.append("\"netFlow\": ").append(flow.get("netFlow")).append(",");
                    jsonBuilder.append("\"currency\": \"").append(flow.get("currency")).append("\",");
                    jsonBuilder.append("\"lastUpdated\": \"").append(flow.get("lastUpdated")).append("\"");
                    jsonBuilder.append("}");
                }
                
                jsonBuilder.append("]}");
                sendResponse(exchange, 200, jsonBuilder.toString(), "application/json");
                
            } catch (Exception e) {
                String errorResponse = "{\"success\": false, \"error\": \"" + e.getMessage() + "\"}";
                sendResponse(exchange, 500, errorResponse, "application/json");
            }
        }
    }
    
    static class GlobalCapitalFlowStatsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                Map<String, Object> stats = GlobalCapitalFlowDataService.getDataStatistics();
                
                StringBuilder jsonBuilder = new StringBuilder();
                jsonBuilder.append("{\"success\": true, \"data\": ");
                jsonBuilder.append("{");
                jsonBuilder.append("\"total_markets\": ").append(stats.get("total_markets")).append(",");
                jsonBuilder.append("\"us_market_flow\": \"").append(stats.get("us_market_flow")).append("\",");
                jsonBuilder.append("\"europe_market_flow\": \"").append(stats.get("europe_market_flow")).append("\",");
                jsonBuilder.append("\"asia_market_flow\": \"").append(stats.get("asia_market_flow")).append("\",");
                jsonBuilder.append("\"last_update\": \"").append(stats.get("last_update")).append("\"");
                jsonBuilder.append("}}");
                
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
                    GlobalCapitalFlowDataService.refreshData();
                    String response = "{\"success\": true, \"message\": \"全球资金流向数据刷新成功\"}";
                    sendResponse(exchange, 200, response, "application/json");
                } else {
                    Map<String, Object> stats = GlobalCapitalFlowDataService.getDataStatistics();
                    String response = "{\"success\": true, \"last_update\": \"" + stats.get("last_update") + "\"}";
                    sendResponse(exchange, 200, response, "application/json");
                }
            } catch (Exception e) {
                String errorResponse = "{\"success\": false, \"error\": \"" + e.getMessage() + "\"}";
                sendResponse(exchange, 500, errorResponse, "application/json");
            }
        }
    }
    
    static class MarketRegionsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
            {
                "success": true,
                "data": [
                    {"regionCode": "US", "regionName": "美股市场", "currency": "USD"},
                    {"regionCode": "EU", "regionName": "欧洲市场", "currency": "EUR"},
                    {"regionCode": "ASIA", "regionName": "亚太市场", "currency": "JPY"},
                    {"regionCode": "EMERGING", "regionName": "新兴市场", "currency": "CNY"}
                ]
            }
            """;
            sendResponse(exchange, 200, response, "application/json");
        }
    }
    
    static class RegionalFlowTrendHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
            {
                "success": true,
                "data": [
                    {"date": "2025-09-07", "us_flow": 125800, "europe_flow": -45600, "asia_flow": 89200},
                    {"date": "2025-09-08", "us_flow": -89600, "europe_flow": 67500, "asia_flow": -23100},
                    {"date": "2025-09-09", "us_flow": 254000, "europe_flow": 125600, "asia_flow": 156300},
                    {"date": "2025-09-10", "us_flow": 182000, "europe_flow": -76400, "asia_flow": 198400},
                    {"date": "2025-09-11", "us_flow": 321000, "europe_flow": 189000, "asia_flow": -87000}
                ]
            }
            """;
            sendResponse(exchange, 200, response, "application/json");
        }
    }
    
    static class CurrencyFlowStatsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
            {
                "success": true,
                "data": {
                    "usd_flow": 2580000,
                    "eur_flow": -890000,
                    "jpy_flow": 1450000,
                    "cny_flow": 760000,
                    "total_global_flow": 3900000
                }
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