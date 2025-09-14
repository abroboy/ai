package com.prevailingtrend.handlers;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.*;
import java.util.*;
import com.google.gson.Gson;

/**
 * API处理器类
 */

// 第一层API处理器
class CompanyListApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    
    public void handle(HttpExchange exchange) throws IOException {
        // 模拟数据
        List<Map<String, Object>> companies = new ArrayList<>();
        
        Map<String, Object> company1 = new HashMap<>();
        company1.put("company_code", "000001");
        company1.put("company_name", "平安银行");
        company1.put("market", "深交所");
        company1.put("status", "ACTIVE");
        company1.put("create_time", "2024-01-01");
        companies.add(company1);
        
        Map<String, Object> company2 = new HashMap<>();
        company2.put("company_code", "000002");
        company2.put("company_name", "万科A");
        company2.put("market", "深交所");
        company2.put("status", "ACTIVE");
        company2.put("create_time", "2024-01-01");
        companies.add(company2);
        
        sendJsonResponse(exchange, companies);
    }
    
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class WindIndustryApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        
        Map<String, Object> item1 = new HashMap<>();
        item1.put("id", 1);
        item1.put("company_code", "000001");
        item1.put("industry_level1", "金融业");
        item1.put("industry_level2", "银行");
        item1.put("industry_level3", "股份制银行");
        item1.put("wind_code", "801020");
        item1.put("update_time", "2024-01-01");
        data.add(item1);
        
        sendJsonResponse(exchange, data);
    }
    
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class DomesticHotspotApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        
        Map<String, Object> item1 = new HashMap<>();
        item1.put("id", 1);
        item1.put("title", "央行降准释放流动性");
        item1.put("content", "央行宣布下调存款准备金率，释放长期流动性约1万亿元");
        item1.put("source", "财经新闻");
        item1.put("publish_time", "2024-01-15");
        item1.put("hotspot_score", 9.2);
        item1.put("keywords", "央行,降准,流动性");
        item1.put("related_industries", "银行,证券,保险");
        item1.put("create_time", "2024-01-15");
        data.add(item1);
        
        sendJsonResponse(exchange, data);
    }
    
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class InternationalHotspotApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class ForumHotspotApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class TencentIndexApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class GlobalCapitalFlowApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class InternetInfoApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

// 第二层API处理器
class CompanyAttributesApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class HotspotDataApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

// 第三层到第六层的API处理器 - 使用相同的模式
class TaxBankReportApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class FinancialStatementsApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class EnterpriseCheckApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class ForumDataApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class IndustryScoreApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class CompanyScoreApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class IndustryCompanyScoreApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class FactorWeightsApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

class CurvePredictionApiHandler implements HttpHandler {
    private static Gson gson = new Gson();
    public void handle(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();
        sendJsonResponse(exchange, data);
    }
    private void sendJsonResponse(HttpExchange exchange, Object data) throws IOException {
        String jsonResponse = gson.toJson(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] responseBytes = jsonResponse.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}