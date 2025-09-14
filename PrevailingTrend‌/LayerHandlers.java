package com.prevailingtrend.handlers;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.*;
import java.util.*;
import com.google.gson.Gson;

/**
 * 所有层的处理器
 */

// 第二层处理器
class Layer2Handler implements HttpHandler {
    public void handle(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        String response = "";
        
        if (path.equals("/layer2/company-attributes")) {
            response = generateCompanyAttributesPage();
        } else if (path.equals("/layer2/hotspot-data")) {
            response = generateHotspotDataPage();
        } else {
            response = generateLayer2MainPage();
        }
        
        sendResponse(exchange, 200, response, "text/html");
    }
    
    private String generateLayer2MainPage() {
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>第二层模块 - AI数据加工</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
        </head>
        <body>
            <div class="container-fluid mt-4">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="/">首页</a></li>
                        <li class="breadcrumb-item active">第二层模块</li>
                    </ol>
                </nav>
                
                <div class="card border-warning">
                    <div class="card-header bg-warning text-white">
                        <h3><i class="bi bi-gear"></i> 第二层模块 - AI数据加工</h3>
                        <p class="mb-0">通过AI加工第一层数据，生成公司属性和热点分析</p>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <i class="bi bi-building-gear fs-1 text-info"></i>
                                        <h5 class="card-title">公司属性表</h5>
                                        <p class="card-text">通过AI加工出来的，表的主键是联合主键：公司名字+行业分类</p>
                                        <a href="/layer2/company-attributes" class="btn btn-info">进入模块</a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6 mb-3">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <i class="bi bi-fire fs-1 text-danger"></i>
                                        <h5 class="card-title">热点数据表</h5>
                                        <p class="card-text">提炼出行业，受益的企业名字列表排序，热点评分项目，热点分值</p>
                                        <a href="/layer2/hotspot-data" class="btn btn-danger">进入模块</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """;
    }
    
    private String generateCompanyAttributesPage() { return "<h1>公司属性表</h1>"; }
    private String generateHotspotDataPage() { return "<h1>热点数据表</h1>"; }
    
    private void sendResponse(HttpExchange exchange, int statusCode, String response, String contentType) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", contentType + "; charset=UTF-8");
        byte[] responseBytes = response.getBytes("UTF-8");
        exchange.sendResponseHeaders(statusCode, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

// 第三层处理器
class Layer3Handler implements HttpHandler {
    public void handle(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        String response = generateLayer3MainPage();
        sendResponse(exchange, 200, response, "text/html");
    }
    
    private String generateLayer3MainPage() {
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>第三层模块 - 深度数据挖掘</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
        </head>
        <body>
            <div class="container-fluid mt-4">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="/">首页</a></li>
                        <li class="breadcrumb-item active">第三层模块</li>
                    </ol>
                </nav>
                
                <div class="card border-warning">
                    <div class="card-header bg-warning text-white">
                        <h3><i class="bi bi-search"></i> 第三层模块 - 深度数据挖掘</h3>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-3 mb-3">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <i class="bi bi-file-earmark-text fs-1 text-primary"></i>
                                        <h5 class="card-title">税银报告</h5>
                                        <a href="/layer3/tax-bank-report" class="btn btn-primary">进入模块</a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 mb-3">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <i class="bi bi-table fs-1 text-success"></i>
                                        <h5 class="card-title">财务三表</h5>
                                        <a href="/layer3/financial-statements" class="btn btn-success">进入模块</a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 mb-3">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <i class="bi bi-building-check fs-1 text-info"></i>
                                        <h5 class="card-title">企查查数据</h5>
                                        <a href="/layer3/enterprise-check" class="btn btn-info">进入模块</a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 mb-3">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <i class="bi bi-chat-square-dots fs-1 text-warning"></i>
                                        <h5 class="card-title">雪球等论坛数据</h5>
                                        <a href="/layer3/forum-data" class="btn btn-warning">进入模块</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """;
    }
    
    private void sendResponse(HttpExchange exchange, int statusCode, String response, String contentType) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", contentType + "; charset=UTF-8");
        byte[] responseBytes = response.getBytes("UTF-8");
        exchange.sendResponseHeaders(statusCode, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

// 第四层处理器
class Layer4Handler implements HttpHandler {
    public void handle(HttpExchange exchange) throws IOException {
        String response = generateLayer4MainPage();
        sendResponse(exchange, 200, response, "text/html");
    }
    
    private String generateLayer4MainPage() {
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>第四层模块 - 智能评分算法</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
        </head>
        <body>
            <div class="container-fluid mt-4">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="/">首页</a></li>
                        <li class="breadcrumb-item active">第四层模块</li>
                    </ol>
                </nav>
                
                <div class="card border-success">
                    <div class="card-header bg-success text-white">
                        <h3><i class="bi bi-calculator"></i> 第四层模块 - 智能评分算法</h3>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-4 mb-3">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <i class="bi bi-bar-chart fs-1 text-primary"></i>
                                        <h5 class="card-title">行业分值表</h5>
                                        <a href="/layer4/industry-score" class="btn btn-primary">进入模块</a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <i class="bi bi-building-fill-up fs-1 text-success"></i>
                                        <h5 class="card-title">公司分值表</h5>
                                        <a href="/layer4/company-score" class="btn btn-success">进入模块</a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <i class="bi bi-diagram-3-fill fs-1 text-info"></i>
                                        <h5 class="card-title">行业+公司分值表</h5>
                                        <a href="/layer4/industry-company-score" class="btn btn-info">进入模块</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """;
    }
    
    private void sendResponse(HttpExchange exchange, int statusCode, String response, String contentType) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", contentType + "; charset=UTF-8");
        byte[] responseBytes = response.getBytes("UTF-8");
        exchange.sendResponseHeaders(statusCode, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

// 第五层处理器
class Layer5Handler implements HttpHandler {
    public void handle(HttpExchange exchange) throws IOException {
        String response = generateLayer5MainPage();
        sendResponse(exchange, 200, response, "text/html");
    }
    
    private String generateLayer5MainPage() {
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>第五层模块 - 因子权重分析</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
        </head>
        <body>
            <div class="container-fluid mt-4">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="/">首页</a></li>
                        <li class="breadcrumb-item active">第五层模块</li>
                    </ol>
                </nav>
                
                <div class="card border-info">
                    <div class="card-header bg-info text-white">
                        <h3><i class="bi bi-sliders"></i> 第五层模块 - 因子权重分析</h3>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-12 mb-3">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <i class="bi bi-sliders fs-1 text-primary"></i>
                                        <h5 class="card-title">对象因子权重表</h5>
                                        <p class="card-text">通过因子权重，预测行业或公司业绩历史数据曲线</p>
                                        <a href="/layer5/factor-weights" class="btn btn-primary">进入模块</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """;
    }
    
    private void sendResponse(HttpExchange exchange, int statusCode, String response, String contentType) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", contentType + "; charset=UTF-8");
        byte[] responseBytes = response.getBytes("UTF-8");
        exchange.sendResponseHeaders(statusCode, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

// 第六层处理器
class Layer6Handler implements HttpHandler {
    public void handle(HttpExchange exchange) throws IOException {
        String response = generateLayer6MainPage();
        sendResponse(exchange, 200, response, "text/html");
    }
    
    private String generateLayer6MainPage() {
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>第六层模块 - 曲线预测分析</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
        </head>
        <body>
            <div class="container-fluid mt-4">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="/">首页</a></li>
                        <li class="breadcrumb-item active">第六层模块</li>
                    </ol>
                </nav>
                
                <div class="card border-primary">
                    <div class="card-header bg-primary text-white">
                        <h3><i class="bi bi-graph-up"></i> 第六层模块 - 曲线预测分析</h3>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-12 mb-3">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <i class="bi bi-graph-up fs-1 text-success"></i>
                                        <h5 class="card-title">曲线预测分析</h5>
                                        <p class="card-text">类似chatBI的能力，把数据曲线化，通过调整因子权重输出对比的曲线</p>
                                        <a href="/layer6/curve-prediction" class="btn btn-success">进入模块</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """;
    }
    
    private void sendResponse(HttpExchange exchange, int statusCode, String response, String contentType) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", contentType + "; charset=UTF-8");
        byte[] responseBytes = response.getBytes("UTF-8");
        exchange.sendResponseHeaders(statusCode, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}