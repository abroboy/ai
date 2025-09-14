package com.windindustry.api;

import com.windindustry.service.StockDataFetcher;
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
        // 股票映射页面（统一版本，支持排序）
        server.createContext("/stock-mappings", new PageHandler("resources/templates/stock-mappings.html"));
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
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>万得行业分类智能数据平台 - 盛行趋势科技</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">
                <style>
                    .sidebar {
                        min-height: 100vh;
                        background: linear-gradient(180deg, #1e3c72 0%%, #2a5298 100%%);
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
                        background: linear-gradient(135deg, #667eea 0%%, #764ba2 100%%);
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
                        background: linear-gradient(45deg, #667eea, #764ba2);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                    }
                    .api-list {
                        background: white;
                        border-radius: 15px;
                        padding: 25px;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                    }
                    .api-item {
                        padding: 12px 15px;
                        margin: 5px 0;
                        background: #f8f9fa;
                        border-radius: 8px;
                        border-left: 4px solid #667eea;
                        transition: all 0.3s ease;
                    }
                    .api-item:hover {
                        background: #e9ecef;
                        transform: translateX(5px);
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
                                        <i class="bi bi-graph-up-arrow"></i> 盛行趋势科技
                                    </h4>
                                    <p class="text-white-50 mb-0 small">PrevailingTrend Technology</p>
                                    <p class="text-white-50 mb-0 small">智能金融数据服务平台</p>
                                </div>
                                
                                <!-- 导航菜单 -->
                                <nav class="nav flex-column">
                                    <a class="nav-link active" href="/">
                                        <i class="bi bi-house-door me-2"></i> 数据中心首页
                                    </a>
                                    <a class="nav-link" href="/stock-mappings">
                                        <i class="bi bi-table me-2"></i> 股票映射管理
                                    </a>
                                    <a class="nav-link" href="/data-analysis">
                                        <i class="bi bi-graph-up me-2"></i> 数据分析面板
                                    </a>
                                    <a class="nav-link" href="/功能测试页面.html">
                                        <i class="bi bi-gear me-2"></i> 功能测试中心
                                    </a>
                                    
                                    <hr class="text-white-50 my-3">
                                    
                                    <h6 class="text-white-50 small text-uppercase mb-3">API服务</h6>
                                    <a class="nav-link" href="/api/stock-mappings">
                                        <i class="bi bi-database me-2"></i> 股票数据API
                                    </a>
                                    <a class="nav-link" href="/api/stock-mappings/stats">
                                        <i class="bi bi-bar-chart me-2"></i> 统计数据API
                                    </a>
                                    <a class="nav-link" href="/api/wind-industries">
                                        <i class="bi bi-collection me-2"></i> 行业分类API
                                    </a>
                                    
                                    <hr class="text-white-50 my-3">
                                    
                                    <h6 class="text-white-50 small text-uppercase mb-3">系统信息</h6>
                                    <div class="text-white-50 small">
                                        <p class="mb-1"><i class="bi bi-server me-2"></i> 服务端口: 5001</p>
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
                                                万得行业分类智能数据平台
                                            </h2>
                                            <p class="mb-0 opacity-75">实时监控5000+只股票 | A股·科创板·创业板·港股通 | 智能分析·实时更新</p>
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
                                    <div class="col-xl-2 col-md-4 col-sm-6 mb-3">
                                        <div class="stats-card text-center">
                                            <h3 class="text-primary mb-1">%s</h3>
                                            <p class="text-muted small mb-0">总股票数</p>
                                        </div>
                                    </div>
                                    <div class="col-xl-2 col-md-4 col-sm-6 mb-3">
                                        <div class="stats-card text-center">
                                            <h3 class="text-success mb-1">%s</h3>
                                            <p class="text-muted small mb-0">A股</p>
                                        </div>
                                    </div>
                                    <div class="col-xl-2 col-md-4 col-sm-6 mb-3">
                                        <div class="stats-card text-center">
                                            <h3 class="text-info mb-1">%s</h3>
                                            <p class="text-muted small mb-0">科创板</p>
                                        </div>
                                    </div>
                                    <div class="col-xl-2 col-md-4 col-sm-6 mb-3">
                                        <div class="stats-card text-center">
                                            <h3 class="text-warning mb-1">%s</h3>
                                            <p class="text-muted small mb-0">创业板</p>
                                        </div>
                                    </div>
                                    <div class="col-xl-2 col-md-4 col-sm-6 mb-3">
                                        <div class="stats-card text-center">
                                            <h3 class="text-danger mb-1">%s</h3>
                                            <p class="text-muted small mb-0">港股通</p>
                                        </div>
                                    </div>
                                    <div class="col-xl-2 col-md-4 col-sm-6 mb-3">
                                        <div class="stats-card text-center">
                                            <small class="text-muted">最后更新</small>
                                            <p class="mb-0 small">%s</p>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- 功能模块 -->
                                <div class="row mb-4">
                                    <div class="col-lg-4 col-md-6 mb-4">
                                        <div class="feature-card">
                                            <div class="feature-icon">
                                                <i class="bi bi-table"></i>
                                            </div>
                                            <h5 class="mb-3">股票映射管理</h5>
                                            <p class="text-muted mb-3">实时管理5000+只股票与万得行业分类的映射关系，支持排序、筛选、分页等高级功能</p>
                                            <a href="/stock-mappings" class="btn btn-primary">进入管理 <i class="bi bi-arrow-right"></i></a>
                                        </div>
                                    </div>
                                    <div class="col-lg-4 col-md-6 mb-4">
                                        <div class="feature-card">
                                            <div class="feature-icon">
                                                <i class="bi bi-graph-up"></i>
                                            </div>
                                            <h5 class="mb-3">数据分析面板</h5>
                                            <p class="text-muted mb-3">智能分析股票资金流向、行业分布、市场趋势等多维度数据，提供专业投资决策支持</p>
                                            <a href="/data-analysis" class="btn btn-info">查看分析 <i class="bi bi-arrow-right"></i></a>
                                        </div>
                                    </div>
                                    <div class="col-lg-4 col-md-6 mb-4">
                                        <div class="feature-card">
                                            <div class="feature-icon">
                                                <i class="bi bi-gear"></i>
                                            </div>
                                            <h5 class="mb-3">系统测试中心</h5>
                                            <p class="text-muted mb-3">全面的功能测试页面，验证API接口、数据拉取、系统性能等各项指标</p>
                                            <a href="/功能测试页面.html" class="btn btn-success">功能测试 <i class="bi bi-arrow-right"></i></a>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- API接口列表 -->
                                <div class="row">
                                    <div class="col-12">
                                        <div class="api-list">
                                            <h5 class="mb-4">
                                                <i class="bi bi-cloud-arrow-down text-primary me-2"></i>
                                                API服务接口
                                            </h5>
                                            <div class="row">
                                                <div class="col-md-6">
                                                    <div class="api-item">
                                                        <a href="/api/stock-mappings" class="text-decoration-none">
                                                            <strong>/api/stock-mappings</strong>
                                                            <br><small class="text-muted">实时股票数据接口</small>
                                                        </a>
                                                    </div>
                                                    <div class="api-item">
                                                        <a href="/api/stock-mappings/stats" class="text-decoration-none">
                                                            <strong>/api/stock-mappings/stats</strong>
                                                            <br><small class="text-muted">数据统计分析接口</small>
                                                        </a>
                                                    </div>
                                                    <div class="api-item">
                                                        <a href="/api/wind-industries" class="text-decoration-none">
                                                            <strong>/api/wind-industries</strong>
                                                            <br><small class="text-muted">万得行业分类接口</small>
                                                        </a>
                                                    </div>
                                                </div>
                                                <div class="col-md-6">
                                                    <div class="api-item">
                                                        <a href="/api/market/distribution" class="text-decoration-none">
                                                            <strong>/api/market/distribution</strong>
                                                            <br><small class="text-muted">市场分布数据接口</small>
                                                        </a>
                                                    </div>
                                                    <div class="api-item">
                                                        <a href="/api/industry/distribution" class="text-decoration-none">
                                                            <strong>/api/industry/distribution</strong>
                                                            <br><small class="text-muted">行业分布统计接口</small>
                                                        </a>
                                                    </div>
                                                    <div class="api-item">
                                                        <a href="/api/capital-flow/trend" class="text-decoration-none">
                                                            <strong>/api/capital-flow/trend</strong>
                                                            <br><small class="text-muted">资金流向趋势接口</small>
                                                        </a>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- 底部信息 -->
                                <div class="row mt-4 mb-4">
                                    <div class="col-12">
                                        <div class="text-center text-muted small">
                                            <p class="mb-1">© 2025 盛行趋势科技 (PrevailingTrend Technology) - 万得行业分类智能数据平台</p>
                                            <p class="mb-0">数据来源: 东方财富、Yahoo Finance等 | 更新频率: 每5分钟 | 技术支持: Java 17 + HTTP服务器</p>
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
                    
                    fetch('/api/stock-mappings/refresh', {method: 'POST'})
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
                                console.error('刷新失败:', data.error);
                            }
                        })
                        .catch(error => {
                            btn.innerHTML = '<i class="bi bi-x-circle me-2"></i> 网络错误';
                            btn.className = 'btn btn-danger text-white';
                            console.error('网络错误:', error);
                        })
                        .finally(() => {
                            setTimeout(() => {
                                btn.innerHTML = originalHtml;
                                btn.className = 'btn refresh-btn text-white';
                                btn.disabled = false;
                            }, 3000);
                        });
                }
                
                // 添加动态样式
                const style = document.createElement('style');
                style.textContent = `
                    .spin {
                        animation: spin 1s linear infinite;
                    }
                    @keyframes spin {
                        from { transform: rotate(0deg); }
                        to { transform: rotate(360deg); }
                    }
                `;
                document.head.appendChild(style);
                </script>
            </body>
            </html>
            """, 
            stats.get("total_stocks"), stats.get("a_stock_count"), stats.get("kc_stock_count"),
            stats.get("gem_stock_count"), stats.get("hk_stock_count"), stats.get("last_update"));
            
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
                comparator = (a, b) -> {
                    Object aVal = a.get("totalMarketValue");
                    Object bVal = b.get("totalMarketValue");
                    double aDouble = (aVal instanceof Number) ? ((Number) aVal).doubleValue() : 0.0;
                    double bDouble = (bVal instanceof Number) ? ((Number) bVal).doubleValue() : 0.0;
                    return Double.compare(aDouble, bDouble);
                };
                break;
            case "dailyNetInflow":
                comparator = (a, b) -> {
                    Object aVal = a.get("dailyNetInflow");
                    Object bVal = b.get("dailyNetInflow");
                    double aDouble = (aVal instanceof Number) ? ((Number) aVal).doubleValue() : 0.0;
                    double bDouble = (bVal instanceof Number) ? ((Number) bVal).doubleValue() : 0.0;
                    return Double.compare(aDouble, bDouble);
                };
                break;
            case "netInflowRatio":
                comparator = (a, b) -> {
                    Object aVal = a.get("netInflowRatio");
                    Object bVal = b.get("netInflowRatio");
                    double aDouble = (aVal instanceof Number) ? ((Number) aVal).doubleValue() : 0.0;
                    double bDouble = (bVal instanceof Number) ? ((Number) bVal).doubleValue() : 0.0;
                    return Double.compare(aDouble, bDouble);
                };
                break;
            case "recentVolatility":
                comparator = (a, b) -> {
                    Object aVal = a.get("recentVolatility");
                    Object bVal = b.get("recentVolatility");
                    double aDouble = (aVal instanceof Number) ? ((Number) aVal).doubleValue() : 0.0;
                    double bDouble = (bVal instanceof Number) ? ((Number) bVal).doubleValue() : 0.0;
                    return Double.compare(aDouble, bDouble);
                };
                break;
            case "latest7dInflow":
                comparator = (a, b) -> {
                    Object aVal = a.get("latest7dInflow");
                    Object bVal = b.get("latest7dInflow");
                    double aDouble = (aVal instanceof Number) ? ((Number) aVal).doubleValue() : 0.0;
                    double bDouble = (bVal instanceof Number) ? ((Number) bVal).doubleValue() : 0.0;
                    return Double.compare(aDouble, bDouble);
                };
                break;
            default:
                // 默认按总市值排序
                comparator = (a, b) -> {
                    Object aVal = a.get("totalMarketValue");
                    Object bVal = b.get("totalMarketValue");
                    double aDouble = (aVal instanceof Number) ? ((Number) aVal).doubleValue() : 0.0;
                    double bDouble = (bVal instanceof Number) ? ((Number) bVal).doubleValue() : 0.0;
                    return Double.compare(aDouble, bDouble);
                };
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