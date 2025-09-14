package com.prevailingtrend.handlers;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.*;
import java.util.*;
import com.google.gson.Gson;

/**
 * 第一层模块处理器
 */
public class Layer1Handler implements HttpHandler {
    
    private static Gson gson = new Gson();
    
    public void handle(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        String response = "";
        
        if (path.equals("/layer1/company-list")) {
            response = generateCompanyListPage();
        } else if (path.equals("/layer1/wind-industry")) {
            response = generateWindIndustryPage();
        } else if (path.equals("/layer1/domestic-hotspot")) {
            response = generateDomesticHotspotPage();
        } else if (path.equals("/layer1/international-hotspot")) {
            response = generateInternationalHotspotPage();
        } else if (path.equals("/layer1/forum-hotspot")) {
            response = generateForumHotspotPage();
        } else if (path.equals("/layer1/tencent-index")) {
            response = generateTencentIndexPage();
        } else if (path.equals("/layer1/global-capital-flow")) {
            response = generateGlobalCapitalFlowPage();
        } else if (path.equals("/layer1/internet-info")) {
            response = generateInternetInfoPage();
        } else {
            response = generateLayer1MainPage();
        }
        
        sendResponse(exchange, 200, response, "text/html");
    }
    
    private static String generateLayer1MainPage() {
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>第一层模块 - 基础数据采集</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
        </head>
        <body>
            <div class="container-fluid mt-4">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="/">首页</a></li>
                        <li class="breadcrumb-item active">第一层模块</li>
                    </ol>
                </nav>
                
                <div class="row">
                    <div class="col-12">
                        <div class="card border-danger">
                            <div class="card-header bg-danger text-white">
                                <h3><i class="bi bi-database"></i> 第一层模块 - 基础数据采集</h3>
                                <p class="mb-0">信息数据有严格的时间限制，要二次确认数据是指定日期之前的数据</p>
                            </div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-3 mb-3">
                                        <div class="card h-100">
                                            <div class="card-body text-center">
                                                <i class="bi bi-building fs-1 text-primary"></i>
                                                <h5 class="card-title">公司名字列表</h5>
                                                <p class="card-text">维护所有监控公司的基础信息</p>
                                                <a href="/layer1/company-list" class="btn btn-primary">进入模块</a>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3 mb-3">
                                        <div class="card h-100">
                                            <div class="card-body text-center">
                                                <i class="bi bi-diagram-3 fs-1 text-success"></i>
                                                <h5 class="card-title">万得行业分类</h5>
                                                <p class="card-text">Wind行业分类数据管理</p>
                                                <a href="/layer1/wind-industry" class="btn btn-success">进入模块</a>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3 mb-3">
                                        <div class="card h-100">
                                            <div class="card-body text-center">
                                                <i class="bi bi-newspaper fs-1 text-danger"></i>
                                                <h5 class="card-title">国内热点数据</h5>
                                                <p class="card-text">国内财经热点信息采集</p>
                                                <a href="/layer1/domestic-hotspot" class="btn btn-danger">进入模块</a>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3 mb-3">
                                        <div class="card h-100">
                                            <div class="card-body text-center">
                                                <i class="bi bi-globe fs-1 text-secondary"></i>
                                                <h5 class="card-title">国外热点数据</h5>
                                                <p class="card-text">国际财经热点信息采集</p>
                                                <a href="/layer1/international-hotspot" class="btn btn-secondary">进入模块</a>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3 mb-3">
                                        <div class="card h-100">
                                            <div class="card-body text-center">
                                                <i class="bi bi-chat-dots fs-1 text-warning"></i>
                                                <h5 class="card-title">雪球等论坛热点数据</h5>
                                                <p class="card-text">社交媒体舆情数据采集</p>
                                                <a href="/layer1/forum-hotspot" class="btn btn-warning">进入模块</a>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3 mb-3">
                                        <div class="card h-100">
                                            <div class="card-body text-center">
                                                <i class="bi bi-graph-up fs-1 text-info"></i>
                                                <h5 class="card-title">腾讯济安指数</h5>
                                                <p class="card-text">腾讯济安金融指数数据</p>
                                                <a href="/layer1/tencent-index" class="btn btn-info">进入模块</a>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3 mb-3">
                                        <div class="card h-100">
                                            <div class="card-body text-center">
                                                <i class="bi bi-globe-americas fs-1 text-dark"></i>
                                                <h5 class="card-title">全球资金流向</h5>
                                                <p class="card-text">全球市场资金流向分析</p>
                                                <a href="/layer1/global-capital-flow" class="btn btn-dark">进入模块</a>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3 mb-3">
                                        <div class="card h-100">
                                            <div class="card-body text-center">
                                                <i class="bi bi-wifi fs-1 text-primary"></i>
                                                <h5 class="card-title">其他互联网信息</h5>
                                                <p class="card-text">其他互联网数据源</p>
                                                <a href="/layer1/internet-info" class="btn btn-primary">进入模块</a>
                                            </div>
                                        </div>
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
    
    private static String generateCompanyListPage() {
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>公司名字列表管理</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
        </head>
        <body>
            <div class="container-fluid mt-4">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="/">首页</a></li>
                        <li class="breadcrumb-item"><a href="/layer1/">第一层模块</a></li>
                        <li class="breadcrumb-item active">公司名字列表</li>
                    </ol>
                </nav>
                
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h4><i class="bi bi-building"></i> 公司名字列表管理</h4>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>公司代码</th>
                                        <th>公司名称</th>
                                        <th>市场</th>
                                        <th>状态</th>
                                        <th>操作</th>
                                    </tr>
                                </thead>
                                <tbody id="companyTableBody">
                                    <tr><td colspan="5" class="text-center">加载中...</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    fetch('/api/layer1/company-list')
                        .then(response => response.json())
                        .then(data => {
                            const tbody = document.getElementById('companyTableBody');
                            if (data.length === 0) {
                                tbody.innerHTML = '<tr><td colspan="5" class="text-center">暂无数据</td></tr>';
                            } else {
                                tbody.innerHTML = data.map(item => `
                                    <tr>
                                        <td>${item.company_code}</td>
                                        <td>${item.company_name}</td>
                                        <td>${item.market || 'N/A'}</td>
                                        <td><span class="badge bg-success">${item.status}</span></td>
                                        <td><button class="btn btn-sm btn-outline-primary">编辑</button></td>
                                    </tr>
                                `).join('');
                            }
                        });
                });
            </script>
        </body>
        </html>
        """;
    }
    
    private static String generateWindIndustryPage() { return "<h1>万得行业分类</h1>"; }
    private static String generateDomesticHotspotPage() { return "<h1>国内热点数据</h1>"; }
    private static String generateInternationalHotspotPage() { return "<h1>国外热点数据</h1>"; }
    private static String generateForumHotspotPage() { return "<h1>雪球等论坛热点数据</h1>"; }
    private static String generateTencentIndexPage() { return "<h1>腾讯济安指数</h1>"; }
    private static String generateGlobalCapitalFlowPage() { return "<h1>全球资金流向</h1>"; }
    private static String generateInternetInfoPage() { return "<h1>其他互联网信息</h1>"; }
    
    private static void sendResponse(HttpExchange exchange, int statusCode, String response, String contentType) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", contentType + "; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = response.getBytes("UTF-8");
        exchange.sendResponseHeaders(statusCode, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}