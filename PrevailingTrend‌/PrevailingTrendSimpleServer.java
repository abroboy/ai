package com.prevailingtrend;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.*;
import java.net.InetSocketAddress;

/**
 * PrevailingTrend Risk Framework Main Server
 * Unified access to all six-layer modules through port 80
 */
public class PrevailingTrendMainServer {
    
    public static void main(String[] args) throws Exception {
        System.out.println("========================================");
        System.out.println("PrevailingTrend Risk Framework Starting...");
        System.out.println("Unified Port: 80");
        System.out.println("========================================");
        
        // Create HTTP Server
        HttpServer server = HttpServer.create(new InetSocketAddress(80), 0);
        
        // Main page
        server.createContext("/", new MainPageHandler());
        
        // Layer routes
        server.createContext("/layer1/", new LayerHandler("Layer 1 - Data Collection"));
        server.createContext("/layer2/", new LayerHandler("Layer 2 - AI Data Processing"));
        server.createContext("/layer3/", new LayerHandler("Layer 3 - Deep Data Mining"));
        server.createContext("/layer4/", new LayerHandler("Layer 4 - Intelligent Scoring"));
        server.createContext("/layer5/", new LayerHandler("Layer 5 - Factor Weight Analysis"));
        server.createContext("/layer6/", new LayerHandler("Layer 6 - Curve Prediction Analysis"));
        
        server.setExecutor(null);
        server.start();
        
        System.out.println("✅ PrevailingTrend Risk Framework Server Started Successfully!");
        System.out.println("Access URL: http://localhost:80");
        System.out.println("========================================");
    }
    
    // Main page handler
    static class MainPageHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = generateMainPage();
            sendResponse(exchange, 200, response, "text/html");
        }
    }
    
    // Layer handler
    static class LayerHandler implements HttpHandler {
        private String layerName;
        
        public LayerHandler(String layerName) {
            this.layerName = layerName;
        }
        
        public void handle(HttpExchange exchange) throws IOException {
            String response = generateLayerPage(layerName);
            sendResponse(exchange, 200, response, "text/html");
        }
    }
    
    // Generate main page HTML
    private static String generateMainPage() {
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>大势所趋风险框架 - PrevailingTrend Risk Framework</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
            <style>
                body {
                    font-family: 'Microsoft YaHei', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }
                .main-container {
                    background: rgba(255, 255, 255, 0.95);
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    backdrop-filter: blur(10px);
                    margin: 20px;
                    padding: 40px;
                }
                .header-section {
                    text-align: center;
                    margin-bottom: 40px;
                }
                .header-title {
                    font-size: 3rem;
                    font-weight: 700;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }
                .layer-card {
                    background: white;
                    border-radius: 15px;
                    padding: 25px;
                    margin-bottom: 25px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                    border-left: 5px solid;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }
                .layer-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                }
                .layer-1 { border-left-color: #e74c3c; }
                .layer-2 { border-left-color: #f39c12; }
                .layer-3 { border-left-color: #f1c40f; }
                .layer-4 { border-left-color: #2ecc71; }
                .layer-5 { border-left-color: #3498db; }
                .layer-6 { border-left-color: #9b59b6; }
                .layer-title {
                    font-size: 1.5rem;
                    font-weight: 600;
                    margin-bottom: 15px;
                    display: flex;
                    align-items: center;
                }
                .layer-icon {
                    margin-right: 15px;
                    width: 40px;
                    height: 40px;
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 1.2rem;
                }
                .module-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-top: 15px;
                }
                .module-btn {
                    padding: 15px;
                    border: 2px solid #e9ecef;
                    border-radius: 10px;
                    background: #f8f9fa;
                    text-decoration: none;
                    color: #495057;
                    font-weight: 500;
                    text-align: center;
                    transition: all 0.3s ease;
                    display: block;
                }
                .module-btn:hover {
                    border-color: #007bff;
                    background: #007bff;
                    color: white;
                    text-decoration: none;
                    transform: scale(1.05);
                }
            </style>
        </head>
        <body>
            <div class="container-fluid">
                <div class="main-container">
                    <div class="header-section">
                        <h1 class="header-title">
                            <i class="bi bi-graph-up-arrow"></i>
                            大势所趋风险框架
                        </h1>
                        <p class="text-muted">PrevailingTrend Risk Framework</p>
                        <p class="text-muted">基于AI的智能风险分析框架 - 六层模块协同工作</p>
                    </div>
                    
                    <!-- Layer 1 Module -->
                    <div class="layer-card layer-1">
                        <div class="layer-title">
                            <div class="layer-icon bg-danger">
                                <i class="bi bi-database"></i>
                            </div>
                            第一层模块 - 基础数据采集
                        </div>
                        <p class="text-muted">信息数据有严格的时间限制，要二次确认数据是指定日期之前的数据</p>
                        <div class="module-grid">
                            <a href="/layer1/company-list" class="module-btn">公司名字列表</a>
                            <a href="/layer1/wind-industry" class="module-btn">万得行业分类</a>
                            <a href="/layer1/domestic-hotspot" class="module-btn">国内热点数据</a>
                            <a href="/layer1/international-hotspot" class="module-btn">国外热点数据</a>
                            <a href="/layer1/forum-hotspot" class="module-btn">雪球等论坛热点数据</a>
                            <a href="/layer1/tencent-index" class="module-btn">腾讯济安指数</a>
                            <a href="/layer1/global-capital-flow" class="module-btn">全球资金流向</a>
                            <a href="/layer1/internet-info" class="module-btn">其他互联网信息</a>
                        </div>
                    </div>
                    
                    <!-- Layer 2 Module -->
                    <div class="layer-card layer-2">
                        <div class="layer-title">
                            <div class="layer-icon bg-warning">
                                <i class="bi bi-gear"></i>
                            </div>
                            第二层模块 - AI数据加工
                        </div>
                        <p class="text-muted">通过AI加工第一层数据，生成公司属性和热点分析</p>
                        <div class="module-grid">
                            <a href="/layer2/company-attributes" class="module-btn">公司属性表</a>
                            <a href="/layer2/hotspot-data" class="module-btn">热点数据表</a>
                        </div>
                    </div>
                    
                    <!-- Layer 3 Module -->
                    <div class="layer-card layer-3">
                        <div class="layer-title">
                            <div class="layer-icon bg-warning">
                                <i class="bi bi-search"></i>
                            </div>
                            第三层模块 - 深度数据挖掘
                        </div>
                        <p class="text-muted">依赖第二层筛选出来的行业和公司，继续按照目标去排查以下数据</p>
                        <div class="module-grid">
                            <a href="/layer3/tax-bank-report" class="module-btn">税银报告</a>
                            <a href="/layer3/financial-statements" class="module-btn">财务三表</a>
                            <a href="/layer3/enterprise-check" class="module-btn">企查查数据</a>
                            <a href="/layer3/forum-data" class="module-btn">雪球等论坛数据</a>
                        </div>
                    </div>
                    
                    <!-- Layer 4 Module -->
                    <div class="layer-card layer-4">
                        <div class="layer-title">
                            <div class="layer-icon bg-success">
                                <i class="bi bi-calculator"></i>
                            </div>
                            第四层模块 - 智能评分算法
                        </div>
                        <p class="text-muted">依赖第三层的数据，通过AI找一个算法来计算</p>
                        <div class="module-grid">
                            <a href="/layer4/industry-score" class="module-btn">行业分值表</a>
                            <a href="/layer4/company-score" class="module-btn">公司分值表</a>
                            <a href="/layer4/industry-company-score" class="module-btn">行业+公司分值表</a>
                        </div>
                    </div>
                    
                    <!-- Layer 5 Module -->
                    <div class="layer-card layer-5">
                        <div class="layer-title">
                            <div class="layer-icon bg-info">
                                <i class="bi bi-sliders"></i>
                            </div>
                            第五层模块 - 因子权重分析
                        </div>
                        <p class="text-muted">通过因子权重，预测行业或公司业绩历史数据曲线，或二级市场曲线原始数据</p>
                        <div class="module-grid">
                            <a href="/layer5/factor-weights" class="module-btn">对象因子权重表</a>
                        </div>
                    </div>
                    
                    <!-- Layer 6 Module -->
                    <div class="layer-card layer-6">
                        <div class="layer-title">
                            <div class="layer-icon bg-primary">
                                <i class="bi bi-graph-up"></i>
                            </div>
                            第六层模块 - 曲线预测分析
                        </div>
                        <p class="text-muted">类似chatBI的能力，把数据曲线化。能够通过调整因子权重输出对比的曲线</p>
                        <div class="module-grid">
                            <a href="/layer6/curve-prediction" class="module-btn">曲线预测分析</a>
                        </div>
                    </div>
                    
                    <div class="text-center mt-4">
                        <p class="text-muted">
                            <i class="bi bi-shield-check"></i>
                            大势所趋风险框架 v1.0 | MySQL数据库 | AI智能分析
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """;
    }
    
    // Generate layer page
    private static String generateLayerPage(String layerName) {
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>""" + layerName + """</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="/">首页</a></li>
                        <li class="breadcrumb-item active">""" + layerName + """</li>
                    </ol>
                </nav>
                
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h3>""" + layerName + """</h3>
                    </div>
                    <div class="card-body">
                        <p>此模块正在开发中...</p>
                        <a href="/" class="btn btn-primary">返回首页</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """;
    }
    
    // Utility method
    static void sendResponse(HttpExchange exchange, int statusCode, String response, String contentType) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", contentType + "; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = response.getBytes("UTF-8");
        exchange.sendResponseHeaders(statusCode, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}