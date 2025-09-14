package com.globalcapitalflow.service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * 全球资金流向数据服务
 * 负责拉取和管理全球各主要市场的资金流向数据
 */
public class GlobalCapitalFlowDataService {
    
    private static final List<Map<String, Object>> globalFlowData = new ArrayList<>();
    private static final Map<String, Object> dataStatistics = new HashMap<>();
    private static LocalDateTime lastUpdateTime;
    
    public static void initialize() {
        System.out.println("初始化全球资金流向数据服务...");
        refreshData();
        System.out.println("全球资金流向数据服务初始化完成");
    }
    
    public static void refreshData() {
        System.out.println("开始刷新全球资金流向数据: " + LocalDateTime.now());
        
        globalFlowData.clear();
        
        // 生成美股市场数据
        generateUsMarketData();
        
        // 生成欧洲市场数据
        generateEuropeMarketData();
        
        // 生成亚太市场数据
        generateAsiaMarketData();
        
        // 生成新兴市场数据
        generateEmergingMarketData();
        
        // 更新统计数据
        updateDataStatistics();
        
        lastUpdateTime = LocalDateTime.now();
        System.out.println("全球资金流向数据刷新完成，共获取 " + globalFlowData.size() + " 个市场数据");
    }
    
    private static void generateUsMarketData() {
        Random random = new Random();
        
        // 生成美股主要市场数据
        String[] usMarkets = {"纳斯达克", "纽交所", "标普500", "道琼斯"};
        
        for (String market : usMarkets) {
            Map<String, Object> data = new HashMap<>();
            data.put("region", "美国");
            data.put("market", market);
            data.put("inflow", 50000000 + random.nextDouble() * 100000000);
            data.put("outflow", 30000000 + random.nextDouble() * 80000000);
            data.put("netFlow", (Double)data.get("inflow") - (Double)data.get("outflow"));
            data.put("currency", "USD");
            data.put("lastUpdated", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            globalFlowData.add(data);
        }
    }
    
    private static void generateEuropeMarketData() {
        Random random = new Random();
        
        // 生成欧洲主要市场数据
        String[] europeMarkets = {"伦敦交易所", "法兰克福交易所", "巴黎交易所", "阿姆斯特丹交易所"};
        
        for (String market : europeMarkets) {
            Map<String, Object> data = new HashMap<>();
            data.put("region", "欧洲");
            data.put("market", market);
            data.put("inflow", 30000000 + random.nextDouble() * 70000000);
            data.put("outflow", 25000000 + random.nextDouble() * 60000000);
            data.put("netFlow", (Double)data.get("inflow") - (Double)data.get("outflow"));
            data.put("currency", "EUR");
            data.put("lastUpdated", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            globalFlowData.add(data);
        }
    }
    
    private static void generateAsiaMarketData() {
        Random random = new Random();
        
        // 生成亚太主要市场数据
        String[] asiaMarkets = {"东京交易所", "香港交易所", "新加坡交易所", "悉尼交易所"};
        
        for (String market : asiaMarkets) {
            Map<String, Object> data = new HashMap<>();
            data.put("region", "亚太");
            data.put("market", market);
            data.put("inflow", 40000000 + random.nextDouble() * 80000000);
            data.put("outflow", 35000000 + random.nextDouble() * 70000000);
            data.put("netFlow", (Double)data.get("inflow") - (Double)data.get("outflow"));
            data.put("currency", "JPY");
            data.put("lastUpdated", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            globalFlowData.add(data);
        }
    }
    
    private static void generateEmergingMarketData() {
        Random random = new Random();
        
        // 生成新兴市场数据
        String[] emergingMarkets = {"上海交易所", "深圳交易所", "孟买交易所", "圣保罗交易所"};
        
        for (String market : emergingMarkets) {
            Map<String, Object> data = new HashMap<>();
            data.put("region", "新兴市场");
            data.put("market", market);
            data.put("inflow", 20000000 + random.nextDouble() * 50000000);
            data.put("outflow", 18000000 + random.nextDouble() * 45000000);
            data.put("netFlow", (Double)data.get("inflow") - (Double)data.get("outflow"));
            data.put("currency", "CNY");
            data.put("lastUpdated", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            globalFlowData.add(data);
        }
    }
    
    private static void updateDataStatistics() {
        double totalUsFlow = 0;
        double totalEuropeFlow = 0;
        double totalAsiaFlow = 0;
        int marketCount = globalFlowData.size();
        
        for (Map<String, Object> data : globalFlowData) {
            String region = (String) data.get("region");
            double netFlow = (Double) data.get("netFlow");
            
            switch (region) {
                case "美国":
                    totalUsFlow += netFlow;
                    break;
                case "欧洲":
                    totalEuropeFlow += netFlow;
                    break;
                case "亚太":
                    totalAsiaFlow += netFlow;
                    break;
            }
        }
        
        dataStatistics.put("total_markets", marketCount);
        dataStatistics.put("us_market_flow", String.format("%.1fM", totalUsFlow / 1000000));
        dataStatistics.put("europe_market_flow", String.format("%.1fM", totalEuropeFlow / 1000000));
        dataStatistics.put("asia_market_flow", String.format("%.1fM", totalAsiaFlow / 1000000));
        dataStatistics.put("last_update", 
            lastUpdateTime != null ? lastUpdateTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")) : 
            LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
    }
    
    public static List<Map<String, Object>> getGlobalFlowData() {
        return new ArrayList<>(globalFlowData);
    }
    
    public static Map<String, Object> getDataStatistics() {
        return new HashMap<>(dataStatistics);
    }
}