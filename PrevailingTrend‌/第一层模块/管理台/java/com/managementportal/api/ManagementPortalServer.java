package com.managementportal.api;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * 管理台统一入口服务器
 * 提供多端口服务的统一管理界面
 */
public class ManagementPortalServer {
    
    public static void main(String[] args) throws Exception {
        System.out.println("========================================");
        System.out.println("趋势科技数据 - 统一管理台启动中...");
        System.out.println("提供多端口服务统一管理界面");
        System.out.println("Java版本: " + System.getProperty("java.version"));
        System.out.println("========================================");
        
        int port = 8090;
        // 如果8090端口被占用，尝试其他端口
        for (int tryPort = 8090; tryPort <= 8099; tryPort++) {
            try {
                HttpServer server = HttpServer.create(new InetSocketAddress(tryPort), 0);
                port = tryPort;
                
                // 主页
                server.createContext("/", new HomeHandler());
                
                server.setExecutor(null);
                server.start();
                
                System.out.println("✅ 管理台服务器启动成功！");
                System.out.println("访问地址: http://localhost:" + port);
                System.out.println("========================================");
                return;
            } catch (Exception e) {
                if (tryPort == 8099) {
                    System.err.println("❌ 无法找到可用端口，启动失败！");
                    System.err.println("错误: " + e.getMessage());
                    throw e;
                }
            }
        }
    }
    
    static class HomeHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try {
                String content = Files.readString(Paths.get("index.html"));
                sendResponse(exchange, 200, content, "text/html");
            } catch (Exception e) {
                String response = """
                <!DOCTYPE html>
                <html lang="zh-CN">
                <head>
                    <meta charset="UTF-8">
                    <title>趋势科技数据 - 统一管理台</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                </head>
                <body class="bg-primary">
                    <div class="container text-center text-white" style="margin-top: 100px;">
                        <h1>🚀 趋势科技数据</h1>
                        <h3>TrendTech Data Analytics</h3>
                        <p class="lead">多端口金融数据监控服务平台</p>
                        <div class="row mt-5">
                            <div class="col-md-2">
                                <div class="card">
                                    <div class="card-body">
                                        <h5>万得行业分类</h5>
                                        <a href="http://localhost:5001" class="btn btn-primary" target="_blank">端口 5001</a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="card">
                                    <div class="card-body">
                                        <h5>全球资金流向</h5>
                                        <a href="http://localhost:5002" class="btn btn-success" target="_blank">端口 5002</a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="card">
                                    <div class="card-body">
                                        <h5>国内热点数据</h5>
                                        <a href="http://localhost:5003" class="btn btn-danger" target="_blank">端口 5003</a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="card">
                                    <div class="card-body">
                                        <h5>国外热点数据</h5>
                                        <a href="http://localhost:5004" class="btn btn-secondary" target="_blank">端口 5004</a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="card">
                                    <div class="card-body">
                                        <h5>腾讯济安指数</h5>
                                        <a href="http://localhost:5005" class="btn btn-info" target="_blank">端口 5005</a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="card">
                                    <div class="card-body">
                                        <h5>论坛热点数据</h5>
                                        <a href="http://localhost:5006" class="btn btn-warning" target="_blank">端口 5006</a>
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
    }
    
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