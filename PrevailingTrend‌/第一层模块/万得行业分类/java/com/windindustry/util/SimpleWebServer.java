import java.io.*;
import java.net.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;

public class SimpleWebServer {
    private static final int PORT = 5001;
    private static final String WEB_ROOT = "src/main/resources";
    private static final String TEMPLATE_ROOT = "src/main/resources/templates";
    private static final String STATIC_ROOT = "src/main/resources/static";
    
    // Mock data
    private static final Map<String, Object> stats = new HashMap<>();
    private static final List<Map<String, Object>> industries = new ArrayList<>();
    private static final List<Map<String, Object>> stocks = new ArrayList<>();
    
    static {
        // Initialize stats
        stats.put("total_industries", 25L);
        stats.put("total_stocks", 100L);
        stats.put("level_1_count", 10L);
        stats.put("level_2_count", 15L);
        
        // Initialize industry data
        for (int i = 1; i <= 25; i++) {
            Map<String, Object> industry = new HashMap<>();
            industry.put("industry_code", "801" + String.format("%05d", i));
            industry.put("industry_name", "Industry " + i);
            industry.put("stock_count", 4);
            industry.put("avg_score", 75.5 + Math.random() * 20);
            industries.add(industry);
        }
        
        // Initialize stock data
        for (int i = 1; i <= 100; i++) {
            Map<String, Object> stock = new HashMap<>();
            stock.put("stock_code", String.format("%06d", i));
            stock.put("stock_name", "Stock " + i);
            stock.put("industry_code", "801" + String.format("%05d", (i % 25) + 1));
            stock.put("industry_name", "Industry " + ((i % 25) + 1));
            stock.put("prediction_score", 60 + Math.random() * 40);
            stock.put("confidence", 0.7 + Math.random() * 0.3);
            stocks.add(stock);
        }
    }
    
    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("Wind Industry Dashboard Starting...");
        System.out.println("Java Version: " + System.getProperty("java.version"));
        System.out.println("Working Directory: " + System.getProperty("user.dir"));
        System.out.println("========================================");
        
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Server started successfully, listening on port: " + PORT);
            System.out.println("Access URL: http://localhost:" + PORT);
            
            ExecutorService executor = Executors.newFixedThreadPool(10);
            
            while (true) {
                Socket clientSocket = serverSocket.accept();
                executor.submit(() -> handleRequest(clientSocket));
            }
        } catch (IOException e) {
            System.err.println("Server startup failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private static void handleRequest(Socket clientSocket) {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
             PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true)) {
            
            String requestLine = in.readLine();
            if (requestLine == null) return;
            
            String[] requestParts = requestLine.split(" ");
            String method = requestParts[0];
            String path = requestParts[1];
            
            System.out.println("Request: " + method + " " + path);
            
            if (path.equals("/")) {
                serveDashboard(out);
            } else if (path.equals("/api/stats")) {
                serveApiStats(out);
            } else if (path.equals("/api/industries")) {
                serveApiIndustries(out);
            } else if (path.equals("/api/stocks")) {
                serveApiStocks(out);
            } else if (path.startsWith("/static/")) {
                serveStaticFile(path, out, clientSocket);
            } else {
                serve404(out);
            }
            
        } catch (IOException e) {
            System.err.println("Error handling request: " + e.getMessage());
        } finally {
            try {
                clientSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    
    private static void serveDashboard(PrintWriter out) {
        try {
            String html = new String(Files.readAllBytes(Paths.get(TEMPLATE_ROOT, "dashboard.html")));
            
            out.println("HTTP/1.1 200 OK");
            out.println("Content-Type: text/html; charset=UTF-8");
            out.println("Content-Length: " + html.length());
            out.println();
            out.println(html);
            
        } catch (IOException e) {
            serve404(out);
        }
    }
    
    private static void serveApiStats(PrintWriter out) {
        String json = "{\n" +
                "  \"total_industries\": " + stats.get("total_industries") + ",\n" +
                "  \"total_stocks\": " + stats.get("total_stocks") + ",\n" +
                "  \"level_1_count\": " + stats.get("level_1_count") + ",\n" +
                "  \"level_2_count\": " + stats.get("level_2_count") + "\n" +
                "}";
        
        out.println("HTTP/1.1 200 OK");
        out.println("Content-Type: application/json; charset=UTF-8");
        out.println("Access-Control-Allow-Origin: *");
        out.println("Content-Length: " + json.length());
        out.println();
        out.println(json);
    }
    
    private static void serveApiIndustries(PrintWriter out) {
        StringBuilder json = new StringBuilder("{\n  \"data\": [\n");
        
        for (int i = 0; i < industries.size(); i++) {
            Map<String, Object> industry = industries.get(i);
            json.append("    {\n");
            json.append("      \"industry_code\": \"").append(industry.get("industry_code")).append("\",\n");
            json.append("      \"industry_name\": \"").append(industry.get("industry_name")).append("\",\n");
            json.append("      \"stock_count\": ").append(industry.get("stock_count")).append(",\n");
            json.append("      \"avg_score\": ").append(industry.get("avg_score")).append("\n");
            json.append("    }");
            if (i < industries.size() - 1) json.append(",");
            json.append("\n");
        }
        
        json.append("  ],\n");
        json.append("  \"total\": ").append(industries.size()).append("\n");
        json.append("}");
        
        String jsonStr = json.toString();
        
        out.println("HTTP/1.1 200 OK");
        out.println("Content-Type: application/json; charset=UTF-8");
        out.println("Access-Control-Allow-Origin: *");
        out.println("Content-Length: " + jsonStr.length());
        out.println();
        out.println(jsonStr);
    }
    
    private static void serveApiStocks(PrintWriter out) {
        StringBuilder json = new StringBuilder("{\n  \"data\": [\n");
        
        for (int i = 0; i < Math.min(20, stocks.size()); i++) {
            Map<String, Object> stock = stocks.get(i);
            json.append("    {\n");
            json.append("      \"stock_code\": \"").append(stock.get("stock_code")).append("\",\n");
            json.append("      \"stock_name\": \"").append(stock.get("stock_name")).append("\",\n");
            json.append("      \"industry_code\": \"").append(stock.get("industry_code")).append("\",\n");
            json.append("      \"industry_name\": \"").append(stock.get("industry_name")).append("\",\n");
            json.append("      \"prediction_score\": ").append(stock.get("prediction_score")).append(",\n");
            json.append("      \"confidence\": ").append(stock.get("confidence")).append("\n");
            json.append("    }");
            if (i < Math.min(20, stocks.size()) - 1) json.append(",");
            json.append("\n");
        }
        
        json.append("  ],\n");
        json.append("  \"total\": ").append(stocks.size()).append("\n");
        json.append("}");
        
        String jsonStr = json.toString();
        
        out.println("HTTP/1.1 200 OK");
        out.println("Content-Type: application/json; charset=UTF-8");
        out.println("Access-Control-Allow-Origin: *");
        out.println("Content-Length: " + jsonStr.length());
        out.println();
        out.println(jsonStr);
    }
    
    private static void serveStaticFile(String path, PrintWriter out, Socket clientSocket) {
        try {
            String filePath = STATIC_ROOT + path.substring(7); // Remove "/static"
            Path file = Paths.get(filePath);
            
            if (Files.exists(file)) {
                byte[] content = Files.readAllBytes(file);
                String contentType = getContentType(filePath);
                
                out.println("HTTP/1.1 200 OK");
                out.println("Content-Type: " + contentType);
                out.println("Content-Length: " + content.length);
                out.println();
                out.flush();
                
                clientSocket.getOutputStream().write(content);
            } else {
                serve404(out);
            }
        } catch (IOException e) {
            serve404(out);
        }
    }
    
    private static String getContentType(String filePath) {
        if (filePath.endsWith(".css")) return "text/css";
        if (filePath.endsWith(".js")) return "application/javascript";
        if (filePath.endsWith(".png")) return "image/png";
        if (filePath.endsWith(".jpg") || filePath.endsWith(".jpeg")) return "image/jpeg";
        return "text/plain";
    }
    
    private static void serve404(PrintWriter out) {
        String html = "<html><body><h1>404 Not Found</h1></body></html>";
        
        out.println("HTTP/1.1 404 Not Found");
        out.println("Content-Type: text/html; charset=UTF-8");
        out.println("Content-Length: " + html.length());
        out.println();
        out.println(html);
    }
}
