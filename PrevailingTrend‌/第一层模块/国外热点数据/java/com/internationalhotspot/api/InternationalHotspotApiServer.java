package com.internationalhotspot.api;

import com.internationalhotspot.service.InternationalHotspotDataService;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

/**
 * 国外热点数据API服务器
 * 监控国外财经热点、国际政策、全球市场等信息
 */
public class InternationalHotspotApiServer {
    
    public static void main(String[] args) throws Exception {
        System.out.println("========================================");
        System.out.println("国外热点数据监控服务器启动中...");
        System.out.println("覆盖: 国际财经、政策动态、全球市场");
        System.out.println("实时监控国际热点趋势");
        System.out.println("Java版本: " + System.getProperty("java.version"));
        System.out.println("========================================");
        
        // 启动数据拉取服务
        System.out.println("启动国外热点数据拉取服务...");
        InternationalHotspotDataService.initialize();
        
        HttpServer server = HttpServer.create(new InetSocketAddress(5004), 0);
        
        // 主页
        server.createContext("/", new HomeHandler());
        // 国际热点数据管理页面
        server.createContext("/international-hotspot", new PageHandler("resources/templates/international-hotspot.html"));
        // 全球市场分析页面
        server.createContext("/global-analysis", new PageHandler("resources/templates/global-analysis.html"));
        
        // API端点
        server.createContext("/api/international-hotspot", new InternationalHotspotHandler());
        server.createContext("/api/international-hotspot/stats", new InternationalHotspotStatsHandler());
        server.createContext("/api/international-hotspot/refresh", new RefreshDataHandler());
        server.createContext("/api/global-regions", new GlobalRegionsHandler());
        server.createContext("/api/international-sentiment", new InternationalSentimentHandler());
        server.createContext("/api/geopolitical-events", new GeopoliticalEventsHandler());
        
        server.setExecutor(null);
        server.start();
        
        System.out.println("✅ 国外热点数据API服务器启动成功！");
        System.out.println("访问地址: http://localhost:5004");
        System.out.println("国际热点数据: http://localhost:5004/international-hotspot");
        System.out.println("全球市场分析: http://localhost:5004/global-analysis");
        System.out.println("实时API测试: http://localhost:5004/api/international-hotspot");
        System.out.println("数据统计: http://localhost:5004/api/international-hotspot/stats");
        System.out.println("========================================");
        
        // 显示当前数据统计
        Map<String, Object> stats = InternationalHotspotDataService.getDataStatistics();
        System.out.println("📊 当前数据统计:");
        System.out.println("   国际热点数: " + stats.get("total_international_hotspots"));
        System.out.println("   美国新闻: " + stats.get("us_news_count"));
        System.out.println("   欧洲新闻: " + stats.get("europe_news_count"));
        System.out.println("   亚洲新闻: " + stats.get("asia_news_count"));
        System.out.println("   全球情绪: " + stats.get("global_sentiment"));
        System.out.println("   最后更新: " + stats.get("last_update"));
    }
    
    static class HomeHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            Map<String, Object> stats = InternationalHotspotDataService.getDataStatistics();
            
            String response = String.format("""
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>国外热点数据监控平台 - 盛行趋势科技</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">
                <style>
                    .sidebar {
                        min-height: 100vh;
                        background: linear-gradient(180deg, #2F4F4F 0%%, #708090 100%%);
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
                        background: linear-gradient(135deg, #2F4F4F 0%%, #708090 100%%);
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
                        background: linear-gradient(45deg, #2F4F4F, #708090);
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
                                        <i class="bi bi-globe"></i> 盛行趋势科技
                                    </h4>
                                    <p class="text-white-50 mb-0 small">PrevailingTrend Technology</p>
                                    <p class="text-white-50 mb-0 small">国外热点数据监控平台</p>
                                </div>
                                
                                <!-- 导航菜单 -->
                                <nav class="nav flex-column">
                                    <a class="nav-link active" href="/">
                                        <i class="bi bi-house-door me-2"></i> 国际监控首页
                                    </a>
                                    <a class="nav-link" href="/international-hotspot">
                                        <i class="bi bi-globe-central-south-asia me-2"></i> 国际热点数据
                                    </a>
                                    <a class="nav-link" href="/global-analysis">
                                        <i class="bi bi-graph-up me-2"></i> 全球市场分析
                                    </a>
                                    
                                    <hr class="text-white-50 my-3">
                                    
                                    <h6 class="text-white-50 small text-uppercase mb-3">API服务</h6>
                                    <a class="nav-link" href="/api/international-hotspot">
                                        <i class="bi bi-database me-2"></i> 国际热点API
                                    </a>
                                    <a class="nav-link" href="/api/international-hotspot/stats">
                                        <i class="bi bi-bar-chart me-2"></i> 统计数据API
                                    </a>
                                    <a class="nav-link" href="/api/global-regions">
                                        <i class="bi bi-geo me-2"></i> 全球区域API
                                    </a>
                                    
                                    <hr class="text-white-50 my-3">
                                    
                                    <h6 class="text-white-50 small text-uppercase mb-3">系统信息</h6>
                                    <div class="text-white-50 small">
                                        <p class="mb-1"><i class="bi bi-server me-2"></i> 服务端口: 5004</p>
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
                                                国外热点数据监控平台
                                            </h2>
                                            <p class="mb-0 opacity-75">实时监控国际热点资讯 | 美国·欧洲·亚洲·全球市场 | 智能分析·情报收集</p>
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
                                            <p class="text-muted small mb-0">国际热点总数</p>
                                        </div>
                                    </div>
                                    <div class="col-xl-3 col-md-6 mb-3">
                                        <div class="stats-card text-center">
                                            <h3 class="text-success mb-1">%s</h3>
                                            <p class="text-muted small mb-0">美国新闻</p>
                                        </div>
                                    </div>
                                    <div class="col-xl-3 col-md-6 mb-3">
                                        <div class="stats-card text-center">
                                            <h3 class="text-info mb-1">%s</h3>
                                            <p class="text-muted small mb-0">欧洲新闻</p>
                                        </div>
                                    </div>
                                    <div class="col-xl-3 col-md-6 mb-3">
                                        <div class="stats-card text-center">
                                            <h3 class="text-warning mb-1">%s</h3>
                                            <p class="text-muted small mb-0">亚洲新闻</p>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- 功能模块 -->
                                <div class="row mb-4">
                                    <div class="col-lg-6 col-md-12 mb-4">
                                        <div class="feature-card">
                                            <div class="feature-icon">
                                                <i class="bi bi-globe"></i>
                                            </div>
                                            <h5 class="mb-3">国际热点数据管理</h5>
                                            <p class="text-muted mb-3">实时监控和管理国际财经热点、地缘政治事件、全球市场动态，提供全球视野的信息服务</p>
                                            <a href="/international-hotspot" class="btn btn-primary">进入管理 <i class="bi bi-arrow-right"></i></a>
                                        </div>
                                    </div>
                                    <div class="col-lg-6 col-md-12 mb-4">
                                        <div class="feature-card">
                                            <div class="feature-icon">
                                                <i class="bi bi-graph-up"></i>
                                            </div>
                                            <h5 class="mb-3">全球市场分析</h5>
                                            <p class="text-muted mb-3">深度分析全球市场趋势、国际政策影响和跨国资本流动，为全球投资提供决策支持</p>
                                            <a href="/global-analysis" class="btn btn-info">查看分析 <i class="bi bi-arrow-right"></i></a>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- 底部信息 -->
                                <div class="row mt-4 mb-4">
                                    <div class="col-12">
                                        <div class="text-center text-muted small">
                                            <p class="mb-1">© 2025 盛行趋势科技 (PrevailingTrend Technology) - 国外热点数据监控平台</p>
                                            <p class="mb-0">数据来源: Reuters、Bloomberg、AP等 | 更新频率: 每5分钟 | 技术支持: Java 17 + HTTP服务器</p>
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
                    
                    fetch('/api/international-hotspot/refresh', {method: 'POST'})
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
            stats.get("total_international_hotspots"), stats.get("us_news_count"), 
            stats.get("europe_news_count"), stats.get("asia_news_count"));
            
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
    
    static class InternationalHotspotHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                List<Map<String, Object>> hotspotData = InternationalHotspotDataService.getInternationalHotspotData();
                
                StringBuilder jsonBuilder = new StringBuilder();
                jsonBuilder.append("{\"success\": true, \"data\": [");
                
                for (int i = 0; i < hotspotData.size(); i++) {
                    if (i > 0) jsonBuilder.append(",");
                    Map<String, Object> hotspot = hotspotData.get(i);
                    jsonBuilder.append("{");
                    jsonBuilder.append("\"id\": \"").append(hotspot.get("id")).append("\",");
                    jsonBuilder.append("\"title\": \"").append(hotspot.get("title")).append("\",");
                    jsonBuilder.append("\"region\": \"").append(hotspot.get("region")).append("\",");
                    jsonBuilder.append("\"category\": \"").append(hotspot.get("category")).append("\",");
                    jsonBuilder.append("\"content\": \"").append(hotspot.get("content")).append("\",");
                    jsonBuilder.append("\"impactScore\": ").append(hotspot.get("impactScore")).append(",");
                    jsonBuilder.append("\"sentiment\": \"").append(hotspot.get("sentiment")).append("\",");
                    jsonBuilder.append("\"source\": \"").append(hotspot.get("source")).append("\",");
                    jsonBuilder.append("\"publishTime\": \"").append(hotspot.get("publishTime")).append("\"");
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
    
    static class InternationalHotspotStatsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                Map<String, Object> stats = InternationalHotspotDataService.getDataStatistics();
                
                StringBuilder jsonBuilder = new StringBuilder();
                jsonBuilder.append("{\"success\": true, \"data\": ");
                jsonBuilder.append("{");
                jsonBuilder.append("\"total_international_hotspots\": ").append(stats.get("total_international_hotspots")).append(",");
                jsonBuilder.append("\"us_news_count\": ").append(stats.get("us_news_count")).append(",");
                jsonBuilder.append("\"europe_news_count\": ").append(stats.get("europe_news_count")).append(",");
                jsonBuilder.append("\"asia_news_count\": ").append(stats.get("asia_news_count")).append(",");
                jsonBuilder.append("\"global_sentiment\": \"").append(stats.get("global_sentiment")).append("\",");
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
                    InternationalHotspotDataService.refreshData();
                    String response = "{\"success\": true, \"message\": \"国外热点数据刷新成功\"}";
                    sendResponse(exchange, 200, response, "application/json");
                } else {
                    Map<String, Object> stats = InternationalHotspotDataService.getDataStatistics();
                    String response = "{\"success\": true, \"last_update\": \"" + stats.get("last_update") + "\"}";
                    sendResponse(exchange, 200, response, "application/json");
                }
            } catch (Exception e) {
                String errorResponse = "{\"success\": false, \"error\": \"" + e.getMessage() + "\"}";
                sendResponse(exchange, 500, errorResponse, "application/json");
            }
        }
    }
    
    static class GlobalRegionsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
            {
                "success": true,
                "data": [
                    {"regionCode": "NORTH_AMERICA", "regionName": "北美地区", "countries": ["美国", "加拿大"]},
                    {"regionCode": "EUROPE", "regionName": "欧洲地区", "countries": ["英国", "德国", "法国"]},
                    {"regionCode": "ASIA_PACIFIC", "regionName": "亚太地区", "countries": ["日本", "韩国", "澳大利亚"]},
                    {"regionCode": "EMERGING", "regionName": "新兴市场", "countries": ["印度", "巴西", "俄罗斯"]}
                ]
            }
            """;
            sendResponse(exchange, 200, response, "application/json");
        }
    }
    
    static class InternationalSentimentHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
            {
                "success": true,
                "data": {
                    "global_sentiment": "中性偏积极",
                    "regional_sentiment": {
                        "north_america": "积极",
                        "europe": "中性",
                        "asia_pacific": "积极",
                        "emerging_markets": "消极"
                    },
                    "sentiment_score": 6.8
                }
            }
            """;
            sendResponse(exchange, 200, response, "application/json");
        }
    }
    
    static class GeopoliticalEventsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = """
            {
                "success": true,
                "data": [
                    {"date": "2025-09-07", "event": "美联储政策会议", "impact_level": "高", "region": "北美"},
                    {"date": "2025-09-08", "event": "欧盟贸易政策调整", "impact_level": "中", "region": "欧洲"},
                    {"date": "2025-09-09", "event": "亚太经济合作", "impact_level": "中", "region": "亚太"},
                    {"date": "2025-09-10", "event": "G20峰会准备", "impact_level": "高", "region": "全球"},
                    {"date": "2025-09-11", "event": "国际贸易谈判", "impact_level": "中", "region": "全球"}
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