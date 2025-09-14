package com.windindustry;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import java.util.*;

@SpringBootApplication
@RestController
public class SimpleWindApp {
    
    public static void main(String[] args) {
        System.setProperty("server.port", "5001");
        System.setProperty("spring.datasource.url", "jdbc:mysql://localhost:3306/pt?characterEncoding=utf8&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=Asia/Shanghai");
        System.setProperty("spring.datasource.driver-class-name", "com.mysql.cj.jdbc.Driver");
        System.setProperty("spring.datasource.username", "root");
        System.setProperty("spring.datasource.password", "rr1234RR");
        System.setProperty("spring.jpa.database-platform", "org.hibernate.dialect.MySQL8Dialect");
        System.setProperty("spring.jpa.hibernate.ddl-auto", "update");
        
        SpringApplication.run(SimpleWindApp.class, args);
    }
    
    @GetMapping("/")
    public String home() {
        return """
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
                            <h4>✅ Spring Boot API服务已启动！</h4>
                            <p>端口: 5001 | 数据库: MySQL | 状态: 运行中</p>
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
                    </div>
                </div>
            </div>
        </body>
        </html>
        """;
    }
    
    @GetMapping("/stock-mappings")
    public String stockMappings() {
        try {
            return java.nio.file.Files.readString(
                java.nio.file.Paths.get("src/main/resources/templates/stock-mappings.html")
            );
        } catch (Exception e) {
            return "redirect:/";
        }
    }
    
    @GetMapping("/data-analysis")
    public String dataAnalysis() {
        try {
            return java.nio.file.Files.readString(
                java.nio.file.Paths.get("src/main/resources/templates/data-analysis.html")
            );
        } catch (Exception e) {
            return "redirect:/";
        }
    }
    
    // 股票映射API模拟
    @GetMapping("/api/stock-mappings")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getStockMappings(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        
        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        
        // 模拟股票数据
        List<Map<String, Object>> stocks = new ArrayList<>();
        String[] stockCodes = {"000001", "000002", "000858", "002415", "300059", "600000", "600036", "600519", "000725"};
        String[] stockNames = {"平安银行", "万科A", "五粮液", "海康威视", "东方财富", "浦发银行", "招商银行", "贵州茅台", "京东方A"};
        String[] industries = {"银行", "房地产", "白酒", "安防", "证券", "银行", "银行", "白酒", "电子"};
        String[] marketTypes = {"A股", "A股", "A股", "A股", "A股", "A股", "A股", "A股", "A股"};
        
        Random random = new Random();
        for (int i = 0; i < Math.min(stockCodes.length, size); i++) {
            Map<String, Object> stock = new HashMap<>();
            stock.put("stockCode", stockCodes[i]);
            stock.put("stockName", stockNames[i]);
            stock.put("industryName", industries[i]);
            stock.put("marketType", marketTypes[i]);
            stock.put("mappingStatus", "已映射");
            stock.put("totalMarketValue", 50000 + random.nextInt(200000));
            stock.put("dailyNetInflow", random.nextInt(20000) - 10000);
            stock.put("netInflowRatio", (random.nextDouble() - 0.5) * 0.1);
            stock.put("recentVolatility", random.nextDouble() * 0.05);
            stock.put("latest7dInflow", random.nextInt(50000) - 25000);
            stock.put("lastUpdated", new Date());
            stocks.add(stock);
        }
        
        Map<String, Object> data = new HashMap<>();
        data.put("content", stocks);
        data.put("totalElements", stockCodes.length);
        data.put("totalPages", 1);
        data.put("currentPage", page);
        data.put("size", size);
        
        response.put("data", data);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/api/stock-mappings/stats")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getStockMappingStats() {
        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        
        Map<String, Object> stats = new HashMap<>();
        stats.put("total_stocks", 21);
        stats.put("mapped_count", 18);
        stats.put("unmapped_count", 3);
        stats.put("a_stock_count", 19);
        stats.put("kc_stock_count", 2);
        
        response.put("data", stats);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/api/wind-industries")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getWindIndustries() {
        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        
        List<Map<String, Object>> industries = new ArrayList<>();
        String[] industryCodes = {"110000", "210000", "220000", "230000", "240000"};
        String[] industryNames = {"银行", "房地产", "白酒", "医药", "科技"};
        
        for (int i = 0; i < industryCodes.length; i++) {
            Map<String, Object> industry = new HashMap<>();
            industry.put("industryCode", industryCodes[i]);
            industry.put("industryName", industryNames[i]);
            industry.put("industryLevel", 1);
            industries.add(industry);
        }
        
        response.put("data", industries);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/api/stock-mappings/refresh")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> refreshStockMappingData() {
        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        response.put("message", "股票映射数据刷新成功");
        return ResponseEntity.ok(response);
    }
}