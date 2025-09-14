package com.prevailingtrend;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.*;
import java.net.InetSocketAddress;
import java.util.concurrent.Executors;

/**
 * 大势所趋风险框架主服务器
 * 统一端口80访问所有六层模块
 * 
 * @author 大势所趋风险框架团队
 * @version 1.0
 */
public class PrevailingTrendMainServer {
    
    private static final int PORT = 80;
    private static final String CHARSET = "UTF-8";
    
    public static void main(String[] args) throws Exception {
        System.out.println("========================================");
        System.out.println("大势所趋风险框架 - Java服务器启动中...");
        System.out.println("PrevailingTrend Risk Framework");
        System.out.println("统一端口：" + PORT);
        System.out.println("========================================");
        
        // 创建HTTP服务器
        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);
        
        // 设置线程池
        server.setExecutor(Executors.newFixedThreadPool(10));
        
        // 配置路由
        server.createContext("/", new MainPageHandler());
        server.createContext("/layer1/", new Layer1Handler());
        server.createContext("/layer2/", new Layer2Handler());
        server.createContext("/layer3/", new Layer3Handler());
        server.createContext("/layer4/", new Layer4Handler());
        server.createContext("/layer5/", new Layer5Handler());
        server.createContext("/layer6/", new Layer6Handler());
        server.createContext("/api/", new ApiHandler());
        
        // 启动服务器
        server.start();
        
        System.out.println("✅ 服务器启动成功！");
        System.out.println("访问地址: http://localhost:" + PORT);
        System.out.println("========================================");
    }
    
    /**
     * 主页处理器
     */
    static class MainPageHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String htmlContent = generateMainPageHtml();
            sendResponse(exchange, 200, htmlContent, "text/html");
        }
        
        private String generateMainPageHtml() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n");
            html.append("    <title>大势所趋风险框架 - PrevailingTrend Risk Framework</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            
            // Add CSS styles
            html.append("    <style>\n");
            html.append("        body {\n");
            html.append("            font-family: 'Microsoft YaHei', sans-serif;\n");
            html.append("            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n");
            html.append("            min-height: 100vh;\n");
            html.append("            margin: 0;\n");
            html.append("            padding: 0;\n");
            html.append("        }\n");
            html.append("        .layout-container {\n");
            html.append("            display: flex;\n");
            html.append("            min-height: 100vh;\n");
            html.append("            gap: 10px;\n");
            html.append("            padding: 15px;\n");
            html.append("        }\n");
            html.append("        .left-nav {\n");
            html.append("            width: 280px;\n");
            html.append("            background: rgba(255, 255, 255, 0.98);\n");
            html.append("            border-radius: 15px;\n");
            html.append("            padding: 20px;\n");
            html.append("            overflow-y: auto;\n");
            html.append("            box-shadow: 0 10px 30px rgba(0,0,0,0.1);\n");
            html.append("            border: 3px solid #e74c3c;\n");
            html.append("        }\n");
            html.append("        .main-content {\n");
            html.append("            flex: 1;\n");
            html.append("            background: rgba(255, 255, 255, 0.95);\n");
            html.append("            border-radius: 15px;\n");
            html.append("            padding: 30px;\n");
            html.append("            overflow-y: auto;\n");
            html.append("            box-shadow: 0 10px 30px rgba(0,0,0,0.1);\n");
            html.append("        }\n");
            html.append("        .nav-header {\n");
            html.append("            font-size: 1.2rem;\n");
            html.append("            font-weight: 700;\n");
            html.append("            color: #e74c3c;\n");
            html.append("            margin-bottom: 20px;\n");
            html.append("            text-align: center;\n");
            html.append("            padding: 10px;\n");
            html.append("            background: #f8f9fa;\n");
            html.append("            border-radius: 8px;\n");
            html.append("        }\n");
            html.append("        .layer-nav-item {\n");
            html.append("            margin-bottom: 15px;\n");
            html.append("            border: 2px solid;\n");
            html.append("            border-radius: 10px;\n");
            html.append("            overflow: hidden;\n");
            html.append("        }\n");
            html.append("        .layer-nav-item.layer-1 { border-color: #e74c3c; }\n");
            html.append("        .layer-nav-item.layer-2 { border-color: #f39c12; }\n");
            html.append("        .layer-nav-item.layer-3 { border-color: #f1c40f; }\n");
            html.append("        .layer-nav-item.layer-4 { border-color: #2ecc71; }\n");
            html.append("        .layer-nav-item.layer-5 { border-color: #3498db; }\n");
            html.append("        .layer-nav-item.layer-6 { border-color: #9b59b6; }\n");
            html.append("        .layer-header {\n");
            html.append("            padding: 12px 15px;\n");
            html.append("            font-weight: 600;\n");
            html.append("            cursor: pointer;\n");
            html.append("            transition: all 0.3s ease;\n");
            html.append("            display: flex;\n");
            html.append("            align-items: center;\n");
            html.append("            justify-content: space-between;\n");
            html.append("        }\n");
            html.append("        .layer-header:hover {\n");
            html.append("            background: rgba(0,0,0,0.05);\n");
            html.append("        }\n");
            html.append("        .layer-modules {\n");
            html.append("            padding: 10px;\n");
            html.append("            background: #f8f9fa;\n");
            html.append("            display: none;\n");
            html.append("        }\n");
            html.append("        .layer-modules.show {\n");
            html.append("            display: block;\n");
            html.append("        }\n");
            html.append("        .module-item {\n");
            html.append("            display: block;\n");
            html.append("            padding: 8px 12px;\n");
            html.append("            margin: 3px 0;\n");
            html.append("            background: white;\n");
            html.append("            border: 1px solid #ddd;\n");
            html.append("            border-radius: 5px;\n");
            html.append("            text-decoration: none;\n");
            html.append("            color: #495057;\n");
            html.append("            font-size: 0.9rem;\n");
            html.append("            transition: all 0.3s ease;\n");
            html.append("        }\n");
            html.append("        .module-item:hover {\n");
            html.append("            background: #007bff;\n");
            html.append("            color: white;\n");
            html.append("            text-decoration: none;\n");
            html.append("            transform: translateX(5px);\n");
            html.append("        }\n");
            html.append("        .header-title {\n");
            html.append("            font-size: 2.2rem;\n");
            html.append("            font-weight: 700;\n");
            html.append("            color: #2c3e50;\n");
            html.append("            text-align: center;\n");
            html.append("            margin-bottom: 30px;\n");
            html.append("            padding: 20px;\n");
            html.append("            background: linear-gradient(135deg, #667eea, #764ba2);\n");
            html.append("            color: white;\n");
            html.append("            border-radius: 15px;\n");
            html.append("            box-shadow: 0 5px 15px rgba(0,0,0,0.1);\n");
            html.append("        }\n");
            html.append("        .content-area {\n");
            html.append("            background: white;\n");
            html.append("            border-radius: 15px;\n");
            html.append("            padding: 40px;\n");
            html.append("            text-align: center;\n");
            html.append("            box-shadow: 0 5px 15px rgba(0,0,0,0.05);\n");
            html.append("            border: 2px dashed #dee2e6;\n");
            html.append("            min-height: 300px;\n");
            html.append("            display: flex;\n");
            html.append("            align-items: center;\n");
            html.append("            justify-content: center;\n");
            html.append("            flex-direction: column;\n");
            html.append("        }\n");
            html.append("        .content-message {\n");
            html.append("            font-size: 1.5rem;\n");
            html.append("            color: #6c757d;\n");
            html.append("            margin-bottom: 20px;\n");
            html.append("        }\n");
            html.append("        .expand-icon {\n");
            html.append("            transition: transform 0.3s ease;\n");
            html.append("        }\n");
            html.append("        .expand-icon.rotated {\n");
            html.append("            transform: rotate(90deg);\n");
            html.append("        }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            
            // Body content
            html.append("<body>\n");
            html.append("    <div class=\"layout-container\">\n");
            
            // 左侧导航栏
            html.append("        <div class=\"left-nav\">\n");
            html.append("            <div class=\"nav-header\">\n");
            html.append("                目录导航栏\n");
            html.append("            </div>\n");
            
            // 第一层模块
            html.append("            <div class=\"layer-nav-item layer-1\">\n");
            html.append("                <div class=\"layer-header\" onclick=\"toggleLayer('layer1')\">\n");
            html.append("                    <span><i class=\"bi bi-database\"></i> 第一层模块 - 基础数据采集</span>\n");
            html.append("                    <i class=\"bi bi-chevron-right expand-icon\" id=\"icon-layer1\"></i>\n");
            html.append("                </div>\n");
            html.append("                <div class=\"layer-modules\" id=\"modules-layer1\">\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('公司名字列表')\">公司名字列表</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('万得行业分类')\">万得行业分类</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('国内热点数据')\">国内热点数据</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('国外热点数据')\">国外热点数据</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('雪球等论坛热点数据')\">雪球等论坛热点数据</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('腾讯济安指数')\">腾讯济安指数</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('全球资金流向')\">全球资金流向</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('其他互联网信息')\">其他互联网信息</div>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
            
            // 第二层模块
            html.append("            <div class=\"layer-nav-item layer-2\">\n");
            html.append("                <div class=\"layer-header\" onclick=\"toggleLayer('layer2')\">\n");
            html.append("                    <span><i class=\"bi bi-gear\"></i> 第二层模块 - AI数据加工</span>\n");
            html.append("                    <i class=\"bi bi-chevron-right expand-icon\" id=\"icon-layer2\"></i>\n");
            html.append("                </div>\n");
            html.append("                <div class=\"layer-modules\" id=\"modules-layer2\">\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('公司属性表')\">公司属性表</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('热点数据表')\">热点数据表</div>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
            
            // 第三层模块
            html.append("            <div class=\"layer-nav-item layer-3\">\n");
            html.append("                <div class=\"layer-header\" onclick=\"toggleLayer('layer3')\">\n");
            html.append("                    <span><i class=\"bi bi-search\"></i> 第三层模块 - 深度数据挖掘</span>\n");
            html.append("                    <i class=\"bi bi-chevron-right expand-icon\" id=\"icon-layer3\"></i>\n");
            html.append("                </div>\n");
            html.append("                <div class=\"layer-modules\" id=\"modules-layer3\">\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('税银报告')\">税银报告</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('财务三表')\">财务三表</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('企查查数据')\">企查查数据</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('雪球等论坛数据')\">雪球等论坛数据</div>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
            
            // 第四层模块
            html.append("            <div class=\"layer-nav-item layer-4\">\n");
            html.append("                <div class=\"layer-header\" onclick=\"toggleLayer('layer4')\">\n");
            html.append("                    <span><i class=\"bi bi-calculator\"></i> 第四层模块 - 智能评分算法</span>\n");
            html.append("                    <i class=\"bi bi-chevron-right expand-icon\" id=\"icon-layer4\"></i>\n");
            html.append("                </div>\n");
            html.append("                <div class=\"layer-modules\" id=\"modules-layer4\">\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('行业分值表')\">行业分值表</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('公司分值表')\">公司分值表</div>\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('行业+公司分值表')\">行业+公司分值表</div>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
            
            // 第五层模块
            html.append("            <div class=\"layer-nav-item layer-5\">\n");
            html.append("                <div class=\"layer-header\" onclick=\"toggleLayer('layer5')\">\n");
            html.append("                    <span><i class=\"bi bi-sliders\"></i> 第五层模块 - 因子权重分析</span>\n");
            html.append("                    <i class=\"bi bi-chevron-right expand-icon\" id=\"icon-layer5\"></i>\n");
            html.append("                </div>\n");
            html.append("                <div class=\"layer-modules\" id=\"modules-layer5\">\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('对象因子权重表')\">对象因子权重表</div>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
            
            // 第六层模块
            html.append("            <div class=\"layer-nav-item layer-6\">\n");
            html.append("                <div class=\"layer-header\" onclick=\"toggleLayer('layer6')\">\n");
            html.append("                    <span><i class=\"bi bi-graph-up\"></i> 第六层模块 - 曲线预测分析</span>\n");
            html.append("                    <i class=\"bi bi-chevron-right expand-icon\" id=\"icon-layer6\"></i>\n");
            html.append("                </div>\n");
            html.append("                <div class=\"layer-modules\" id=\"modules-layer6\">\n");
            html.append("                    <div class=\"module-item\" onclick=\"loadModule('曲线预测分析')\">曲线预测分析</div>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
            html.append("        </div>\n");
            
            // 中间主要内容区域
            html.append("        <div class=\"main-content\">\n");
            html.append("            <div class=\"header-title\">\n");
            html.append("                <i class=\"bi bi-graph-up-arrow\"></i>\n");
            html.append("                大势所趋风险框架\n");
            html.append("            </div>\n");
            html.append("            \n");
            html.append("            <div class=\"content-area\">\n");
            html.append("                <div class=\"content-message\">\n");
            html.append("                    这里是左边点击后，显示的子页面。\n");
            html.append("                </div>\n");
            html.append("                <div class=\"text-muted\">\n");
            html.append("                    <i class=\"bi bi-arrow-left\"></i> 请从左侧导航栏选择模块查看详细内容\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
            html.append("        </div>\n");
            html.append("    </div>\n");
            
            // JavaScript功能
            html.append("    <script>\n");
            html.append("        function toggleLayer(layerId) {\n");
            html.append("            const modules = document.getElementById('modules-' + layerId);\n");
            html.append("            const icon = document.getElementById('icon-' + layerId);\n");
            html.append("            \n");
            html.append("            if (modules.classList.contains('show')) {\n");
            html.append("                modules.classList.remove('show');\n");
            html.append("                icon.classList.remove('rotated');\n");
            html.append("            } else {\n");
            html.append("                modules.classList.add('show');\n");
            html.append("                icon.classList.add('rotated');\n");
            html.append("            }\n");
            html.append("        }\n");
            html.append("        \n");
            html.append("        function loadModule(moduleName) {\n");
            html.append("            const contentArea = document.querySelector('.content-area');\n");
            html.append("            contentArea.innerHTML = `\n");
            html.append("                <div class=\"content-message\">\n");
            html.append("                    正在加载：${moduleName}\n");
            html.append("                </div>\n");
            html.append("                <div class=\"text-muted\">\n");
            html.append("                    <i class=\"bi bi-gear-fill\"></i> 模块功能开发中，即将上线...\n");
            html.append("                </div>\n");
            html.append("            `;\n");
            html.append("        }\n");
            html.append("        \n");
            html.append("        // 页面加载完成后的初始化\n");
            html.append("        document.addEventListener('DOMContentLoaded', function() {\n");
            html.append("            console.log('大势所趋风险框架管理台已加载');\n");
            html.append("        });\n");
            html.append("    </script>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            
            return html.toString();
        }
    }
    
    /**
     * 层级处理器基类
     */
    static abstract class LayerHandler implements HttpHandler {
        protected final String layerName;
        
        public LayerHandler(String layerName) {
            this.layerName = layerName;
        }
        
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String response = generateLayerPage();
            sendResponse(exchange, 200, response, "text/html");
        }
        
        protected String generateLayerPage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>").append(layerName).append("</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("</head>\n");
            html.append("<body class=\"bg-light\">\n");
            html.append("    <div class=\"container mt-4\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">").append(layerName).append("</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        \n");
            html.append("        <div class=\"card\">\n");
            html.append("            <div class=\"card-header bg-primary text-white\">\n");
            html.append("                <h3>").append(layerName).append("</h3>\n");
            html.append("            </div>\n");
            html.append("            <div class=\"card-body\">\n");
            html.append("                <div class=\"alert alert-info\">\n");
            html.append("                    <i class=\"bi bi-info-circle\"></i>\n");
            html.append("                    此模块正在开发中，将提供完整的数据管理和分析功能。\n");
            html.append("                </div>\n");
            html.append("                <a href=\"/\" class=\"btn btn-primary\">返回首页</a>\n");
            html.append("            </div>\n");
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
    }
    
    // 各层处理器实现
    static class Layer1Handler extends LayerHandler {
        public Layer1Handler() { super("第一层模块 - 基础数据采集"); }
    }
    
    static class Layer2Handler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String path = exchange.getRequestURI().getPath();
        }
    }
    
    static class Layer3Handler extends LayerHandler {
        public Layer3Handler() { super("第三层模块 - 深度数据挖掘"); }
    }
    
    static class Layer4Handler extends LayerHandler {
        public Layer4Handler() { super("第四层模块 - 智能评分算法"); }
    }
    
    static class Layer5Handler extends LayerHandler {
        public Layer5Handler() { super("第五层模块 - 因子权重分析"); }
    }
    
    static class Layer6Handler extends LayerHandler {
        public Layer6Handler() { super("第六层模块 - 曲线预测分析"); }
    }
    
    /**
     * API处理器
     */
    static class ApiHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String path = exchange.getRequestURI().getPath();
            String response;
            
            if (path.contains("company-attributes")) {
                response = generateCompanyAttributesPage();
            } else if (path.contains("hotspot-data")) {
                response = generateHotspotDataPage();
            } else {
                response = generateLayer2HomePage();
            }
            
            sendResponse(exchange, 200, response, "text/html");
        }
        
        private String generateLayer2HomePage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>第二层模块 - AI数据加工</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            html.append("    <style>\n");
            html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); min-height: 100vh; }\n");
            html.append("        .module-card { background: rgba(255,255,255,0.95); border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 20px; border: 2px solid #f39c12; }\n");
            html.append("        .module-header { background: linear-gradient(135deg, #f39c12, #e67e22); color: white; padding: 20px; border-radius: 13px 13px 0 0; }\n");
            html.append("        .feature-card { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 10px; padding: 20px; margin-bottom: 15px; }\n");
            html.append("        .btn-custom { background: linear-gradient(135deg, #f39c12, #e67e22); border: none; color: white; }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            html.append("<body>\n");
            html.append("    <div class=\"container-fluid\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">第二层模块</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"module-card\">\n");
            html.append("            <div class=\"module-header\">\n");
            html.append("                <h2><i class=\"bi bi-gear-fill\"></i> 第二层模块 - AI数据加工</h2>\n");
            html.append("                <p class=\"mb-0\">将第一层的原始数据通过AI算法进行智能加工处理</p>\n");
            html.append("            </div>\n");
            html.append("            <div class=\"p-4\">\n");
            html.append("                <div class=\"feature-card\">\n");
            html.append("                    <h4><i class=\"bi bi-building\"></i> 公司属性表</h4>\n");
            html.append("                    <p>对公司基础信息进行AI分析和属性标注</p>\n");
            html.append("                    <a href=\"/layer2/company-attributes\" class=\"btn btn-custom\">\n");
            html.append("                        <i class=\"bi bi-table\"></i> 查看公司属性表\n");
            html.append("                    </a>\n");
            html.append("                </div>\n");
            html.append("                <div class=\"feature-card\">\n");
            html.append("                    <h4><i class=\"bi bi-fire\"></i> 热点数据表</h4>\n");
            html.append("                    <p>通过AI算法分析热点数据，提取关键信息</p>\n");
            html.append("                    <a href=\"/layer2/hotspot-data\" class=\"btn btn-custom\">\n");
            html.append("                        <i class=\"bi bi-table\"></i> 查看热点数据表\n");
            html.append("                    </a>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
        
        private String generateCompanyAttributesPage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>公司属性表 - AI数据加工</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            html.append("    <style>\n");
            html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); min-height: 100vh; }\n");
            html.append("        .table-container { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }\n");
            html.append("        .table th { background: linear-gradient(135deg, #f39c12, #e67e22); color: white; }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            html.append("<body>\n");
            html.append("    <div class=\"container-fluid\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/layer2/\">第二层模块</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">公司属性表</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"table-container\">\n");
            html.append("            <h3><i class=\"bi bi-building\"></i> 公司属性表</h3>\n");
            html.append("            <div class=\"table-responsive\">\n");
            html.append("                <table class=\"table table-hover\">\n");
            html.append("                    <thead>\n");
            html.append("                        <tr>\n");
            html.append("                            <th>公司名称</th><th>股票代码</th><th>所属行业</th><th>公司规模</th><th>市值(亿)</th>\n");
            html.append("                        </tr>\n");
            html.append("                    </thead>\n");
            html.append("                    <tbody>\n");
            
            // 添加示例数据
            String[][] companies = {
                {"中国平安", "000001", "保险", "大型", "1,245.8"},
                {"贵州茅台", "600519", "白酒", "大型", "2,156.3"},
                {"腾讯控股", "00700", "互联网", "大型", "3,287.5"},
                {"比亚迪", "002594", "新能源", "大型", "1,089.2"},
                {"宁德时代", "300750", "电池", "大型", "1,567.9"}
            };
            
            for (String[] company : companies) {
                html.append("                        <tr>\n");
                for (String field : company) {
                    html.append("                            <td>").append(field).append("</td>\n");
                }
                html.append("                        </tr>\n");
            }
            
            html.append("                    </tbody>\n");
            html.append("                </table>\n");
            html.append("            </div>\n");
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
        
        private String generateHotspotDataPage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>热点数据表 - AI数据加工</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            html.append("    <style>\n");
            html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); min-height: 100vh; }\n");
            html.append("        .hotspot-container { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }\n");
            html.append("        .hotspot-item { border-left: 4px solid #e74c3c; padding: 15px; margin-bottom: 15px; background: #f8f9fa; border-radius: 8px; }\n");
            html.append("        .sentiment-positive { color: #2ecc71; } .sentiment-negative { color: #e74c3c; } .sentiment-neutral { color: #95a5a6; }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            html.append("<body>\n");
            html.append("    <div class=\"container-fluid\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/layer2/\">第二层模块</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">热点数据表</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"hotspot-container\">\n");
            html.append("            <h3><i class=\"bi bi-fire\"></i> 实时热点数据分析</h3>\n");
            
            // 添加热点数据项
            String[][] hotspots = {
                {"人工智能赛道持续升温", "积极", "92", "新浪财经"},
                {"新能源汽车销量创新高", "积极", "88", "中国证券报"},
                {"半导体行业回暖趋势明显", "积极", "85", "第一财经"},
                {"房地产市场政策调整预期", "中性", "65", "经济参考报"},
                {"美联储加息预期渐趋缓和", "积极", "78", "华尔街日报"}
            };
            
            for (String[] hotspot : hotspots) {
                String sentimentClass = "sentiment-positive";
                if (hotspot[1].equals("中性")) sentimentClass = "sentiment-neutral";
                else if (hotspot[1].equals("消极")) sentimentClass = "sentiment-negative";
                
                html.append("            <div class=\"hotspot-item\">\n");
                html.append("                <div class=\"d-flex justify-content-between align-items-start\">\n");
                html.append("                    <div class=\"flex-grow-1\">\n");
                html.append("                        <h5>").append(hotspot[0]).append("</h5>\n");
                html.append("                        <div class=\"d-flex align-items-center gap-3\">\n");
                html.append("                            <span class=\"badge bg-secondary\">").append(hotspot[3]).append("</span>\n");
                html.append("                            <span class=\"").append(sentimentClass).append("\"><i class=\"bi bi-heart-fill\"></i> 情感: ").append(hotspot[1]).append("</span>\n");
                html.append("                            <span class=\"text-primary\"><i class=\"bi bi-graph-up\"></i> 热度: ").append(hotspot[2]).append("</span>\n");
                html.append("                        </div>\n");
                html.append("                    </div>\n");
                html.append("                    <small class=\"text-muted\">").append((int)(Math.random() * 30) + 1).append("分钟前</small>\n");
                html.append("                </div>\n");
                html.append("            </div>\n");
            }
            
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
    }
    
    static class Layer3Handler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String path = exchange.getRequestURI().getPath();
            String response;
            
            if (path.contains("tax-bank-report")) {
                response = generateTaxBankReportPage();
            } else if (path.contains("financial-statements")) {
                response = generateFinancialStatementsPage();
            } else if (path.contains("qichacha-data")) {
                response = generateQichachaDataPage();
            } else if (path.contains("forum-data")) {
                response = generateForumDataPage();
            } else {
                response = generateLayer3HomePage();
            }
            
            sendResponse(exchange, 200, response, "text/html");
        }
        
        private String generateLayer3HomePage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>第三层模块 - 深度数据挖掘</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            html.append("    <style>\n");
            html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); min-height: 100vh; }\n");
            html.append("        .module-card { background: rgba(255,255,255,0.95); border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 20px; border: 2px solid #f1c40f; }\n");
            html.append("        .module-header { background: linear-gradient(135deg, #f1c40f, #f39c12); color: white; padding: 20px; border-radius: 13px 13px 0 0; }\n");
            html.append("        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }\n");
            html.append("        .feature-card { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 10px; padding: 20px; transition: all 0.3s ease; }\n");
            html.append("        .feature-card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }\n");
            html.append("        .btn-custom { background: linear-gradient(135deg, #f1c40f, #f39c12); border: none; color: white; }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            html.append("<body>\n");
            html.append("    <div class=\"container-fluid\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">第三层模块</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"module-card\">\n");
            html.append("            <div class=\"module-header\">\n");
            html.append("                <h2><i class=\"bi bi-search\"></i> 第三层模块 - 深度数据挖掘</h2>\n");
            html.append("                <p class=\"mb-0\">对第二层的数据进行深度挖掘和分析</p>\n");
            html.append("            </div>\n");
            html.append("            <div class=\"p-4\">\n");
            html.append("                <div class=\"feature-grid\">\n");
            html.append("                    <div class=\"feature-card\">\n");
            html.append("                        <h4><i class=\"bi bi-file-earmark-bar-graph\"></i> 税务银行报告</h4>\n");
            html.append("                        <p>分析公司税务和银行报告中的关键数据</p>\n");
            html.append("                        <a href=\"/layer3/tax-bank-report\" class=\"btn btn-custom\">\n");
            html.append("                            <i class=\"bi bi-file-earmark-bar-graph\"></i> 查看税务银行报告\n");
            html.append("                        </a>\n");
            html.append("                    </div>\n");
            html.append("                    <div class=\"feature-card\">\n");
            html.append("                        <h4><i class=\"bi bi-file-earmark-spreadsheet\"></i> 财务报表</h4>\n");
            html.append("                        <p>分析公司的财务报表数据</p>\n");
            html.append("                        <a href=\"/layer3/financial-statements\" class=\"btn btn-custom\">\n");
            html.append("                            <i class=\"bi bi-file-earmark-spreadsheet\"></i> 查看财务报表\n");
            html.append("                        </a>\n");
            html.append("                    </div>\n");
            html.append("                    <div class=\"feature-card\">\n");
            html.append("                        <h4><i class=\"bi bi-file-earmark-text\"></i> 工商数据</h4>\n");
            html.append("                        <p>分析公司的工商数据</p>\n");
            html.append("                        <a href=\"/layer3/qichacha-data\" class=\"btn btn-custom\">\n");
            html.append("                            <i class=\"bi bi-file-earmark-text\"></i> 查看工商数据\n");
            html.append("                        </a>\n");
            html.append("                    </div>\n");
            html.append("                    <div class=\"feature-card\">\n");
            html.append("                        <h4><i class=\"bi bi-chat-left-text\"></i> 论坛数据</h4>\n");
            html.append("                        <p>分析公司相关的论坛讨论数据</p>\n");
            html.append("                        <a href=\"/layer3/forum-data\" class=\"btn btn-custom\">\n");
            html.append("                            <i class=\"bi bi-chat-left-text\"></i> 查看论坛数据\n");
            html.append("                        </a>\n");
            html.append("                    </div>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
        
        private String generateTaxBankReportPage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>税务银行报告 - 深度数据挖掘</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            html.append("    <style>\n");
            html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); min-height: 100vh; }\n");
            html.append("        .report-container { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }\n");
            html.append("        .report-item { border-left: 4px solid #e74c3c; padding: 15px; margin-bottom: 15px; background: #f8f9fa; border-radius: 8px; }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            html.append("<body>\n");
            html.append("    <div class=\"container-fluid\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/layer3/\">第三层模块</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">税务银行报告</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"report-container\">\n");
            html.append("            <h3><i class=\"bi bi-file-earmark-bar-graph\"></i> 税务银行报告</h3>\n");
            
            // 添加税务银行报告项
            String[][] reports = {
                {"中国平安", "2022", "1,245.8", "10.2", "12.3"},
                {"贵州茅台", "2022", "2,156.3", "11.5", "13.8"},
                {"腾讯控股", "2022", "3,287.5", "12.7", "14.1"},
                {"比亚迪", "2022", "1,089.2", "10.5", "11.9"},
                {"宁德时代", "2022", "1,567.9", "11.8", "13.2"}
            };
            
            for (String[] report : reports) {
                html.append("            <div class=\"report-item\">\n");
                html.append("                <div class=\"d-flex justify-content-between align-items-start\">\n");
                html.append("                    <div class=\"flex-grow-1\">\n");
                html.append("                        <h5>").append(report[0]).append("</h5>\n");
                html.append("                        <div class=\"d-flex align-items-center gap-3\">\n");
                html.append("                            <span class=\"badge bg-secondary\">").append(report[1]).append("</span>\n");
                html.append("                            <span class=\"text-primary\"><i class=\"bi bi-graph-up\"></i> 市值(亿): ").append(report[2]).append("</span>\n");
                html.append("                            <span class=\"text-primary\"><i class=\"bi bi-graph-up\"></i> 净利润(亿): ").append(report[3]).append("</span>\n");
                html.append("                            <span class=\"text-primary\"><i class=\"bi bi-graph-up\"></i> 股息率(%): ").append(report[4]).append("</span>\n");
                html.append("                        </div>\n");
                html.append("                    </div>\n");
                html.append("                    <small class=\"text-muted\">").append((int)(Math.random() * 30) + 1).append("分钟前</small>\n");
                html.append("                </div>\n");
                html.append("            </div>\n");
            }
            
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
        
        private String generateFinancialStatementsPage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>财务报表 - 深度数据挖掘</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            html.append("    <style>\n");
            html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); min-height: 100vh; }\n");
            html.append("        .statement-container { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }\n");
            html.append("        .statement-item { border-left: 4px solid #e74c3c; padding: 15px; margin-bottom: 15px; background: #f8f9fa; border-radius: 8px; }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            html.append("<body>\n");
            html.append("    <div class=\"container-fluid\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/layer3/\">第三层模块</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">财务报表</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"statement-container\">\n");
            html.append("            <h3><i class=\"bi bi-file-earmark-spreadsheet\"></i> 财务报表</h3>\n");
            
            // 添加财务报表项
            String[][] statements = {
                {"中国平安", "2022", "1,245.8", "10.2", "12.3"},
                {"贵州茅台", "2022", "2,156.3", "11.5", "13.8"},
                {"腾讯控股", "2022", "3,287.5", "12.7", "14.1"},
                {"比亚迪", "2022", "1,089.2", "10.5", "11.9"},
                {"宁德时代", "2022", "1,567.9", "11.8", "13.2"}
            };
            
            for (String[] statement : statements) {
                html.append("            <div class=\"statement-item\">\n");
                html.append("                <div class=\"d-flex justify-content-between align-items-start\">\n");
                html.append("                    <div class=\"flex-grow-1\">\n");
                html.append("                        <h5>").append(statement[0]).append("</h5>\n");
                html.append("                        <div class=\"d-flex align-items-center gap-3\">\n");
                html.append("                            <span class=\"badge bg-secondary\">").append(statement[1]).append("</span>\n");
                html.append("                            <span class=\"text-primary\"><i class=\"bi bi-graph-up\"></i> 市值(亿): ").append(statement[2]).append("</span>\n");
                html.append("                            <span class=\"text-primary\"><i class=\"bi bi-graph-up\"></i> 净利润(亿): ").append(statement[3]).append("</span>\n");
                html.append("                            <span class=\"text-primary\"><i class=\"bi bi-graph-up\"></i> 股息率(%): ").append(statement[4]).append("</span>\n");
                html.append("                        </div>\n");
                html.append("                    </div>\n");
                html.append("                    <small class=\"text-muted\">").append((int)(Math.random() * 30) + 1).append("分钟前</small>\n");
                html.append("                </div>\n");
                html.append("            </div>\n");
            }
            
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
    }
    
    private String generateTaxBankReportPage() {
        StringBuilder html = new StringBuilder();
        html.append("<!DOCTYPE html>\n");
        html.append("<html lang=\"zh-CN\">\n");
        html.append("<head>\n");
        html.append("    <meta charset=\"UTF-8\">\n");
        html.append("    <title>税银报告 - 深度数据挖掘</title>\n");
        html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
        html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
        html.append("    <style>\n");
        html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); min-height: 100vh; }\n");
        html.append("        .report-container { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }\n");
        html.append("        .metric-card { background: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin-bottom: 15px; border-radius: 8px; }\n");
        html.append("        .risk-high { border-left-color: #e74c3c; } .risk-medium { border-left-color: #f39c12; } .risk-low { border-left-color: #2ecc71; }\n");
        html.append("    </style>\n");
        html.append("</head>\n");
        html.append("<body>\n");
        html.append("    <div class=\"container-fluid\">\n");
        html.append("        <nav aria-label=\"breadcrumb\">\n");
        html.append("            <ol class=\"breadcrumb\">\n");
        html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
        html.append("                <li class=\"breadcrumb-item\"><a href=\"/layer3/\">第三层模块</a></li>\n");
        html.append("                <li class=\"breadcrumb-item active\">税银报告</li>\n");
        html.append("            </ol>\n");
        html.append("        </nav>\n");
        html.append("        <div class=\"report-container\">\n");
        html.append("            <h3><i class=\"bi bi-file-earmark-text\"></i> 税银报告分析</h3>\n");
        
        // 税银数据示例
        String[][] taxData = {
            {"中国平安", "税收健康", "AAA", "低风险", "98.5%"},
            {"贵州茅台", "税收健康", "AA+", "低风险", "97.2%"},
            {"腾讯控股", "税收健康", "AA", "低风险", "95.8%"},
            {"比亚迪", "税收正常", "A+", "中风险", "89.3%"},
            {"宁德时代", "税收健康", "AA-", "低风险", "93.7%"}
        };
        
        for (String[] data : taxData) {
            String riskClass = data[3].contains("低") ? "risk-low" : data[3].contains("中") ? "risk-medium" : "risk-high";
            html.append("            <div class=\"metric-card ").append(riskClass).append("\">\n");
            html.append("                <div class=\"row align-items-center\">\n");
            html.append("                    <div class=\"col-md-3\"><strong>").append(data[0]).append("</strong></div>\n");
            html.append("                    <div class=\"col-md-2\"><span class=\"badge bg-success\">").append(data[1]).append("</span></div>\n");
            html.append("                    <div class=\"col-md-2\"><span class=\"badge bg-primary\">信用评级: ").append(data[2]).append("</span></div>\n");
            html.append("                    <div class=\"col-md-2\"><span class=\"badge bg-warning\">").append(data[3]).append("</span></div>\n");
            html.append("                    <div class=\"col-md-3\"><span class=\"text-success\">合规率: ").append(data[4]).append("</span></div>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
        }
        
        html.append("        </div>\n");
        html.append("    </div>\n");
        html.append("</body>\n");
        html.append("</html>\n");
        return html.toString();
    }
    
    private String generateFinancialStatementsPage() {
        return "<html><body><h1>财务三表正在开发中...</h1><a href='/layer3/'>返回</a></body></html>";
    }
    
    private String generateQichachaDataPage() {
        return "<html><body><h1>企查查数据正在开发中...</h1><a href='/layer3/'>返回</a></body></html>";
    }
    
    private String generateForumDataPage() {
        return "<html><body><h1>雪球论坛数据正在开发中...</h1><a href='/layer3/'>返回</a></body></html>";
    }
}

            html.append("        </nav>\n");
            html.append("        <div class=\"module-card\">\n");
            html.append("            <div class=\"module-header\">\n");
            html.append("                <h2><i class=\"bi bi-exclamation-triangle\"></i> 第四层模块 - 风险评估</h2>\n");
            html.append("                <p class=\"mb-0\">对第三层的数据进行风险评估</p>\n");
            html.append("            </div>\n");
            html.append("            <div class=\"p-4\">\n");
            html.append("                <div class=\"feature-card\">\n");
            html.append("                    <h4><i class=\"bi bi-chat-quote\"></i> 情感分析</h4>\n");
            html.append("                    <p>分析公司相关的文本数据，提取情感倾向</p>\n");
            html.append("                    <a href=\"/layer4/sentiment-analysis\" class=\"btn btn-custom\">\n");
            html.append("                        <i class=\"bi bi-chat-quote\"></i> 查看情感分析\n");
            html.append("                    </a>\n");
            html.append("                </div>\n");
            html.append("                <div class=\"feature-card\">\n");
            html.append("                    <h4><i class=\"bi bi-shield-exclamation\"></i> 风险评估</h4>\n");
            html.append("                    <p>评估公司的整体风险水平</p>\n");
            html.append("                    <a href=\"/layer4/risk-assessment\" class=\"btn btn-custom\">\n");
            html.append("                        <i class=\"bi bi-shield-exclamation\"></i> 查看风险评估\n");
            html.append("                    </a>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
        
        private String generateSentimentAnalysisPage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>情感分析 - 风险评估</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            html.append("    <style>\n");
            html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); min-height: 100vh; }\n");
            html.append("        .sentiment-container { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }\n");
            html.append("        .sentiment-item { border-left: 4px solid #e74c3c; padding: 15px; margin-bottom: 15px; background: #f8f9fa; border-radius: 8px; }\n");
            html.append("        .sentiment-positive { color: #2ecc71; } .sentiment-negative { color: #e74c3c; } .sentiment-neutral { color: #95a5a6; }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            html.append("<body>\n");
            html.append("    <div class=\"container-fluid\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/layer4/\">第四层模块</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">情感分析</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"sentiment-container\">\n");
            html.append("            <h3><i class=\"bi bi-chat-quote\"></i> 情感分析</h3>\n");
            
            // 添加情感分析项
            String[][] sentiments = {
                {"中国平安", "2022", "积极", "92", "新浪财经"},
                {"贵州茅台", "2022", "积极", "88", "中国证券报"},
                {"腾讯控股", "2022", "积极", "85", "第一财经"},
                {"比亚迪", "2022", "中性", "65", "经济参考报"},
                {"宁德时代", "2022", "积极", "78", "华尔街日报"}
            };
            
            for (String[] sentiment : sentiments) {
                String sentimentClass = "sentiment-positive";
                if (sentiment[2].equals("中性")) sentimentClass = "sentiment-neutral";
                else if (sentiment[2].equals("消极")) sentimentClass = "sentiment-negative";
                
                html.append("            <div class=\"sentiment-item\">\n");
                html.append("                <div class=\"d-flex justify-content-between align-items-start\">\n");
                html.append("                    <div class=\"flex-grow-1\">\n");
                html.append("                        <h5>").append(sentiment[0]).append("</h5>\n");
                html.append("                        <div class=\"d-flex align-items-center gap-3\">\n");
                html.append("                            <span class=\"badge bg-secondary\">").append(sentiment[1]).append("</span>\n");
                html.append("                            <span class=\"").append(sentimentClass).append("\"><i class=\"bi bi-heart-fill\"></i> 情感: ").append(sentiment[2]).append("</span>\n");
                html.append("                            <span class=\"text-primary\"><i class=\"bi bi-graph-up\"></i> 热度: ").append(sentiment[3]).append("</span>\n");
                html.append("                        </div>\n");
                html.append("                    </div>\n");
                html.append("                    <small class=\"text-muted\">").append((int)(Math.random() * 30) + 1).append("分钟前</small>\n");
                html.append("                </div>\n");
                html.append("            </div>\n");
            }
            
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
        
        private String generateRiskAssessmentPage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>风险评估 - 风险评估</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            html.append("    <style>\n");
            html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); min-height: 100vh; }\n");
            html.append("        .risk-container { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }\n");
            html.append("        .risk-item { border-left: 4px solid #e74c3c; padding: 15px; margin-bottom: 15px; background: #f8f9fa; border-radius: 8px; }\n");
            html.append("        .risk-level { color: #e74c3c; }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            html.append("<body>\n");
            html.append("    <div class=\"container-fluid\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/layer4/\">第四层模块</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">风险评估</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"risk-container\">\n");
            html.append("            <h3><i class=\"bi bi-shield-exclamation\"></i> 风险评估</h3>\n");
            
            // 添加风险评估项
            String[][] risks = {
                {"中国平安", "2022", "低", "10.2", "12.3"},
                {"贵州茅台", "2022", "中", "11.5", "13.8"},
                {"腾讯控股", "2022", "高", "12.7", "14.1"},
                {"比亚迪", "2022", "中", "10.5", "11.9"},
                {"宁德时代", "2022", "低", "11.8", "13.2"}
            };
            
            for (String[] risk : risks) {
                html.append("            <div class=\"risk-item\">\n");
                html.append("                <div class=\"d-flex justify-content-between align-items-start\">\n");
                html.append("                    <div class=\"flex-grow-1\">\n");
                html.append("                        <h5>").append(risk[0]).append("</h5>\n");
                html.append("                        <div class=\"d-flex align-items-center gap-3\">\n");
                html.append("                            <span class=\"badge bg-secondary\">").append(risk[1]).append("</span>\n");
                html.append("                            <span class=\"risk-level\"><i class=\"bi bi-shield-exclamation\"></i> 风险等级: ").append(risk[2]).append("</span>\n");
                html.append("                            <span class=\"text-primary\"><i class=\"bi bi-graph-up\"></i> 市值(亿): ").append(risk[3]).append("</span>\n");
                html.append("                            <span class=\"text-primary\"><i class=\"bi bi-graph-up\"></i> 净利润(亿): ").append(risk[4]).append("</span>\n");
                html.append("                        </div>\n");
                html.append("                    </div>\n");
                html.append("                    <small class=\"text-muted\">").append((int)(Math.random() * 30) + 1).append("分钟前</small>\n");
                html.append("                </div>\n");
                html.append("            </div>\n");
            }
            
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
    }
    
    static class Layer5Handler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String path = exchange.getRequestURI().getPath();
            String response;
            
            if (path.contains("factor-weights")) {
                response = generateFactorWeightsPage();
            } else {
                response = generateLayer5HomePage();
            }
            
            sendResponse(exchange, 200, response, "text/html");
        }
        
        private String generateLayer5HomePage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>第五层模块 - 因子权重分析</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            html.append("    <style>\n");
            html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); min-height: 100vh; }\n");
            html.append("        .module-card { background: rgba(255,255,255,0.95); border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 20px; border: 2px solid #3498db; }\n");
            html.append("        .module-header { background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 20px; border-radius: 13px 13px 0 0; }\n");
            html.append("        .feature-card { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 10px; padding: 20px; margin-bottom: 15px; }\n");
            html.append("        .btn-custom { background: linear-gradient(135deg, #3498db, #2980b9); border: none; color: white; }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            html.append("<body>\n");
            html.append("    <div class=\"container-fluid\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">第五层模块</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"module-card\">\n");
            html.append("            <div class=\"module-header\">\n");
            html.append("                <h2><i class=\"bi bi-sliders\"></i> 第五层模块 - 因子权重分析</h2>\n");
            html.append("                <p class=\"mb-0\">对影响因素进行权重分析和优化配置</p>\n");
            html.append("            </div>\n");
            html.append("            <div class=\"p-4\">\n");
            html.append("                <div class=\"feature-card\">\n");
            html.append("                    <h4><i class=\"bi bi-bar-chart\"></i> 对象因子权重表</h4>\n");
            html.append("                    <p>分析各因子对评估对象的影响权重</p>\n");
            html.append("                    <a href=\"/layer5/factor-weights\" class=\"btn btn-custom\">\n");
            html.append("                        <i class=\"bi bi-table\"></i> 查看因子权重表\n");
            html.append("                    </a>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
        
        private String generateFactorWeightsPage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>对象因子权重表 - 因子权重分析</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            html.append("    <style>\n");
            html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); min-height: 100vh; }\n");
            html.append("        .table-container { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }\n");
            html.append("        .table th { background: linear-gradient(135deg, #3498db, #2980b9); color: white; }\n");
            html.append("        .weight-high { color: #2980b9; font-weight: bold; }\n");
            html.append("        .weight-medium { color: #f39c12; font-weight: bold; }\n");
            html.append("        .weight-low { color: #95a5a6; font-weight: bold; }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            html.append("<body>\n");
            html.append("    <div class=\"container-fluid\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/layer5/\">第五层模块</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">对象因子权重表</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"table-container\">\n");
            html.append("            <h3><i class=\"bi bi-bar-chart\"></i> 对象因子权重表</h3>\n");
            html.append("            <div class=\"table-responsive\">\n");
            html.append("                <table class=\"table table-hover\">\n");
            html.append("                    <thead>\n");
            html.append("                        <tr>\n");
            html.append("                            <th>评估对象</th><th>因子名称</th><th>权重值</th><th>影响程度</th><th>趋势分析</th><th>调整建议</th>\n");
            html.append("                        </tr>\n");
            html.append("                    </thead>\n");
            html.append("                    <tbody>\n");
            
            // 添加示例数据
            String[][] factors = {
                {"人工智能行业", "技术创新", "0.35", "高", "上升", "保持权重"},
                {"人工智能行业", "市场需求", "0.25", "高", "稳定", "适度增加"},
                {"人工智能行业", "政策支持", "0.20", "中", "上升", "适当增加"},
                {"人工智能行业", "资本投入", "0.15", "中", "稳定", "维持现状"},
                {"人工智能行业", "人才储备", "0.05", "低", "上升", "显著增加"}
            };
            
            for (String[] factor : factors) {
                String weightClass = "weight-low";
                double weight = Double.parseDouble(factor[2]);
                if (weight >= 0.3) weightClass = "weight-high";
                else if (weight >= 0.15) weightClass = "weight-medium";
                
                html.append("                        <tr>\n");
                html.append("                            <td>").append(factor[0]).append("</td>\n");
                html.append("                            <td>").append(factor[1]).append("</td>\n");
                html.append("                            <td class=\"").append(weightClass).append("\">").append(factor[2]).append("</td>\n");
                html.append("                            <td>").append(factor[3]).append("</td>\n");
                html.append("                            <td>").append(factor[4]).append("</td>\n");
                html.append("                            <td>").append(factor[5]).append("</td>\n");
                html.append("                        </tr>\n");
            }
            
            html.append("                    </tbody>\n");
            html.append("                </table>\n");
            html.append("            </div>\n");
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
    }
    
    static class Layer6Handler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String path = exchange.getRequestURI().getPath();
            String response;
            
            if (path.contains("curve-prediction")) {
                response = generateCurvePredictionPage();
            } else {
                response = generateLayer6HomePage();
            }
            
            sendResponse(exchange, 200, response, "text/html");
        }
        
        private String generateLayer6HomePage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>第六层模块 - 曲线预测分析</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            html.append("    <style>\n");
            html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); min-height: 100vh; }\n");
            html.append("        .module-card { background: rgba(255,255,255,0.95); border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 20px; border: 2px solid #9b59b6; }\n");
            html.append("        .module-header { background: linear-gradient(135deg, #9b59b6, #8e44ad); color: white; padding: 20px; border-radius: 13px 13px 0 0; }\n");
            html.append("        .feature-card { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 10px; padding: 20px; margin-bottom: 15px; }\n");
            html.append("        .btn-custom { background: linear-gradient(135deg, #9b59b6, #8e44ad); border: none; color: white; }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            html.append("<body>\n");
            html.append("    <div class=\"container-fluid\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">第六层模块</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"module-card\">\n");
            html.append("            <div class=\"module-header\">\n");
            html.append("                <h2><i class=\"bi bi-graph-up\"></i> 第六层模块 - 曲线预测分析</h2>\n");
            html.append("                <p class=\"mb-0\">基于历史数据和算法模型进行趋势预测分析</p>\n");
            html.append("            </div>\n");
            html.append("            <div class=\"p-4\">\n");
            html.append("                <div class=\"feature-card\">\n");
            html.append("                    <h4><i class=\"bi bi-graph-up-arrow\"></i> 曲线预测分析</h4>\n");
            html.append("                    <p>通过多种算法模型进行趋势预测和风险预警</p>\n");
            html.append("                    <a href=\"/layer6/curve-prediction\" class=\"btn btn-custom\">\n");
            html.append("                        <i class=\"bi bi-bar-chart\"></i> 查看预测分析\n");
            html.append("                    </a>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
        
        private String generateCurvePredictionPage() {
            StringBuilder html = new StringBuilder();
            html.append("<!DOCTYPE html>\n");
            html.append("<html lang=\"zh-CN\">\n");
            html.append("<head>\n");
            html.append("    <meta charset=\"UTF-8\">\n");
            html.append("    <title>曲线预测分析 - 预测分析模块</title>\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
            html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
            html.append("    <style>\n");
            html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); min-height: 100vh; }\n");
            html.append("        .chart-container { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }\n");
            html.append("        .chart-header { background: linear-gradient(135deg, #9b59b6, #8e44ad); color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; }\n");
            html.append("        .prediction-high { color: #27ae60; font-weight: bold; }\n");
            html.append("        .prediction-medium { color: #f39c12; font-weight: bold; }\n");
            html.append("        .prediction-low { color: #e74c3c; font-weight: bold; }\n");
            html.append("    </style>\n");
            html.append("</head>\n");
            html.append("<body>\n");
            html.append("    <div class=\"container-fluid\">\n");
            html.append("        <nav aria-label=\"breadcrumb\">\n");
            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/layer6/\">第六层模块</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">曲线预测分析</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"chart-container\">\n");
            html.append("            <div class=\"chart-header\">\n");
            html.append("                <h3><i class=\"bi bi-graph-up-arrow\"></i> 曲线预测分析</h3>\n");
            html.append("                <p class=\"mb-0\">基于多维度数据和算法模型的趋势预测</p>\n");
            html.append("            </div>\n");
            html.append("            \n");
            html.append("            <div class=\"row\">\n");
            html.append("                <div class=\"col-md-6\">\n");
            html.append("                    <div class=\"card mb-4\">\n");
            html.append("                        <div class=\"card-header bg-primary text-white\">\n");
            html.append("                            <h5><i class=\"bi bi-bank\"></i> 行业趋势预测</h5>\n");
            html.append("                        </div>\n");
            html.append("                        <div class=\"card-body\">\n");
            html.append("                            <div class=\"table-responsive\">\n");
            html.append("                                <table class=\"table table-hover\">\n");
            html.append("                                    <thead>\n");
            html.append("                                        <tr>\n");
            html.append("                                            <th>行业名称</th><th>预测趋势</th><th>置信度</th><th>时间范围</th>\n");
            html.append("                                        </tr>\n");
            html.append("                                    </thead>\n");
            html.append("                                    <tbody>\n");
        
        // 添加行业趋势预测数据
        String[][] industryPredictions = {
            {"人工智能", "持续增长", "92%", "未来6个月"},
            {"新能源汽车", "稳定增长", "88%", "未来6个月"},
            {"生物医药", "快速增长", "85%", "未来6个月"},
            {"房地产", "缓慢下降", "75%", "未来6个月"},
            {"消费电子", "稳定波动", "80%", "未来6个月"}
        };
        
        for (String[] prediction : industryPredictions) {
            String predictionClass = "prediction-high";
            int confidence = Integer.parseInt(prediction[2].replace("%", ""));
            if (confidence < 80) predictionClass = "prediction-medium";
            if (confidence < 70) predictionClass = "prediction-low";
            
            html.append("                                        <tr>\n");
            html.append("                                            <td>").append(prediction[0]).append("</td>\n");
            html.append("                                            <td class=\"").append(predictionClass).append("\">").append(prediction[1]).append("</td>\n");
            html.append("                                            <td>").append(prediction[2]).append("</td>\n");
            html.append("                                            <td>").append(prediction[3]).append("</td>\n");
            html.append("                                        </tr>\n");
        }
        
        html.append("                                    </tbody>\n");
        html.append("                                </table>\n");
        html.append("                            </div>\n");
        html.append("                        </div>\n");
        html.append("                    </div>\n");
        html.append("                </div>\n");
        html.append("                \n");
        html.append("                <div class=\"col-md-6\">\n");
        html.append("                    <div class=\"card mb-4\">\n");
        html.append("                        <div class=\"card-header bg-success text-white\">\n");
        html.append("                            <h5><i class=\"bi bi-building\"></i> 公司表现预测</h5>\n");
        html.append("                        </div>\n");
        html.append("                        <div class=\"card-body\">\n");
        html.append("                            <div class=\"table-responsive\">\n");
        html.append("                                <table class=\"table table-hover\">\n");
        html.append("                                    <thead>\n");
        html.append("                                        <tr>\n");
        html.append("                                            <th>公司名称</th><th>预测表现</th><th>置信度</th><th>风险等级</th>\n");
        html.append("                                        </tr>\n");
        html.append("                                    </thead>\n");
        html.append("                                    <tbody>\n");
        
        // 添加公司表现预测数据
        String[][] companyPredictions = {
            {"中国平安", "稳定增长", "95%", "低风险"},
            {"贵州茅台", "持续增长", "92%", "低风险"},
            {"腾讯控股", "稳定增长", "88%", "中等风险"},
            {"比亚迪", "快速增长", "85%", "中等风险"},
            {"宁德时代", "稳定增长", "82%", "中等风险"}
        };
        
        for (String[] prediction : companyPredictions) {
            String predictionClass = "prediction-high";
            int confidence = Integer.parseInt(prediction[2].replace("%", ""));
            if (confidence < 85) predictionClass = "prediction-medium";
            if (confidence < 80) predictionClass = "prediction-low";
            
            html.append("                                        <tr>\n");
            html.append("                                            <td>").append(prediction[0]).append("</td>\n");
            html.append("                                            <td class=\"").append(predictionClass).append("\">").append(prediction[1]).append("</td>\n");
            html.append("                                            <td>").append(prediction[2]).append("</td>\n");
            html.append("                                            <td>").append(prediction[3]).append("</td>\n");
            html.append("                                        </tr>\n");
        }
        
        html.append("                                    </tbody>\n");
        html.append("                                </table>\n");
        html.append("                            </div>\n");
        html.append("                        </div>\n");
        html.append("                    </div>\n");
        html.append("                </div>\n");
        html.append("            </div>\n");
        html.append("            \n");
        html.append("            <div class=\"card\">\n");
        html.append("                <div class=\"card-header bg-info text-white\">\n");
        html.append("                    <h5><i class=\"bi bi-exclamation-triangle\"></i> 风险预警</h5>\n");
        html.append("                </div>\n");
        html.append("                <div class=\"card-body\">\n");
        html.append("                    <div class=\"alert alert-warning\">\n");
        html.append("                        <h6><i class=\"bi bi-lightning\"></i> 高风险预警</h6>\n");
        html.append("                        <p>以下领域可能存在较高风险，请重点关注：</p>\n");
        html.append("                        <ul>\n");
        html.append("                            <li>房地产行业政策调整风险</li>\n");
        html.append("                            <li>部分消费电子企业供应链风险</li>\n");
        html.append("                            <li>国际汇率波动对出口企业的影响</li>\n");
        html.append("                        </ul>\n");
        html.append("                    </div>\n");
        html.append("                    <div class=\"alert alert-info\">\n");
        html.append("                        <h6><i class=\"bi bi-stars\"></i> 投资机会</h6>\n");
        html.append("                        <p>以下领域存在较好投资机会：</p>\n");
        html.append("                        <ul>\n");
        html.append("                            <li>人工智能与新能源结合领域</li>\n");
        html.append("                            <li>生物医药创新研发企业</li>\n");
        html.append("                            <li>高端制造与自动化领域</li>\n");
        html.append("                        </ul>\n");
        html.append("                    </div>\n");
        html.append("                </div>\n");
        html.append("            </div>\n");
        html.append("        </div>\n");
        html.append("    </div>\n");
        html.append("</body>\n");
        html.append("</html>\n");
        return html.toString();
    }
}

            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
    }
    
}

            html.append("            <ol class=\"breadcrumb\">\n");
            html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
            html.append("                <li class=\"breadcrumb-item active\">第三层模块</li>\n");
            html.append("            </ol>\n");
            html.append("        </nav>\n");
            html.append("        <div class=\"module-card\">\n");
            html.append("            <div class=\"module-header\">\n");
            html.append("                <h2><i class=\"bi bi-search\"></i> 第三层模块 - 深度数据挖掘</h2>\n");
            html.append("                <p class=\"mb-0\">基于第二层加工数据，进行深度挖掘和专业分析</p>\n");
            html.append("            </div>\n");
            html.append("            <div class=\"p-4\">\n");
            html.append("                <div class=\"feature-grid\">\n");
            
            // 税银报告模块
            html.append("                    <div class=\"feature-card\">\n");
            html.append("                        <h4><i class=\"bi bi-file-earmark-text text-primary\"></i> 税银报告</h4>\n");
            html.append("                        <p>整合税务和银行数据，分析企业财务健康状况</p>\n");
            html.append("                        <a href=\"/layer3/tax-bank-report\" class=\"btn btn-custom\">\n");
            html.append("                            <i class=\"bi bi-graph-up\"></i> 查看税银报告\n");
            html.append("                        </a>\n");
            html.append("                    </div>\n");
            
            // 财务三表模块
            html.append("                    <div class=\"feature-card\">\n");
            html.append("                        <h4><i class=\"bi bi-table text-success\"></i> 财务三表</h4>\n");
            html.append("                        <p>资产负债表、利润表、现金流量表的深度分析</p>\n");
            html.append("                        <a href=\"/layer3/financial-statements\" class=\"btn btn-custom\">\n");
            html.append("                            <i class=\"bi bi-calculator\"></i> 查看财务三表\n");
            html.append("                        </a>\n");
            html.append("                    </div>\n");
            
            // 企查查数据模块
            html.append("                    <div class=\"feature-card\">\n");
            html.append("                        <h4><i class=\"bi bi-building text-info\"></i> 企查查数据</h4>\n");
            html.append("                        <p>企业工商信息、法律风险、关联关系等数据</p>\n");
            html.append("                        <a href=\"/layer3/qichacha-data\" class=\"btn btn-custom\">\n");
            html.append("                            <i class=\"bi bi-search\"></i> 查看企查查数据\n");
            html.append("                        </a>\n");
            html.append("                    </div>\n");
            
            // 雪球论坛数据模块
            html.append("                    <div class=\"feature-card\">\n");
            html.append("                        <h4><i class=\"bi bi-chat-dots text-warning\"></i> 雪球论坛数据</h4>\n");
            html.append("                        <p>投资者情绪、市场舆情、股价预期等信息</p>\n");
            html.append("                        <a href=\"/layer3/forum-data\" class=\"btn btn-custom\">\n");
            html.append("                            <i class=\"bi bi-people\"></i> 查看论坛数据\n");
            html.append("                        </a>\n");
            html.append("                    </div>\n");
            
            html.append("                </div>\n");
            html.append("            </div>\n");
            html.append("        </div>\n");
            html.append("    </div>\n");
            html.append("</body>\n");
            html.append("</html>\n");
            return html.toString();
        }
    
    private String generateTaxBankReportPage() {
        StringBuilder html = new StringBuilder();
        html.append("<!DOCTYPE html>\n");
        html.append("<html lang=\"zh-CN\">\n");
        html.append("<head>\n");
        html.append("    <meta charset=\"UTF-8\">\n");
        html.append("    <title>税银报告 - 深度数据挖掘</title>\n");
        html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
        html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
        html.append("    <style>\n");
        html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); min-height: 100vh; }\n");
        html.append("        .report-container { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }\n");
        html.append("        .metric-card { background: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin-bottom: 15px; border-radius: 8px; }\n");
        html.append("        .risk-high { border-left-color: #e74c3c; } .risk-medium { border-left-color: #f39c12; } .risk-low { border-left-color: #2ecc71; }\n");
        html.append("    </style>\n");
        html.append("</head>\n");
        html.append("<body>\n");
        html.append("    <div class=\"container-fluid\">\n");
        html.append("        <nav aria-label=\"breadcrumb\">\n");
        html.append("            <ol class=\"breadcrumb\">\n");
        html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
        html.append("                <li class=\"breadcrumb-item\"><a href=\"/layer3/\">第三层模块</a></li>\n");
        html.append("                <li class=\"breadcrumb-item active\">税银报告</li>\n");
        html.append("            </ol>\n");
        html.append("        </nav>\n");
        html.append("        <div class=\"report-container\">\n");
        html.append("            <h3><i class=\"bi bi-file-earmark-text\"></i> 税银报告分析</h3>\n");
        
        // 税银数据示例
        String[][] taxData = {
            {"中国平安", "税收健康", "AAA", "低风险", "98.5%"},
            {"贵州茅台", "税收健康", "AA+", "低风险", "97.2%"},
            {"腾讯控股", "税收健康", "AA", "低风险", "95.8%"},
            {"比亚迪", "税收正常", "A+", "中风险", "89.3%"},
            {"宁德时代", "税收健康", "AA-", "低风险", "93.7%"}
        };
        
        for (String[] data : taxData) {
            String riskClass = data[3].contains("低") ? "risk-low" : data[3].contains("中") ? "risk-medium" : "risk-high";
            html.append("            <div class=\"metric-card ").append(riskClass).append("\">\n");
            html.append("                <div class=\"row align-items-center\">\n");
            html.append("                    <div class=\"col-md-3\"><strong>").append(data[0]).append("</strong></div>\n");
            html.append("                    <div class=\"col-md-2\"><span class=\"badge bg-success\">").append(data[1]).append("</span></div>\n");
            html.append("                    <div class=\"col-md-2\"><span class=\"badge bg-primary\">信用评级: ").append(data[2]).append("</span></div>\n");
            html.append("                    <div class=\"col-md-2\"><span class=\"badge bg-warning\">").append(data[3]).append("</span></div>\n");
            html.append("                    <div class=\"col-md-3\"><span class=\"text-success\">合规率: ").append(data[4]).append("</span></div>\n");
            html.append("                </div>\n");
            html.append("            </div>\n");
        }
        
        html.append("        </div>\n");
        html.append("    </div>\n");
        html.append("</body>\n");
        html.append("</html>\n");
        return html.toString();
    }
    
    private String generateFinancialStatementsPage() {
        return "<html><body><h1>财务三表正在开发中...</h1><a href='/layer3/'>返回</a></body></html>";
    }
    
    private String generateQichachaDataPage() {
        return "<html><body><h1>企查查数据正在开发中...</h1><a href='/layer3/'>返回</a></body></html>";
    }
    
    private String generateForumDataPage() {
        return "<html><body><h1>雪球论坛数据正在开发中...</h1><a href='/layer3/'>返回</a></body></html>";
    }
}

static class Layer4Handler implements HttpHandler {
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        String response;
        
        if (path.contains("industry-scores")) {
            response = generateIndustryScoresPage();
        } else if (path.contains("company-scores")) {
            response = generateCompanyScoresPage();
        } else if (path.contains("industry-company-scores")) {
            response = generateIndustryCompanyScoresPage();
        } else {
            response = generateLayer4HomePage();
        }
        
        sendResponse(exchange, 200, response, "text/html");
    }
    
    private String generateLayer4HomePage() {
        StringBuilder html = new StringBuilder();
        html.append("<!DOCTYPE html>\n");
        html.append("<html lang=\"zh-CN\">\n");
        html.append("<head>\n");
        html.append("    <meta charset=\"UTF-8\">\n");
        html.append("    <title>第四层模块 - 智能评分算法</title>\n");
        html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
        html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
        html.append("    <style>\n");
        html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); min-height: 100vh; }\n");
        html.append("        .module-card { background: rgba(255,255,255,0.95); border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 20px; border: 2px solid #2ecc71; }\n");
        html.append("        .module-header { background: linear-gradient(135deg, #2ecc71, #27ae60); color: white; padding: 20px; border-radius: 13px 13px 0 0; }\n");
        html.append("        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }\n");
        html.append("        .feature-card { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 10px; padding: 20px; transition: all 0.3s ease; }\n");
        html.append("        .feature-card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }\n");
        html.append("        .btn-custom { background: linear-gradient(135deg, #2ecc71, #27ae60); border: none; color: white; }\n");
        html.append("    </style>\n");
        html.append("</head>\n");
        html.append("<body>\n");
        html.append("    <div class=\"container-fluid\">\n");
        html.append("        <nav aria-label=\"breadcrumb\">\n");
        html.append("            <ol class=\"breadcrumb\">\n");
        html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
        html.append("                <li class=\"breadcrumb-item active\">第四层模块</li>\n");
        html.append("            </ol>\n");
        html.append("        </nav>\n");
        html.append("        <div class=\"module-card\">\n");
        html.append("            <div class=\"module-header\">\n");
        html.append("                <h2><i class=\"bi bi-calculator\"></i> 第四层模块 - 智能评分算法</h2>\n");
        html.append("                <p class=\"mb-0\">基于第三层挖掘数据，进行智能评分和风险评估</p>\n");
        html.append("            </div>\n");
        html.append("            <div class=\"p-4\">\n");
        html.append("                <div class=\"feature-grid\">\n");
        
        // 行业分值表模块
        html.append("                    <div class=\"feature-card\">\n");
        html.append("                        <h4><i class=\"bi bi-building text-primary\"></i> 行业分值表</h4>\n");
        html.append("                        <p>对各行业进行综合评分和风险评估</p>\n");
        html.append("                        <a href=\"/layer4/industry-scores\" class=\"btn btn-custom\">\n");
        html.append("                            <i class=\"bi bi-graph-up\"></i> 查看行业分值表\n");
        html.append("                        </a>\n");
        html.append("                    </div>\n");
        
        // 公司分值表模块
        html.append("                    <div class=\"feature-card\">\n");
        html.append("                        <h4><i class=\"bi bi-building text-success\"></i> 公司分值表</h4>\n");
        html.append("                        <p>对企业进行多维度评分和风险评估</p>\n");
        html.append("                        <a href=\"/layer4/company-scores\" class=\"btn btn-custom\">\n");
        html.append("                            <i class=\"bi bi-graph-up\"></i> 查看公司分值表\n");
        html.append("                        </a>\n");
        html.append("                    </div>\n");
        
        // 行业+公司分值表模块
        html.append("                    <div class=\"feature-card\">\n");
        html.append("                        <h4><i class=\"bi bi-building text-info\"></i> 行业+公司分值表</h4>\n");
        html.append("                        <p>综合行业和企业数据进行评分对比</p>\n");
        html.append("                        <a href=\"/layer4/industry-company-scores\" class=\"btn btn-custom\">\n");
        html.append("                            <i class=\"bi bi-graph-up\"></i> 查看综合分值表\n");
        html.append("                        </a>\n");
        html.append("                    </div>\n");
        
        html.append("                </div>\n");
        html.append("            </div>\n");
        html.append("        </div>\n");
        html.append("    </div>\n");
        html.append("</body>\n");
        html.append("</html>\n");
        return html.toString();
    }
    
    private String generateIndustryScoresPage() {
        return "<html><body><h1>行业分值表正在开发中...</h1><a href='/layer4/'>返回</a></body></html>";
    }
    
    private String generateCompanyScoresPage() {
        return "<html><body><h1>公司分值表正在开发中...</h1><a href='/layer4/'>返回</a></body></html>";
    }
    
    private String generateIndustryCompanyScoresPage() {
        return "<html><body><h1>行业+公司分值表正在开发中...</h1><a href='/layer4/'>返回</a></body></html>";
    }
}

static class Layer5Handler implements HttpHandler {
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        String response;
        
        if (path.contains("factor-weights")) {
            response = generateFactorWeightsPage();
        } else {
            response = generateLayer5HomePage();
        }
        
        sendResponse(exchange, 200, response, "text/html");
    }
    
    private String generateLayer5HomePage() {
        StringBuilder html = new StringBuilder();
        html.append("<!DOCTYPE html>\n");
        html.append("<html lang=\"zh-CN\">\n");
        html.append("<head>\n");
        html.append("    <meta charset=\"UTF-8\">\n");
        html.append("    <title>第五层模块 - 因子权重分析</title>\n");
        html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
        html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
        html.append("    <style>\n");
        html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); min-height: 100vh; }\n");
        html.append("        .module-card { background: rgba(255,255,255,0.95); border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 20px; border: 2px solid #3498db; }\n");
        html.append("        .module-header { background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 20px; border-radius: 13px 13px 0 0; }\n");
        html.append("        .feature-card { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 10px; padding: 20px; margin-bottom: 20px; }\n");
        html.append("        .btn-custom { background: linear-gradient(135deg, #3498db, #2980b9); border: none; color: white; }\n");
        html.append("        .weight-bar { height: 20px; border-radius: 10px; margin: 10px 0; }\n");
        html.append("    </style>\n");
        html.append("</head>\n");
        html.append("<body>\n");
        html.append("    <div class=\"container-fluid\">\n");
        html.append("        <nav aria-label=\"breadcrumb\">\n");
        html.append("            <ol class=\"breadcrumb\">\n");
        html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
        html.append("                <li class=\"breadcrumb-item active\">第五层模块</li>\n");
        html.append("            </ol>\n");
        html.append("        </nav>\n");
        html.append("        <div class=\"module-card\">\n");
        html.append("            <div class=\"module-header\">\n");
        html.append("                <h2><i class=\"bi bi-sliders\"></i> 第五层模块 - 因子权重分析</h2>\n");
        html.append("                <p class=\"mb-0\">基于第四层评分结果，进行因子权重分析和优化</p>\n");
        html.append("            </div>\n");
        html.append("            <div class=\"p-4\">\n");
        html.append("                <div class=\"feature-card\">\n");
        html.append("                    <h4><i class=\"bi bi-bar-chart text-primary\"></i> 对象因子权重表</h4>\n");
        html.append("                    <p>分析各因子对最终评分的贡献度和权重分配</p>\n");
        html.append("                    <a href=\"/layer5/factor-weights\" class=\"btn btn-custom\">\n");
        html.append("                        <i class=\"bi bi-graph-up\"></i> 查看因子权重表\n");
        html.append("                    </a>\n");
        html.append("                </div>\n");
        html.append("            </div>\n");
        html.append("        </div>\n");
        html.append("    </div>\n");
        html.append("</body>\n");
        html.append("</html>\n");
        return html.toString();
    }
    
    private String generateFactorWeightsPage() {
        StringBuilder html = new StringBuilder();
        html.append("<!DOCTYPE html>\n");
        html.append("<html lang=\"zh-CN\">\n");
        html.append("<head>\n");
        html.append("    <meta charset=\"UTF-8\">\n");
        html.append("    <title>因子权重表 - 因子权重分析</title>\n");
        html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n");
        html.append("    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css\" rel=\"stylesheet\">\n");
        html.append("    <style>\n");
        html.append("        body { font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); min-height: 100vh; }\n");
        html.append("        .weights-container { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }\n");
        html.append("        .weight-item { margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 10px; }\n");
        html.append("        .weight-bar { height: 20px; border-radius: 10px; margin: 10px 0; }\n");
        html.append("    </style>\n");
        html.append("</head>\n");
        html.append("<body>\n");
        html.append("    <div class=\"container-fluid\">\n");
        html.append("        <nav aria-label=\"breadcrumb\">\n");
        html.append("            <ol class=\"breadcrumb\">\n");
        html.append("                <li class=\"breadcrumb-item\"><a href=\"/\">首页</a></li>\n");
        html.append("                <li class=\"breadcrumb-item\"><a href=\"/layer5/\">第五层模块</a></li>\n");
        html.append("                <li class=\"breadcrumb-item active\">因子权重表</li>\n");
        html.append("            </ol>\n");
        html.append("        </nav>\n");
        html.append("        <div class=\"weights-container\">\n");
        html.append("            <h3><i class=\"bi bi-bar-chart\"></i> 因子权重分析表</h3>\n");
        
        // 因子权重数据示例
        String[][] factors = {
            {"财务健康度", "0.25", "#e74c3c"},
            {"市场表现", "0.20", "#f39c12"},
            {"行业前景", "0.15", "#f1c40f"},
            {"创新能力", "0.15", "#2ecc71"},
            {"管理质量", "0.10", "#3498db"},
            {"合规风险", "0.10", "#9b59b6"},
            {"社会责任", "0.05", "#1abc9c"}
        };
        
        for (String[] factor : factors) {
            html.append("            <div class=\"weight-item\">\n");
            html.append("                <div class=\"d-flex justify-content-between\">\n");
            html.append("                    <strong>").append(factor[0]).append("</strong>\n");
            html.append("                    <span class=\"badge bg-primary\">").append((Double.parseDouble(factor[1]) * 100)).append("%</span>\n");
            html.append("                </div>\n");
            html.append("                <div class=\"weight-bar\" style=\"background: linear-gradient(90deg, ").append(factor[2]).append(" ").append((Double.parseDouble(factor[1]) * 100)).append("%, #ecf0f1 ").append((Double.parseDouble(factor[1]) * 100)).append("%);\"></div>\n");
            html.append("            </div>\n");
        }
        
        html.append("        </div>\n");
        html.append("    </div>\n");
        html.append("</body>\n");
        html.append("</html>\n");
        return html.toString();
    }
}

static class Layer6Handler extends LayerHandler {
    public Layer6Handler() { super("第六层模块 - 曲线预测分析"); }
}

/**
 * API处理器
 */
static class ApiHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        String jsonResponse = 
            "{\n" +
            "    \"status\": \"success\",\n" +
            "    \"message\": \"API正在开发中\",\n" +
            "    \"data\": [],\n" +
            "    \"timestamp\": " + System.currentTimeMillis() + "\n" +
            "}";
        
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        
        byte[] responseBytes = jsonResponse.getBytes(CHARSET);
        exchange.sendResponseHeaders(200, responseBytes.length);
        
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}

/**
 * 发送HTTP响应的工具方法
 */
static void sendResponse(HttpExchange exchange, int statusCode, String response, String contentType) throws IOException {
    exchange.getResponseHeaders().set("Content-Type", contentType + "; charset=" + CHARSET);
    exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
    
    byte[] responseBytes = response.getBytes(CHARSET);
    exchange.sendResponseHeaders(statusCode, responseBytes.length);
    
    try (OutputStream os = exchange.getResponseBody()) {
        os.write(responseBytes);
    }
}

