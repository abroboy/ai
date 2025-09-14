package com.tencentindex.service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * 腾讯济安指数数据服务
 * 负责拉取和管理腾讯济安金融指数数据
 */
public class TencentIndexDataService {
    
    private static final List<Map<String, Object>> indexData = new ArrayList<>();
    private static final Map<String, Object> dataStatistics = new HashMap<>();
    private static LocalDateTime lastUpdateTime;
    
    public static void initialize() {
        System.out.println("初始化腾讯济安指数数据服务...");
        refreshData();
        System.out.println("腾讯济安指数数据服务初始化完成");
    }
    
    public static void refreshData() {
        System.out.println("开始刷新腾讯济安指数数据: " + LocalDateTime.now());
        
        indexData.clear();
        
        // 生成腾讯济安指数数据
        generateJianIndexData();
        
        // 生成金融科技指数数据
        generateFintechIndexData();
        
        // 生成创新指数数据
        generateInnovationIndexData();
        
        // 生成数字经济指数数据
        generateDigitalIndexData();
        
        // 更新统计数据
        updateDataStatistics();
        
        lastUpdateTime = LocalDateTime.now();
        System.out.println("腾讯济安指数数据刷新完成，共获取 " + indexData.size() + " 个指数数据");
    }
    
    private static void generateJianIndexData() {
        Random random = new Random();
        
        String[] jianIndices = {"济安指数", "济安金融指数", "济安银行指数", "济安保险指数"};
        
        for (String indexName : jianIndices) {
            Map<String, Object> data = new HashMap<>();
            data.put("indexCode", "JIAN_" + indexName.hashCode());
            data.put("indexName", indexName);
            data.put("currentValue", 3000 + random.nextDouble() * 500);
            data.put("changePercent", -2.0 + random.nextDouble() * 4.0);
            data.put("volume", 1000000 + random.nextLong() % 9000000);
            data.put("marketCap", 500000000000L + random.nextLong() % 1000000000000L);
            data.put("lastUpdated", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            indexData.add(data);
        }
    }
    
    private static void generateFintechIndexData() {
        Random random = new Random();
        
        String[] fintechIndices = {"金融科技指数", "支付科技指数", "区块链指数", "数字货币指数"};
        
        for (String indexName : fintechIndices) {
            Map<String, Object> data = new HashMap<>();
            data.put("indexCode", "FINTECH_" + indexName.hashCode());
            data.put("indexName", indexName);
            data.put("currentValue", 1800 + random.nextDouble() * 300);
            data.put("changePercent", -1.5 + random.nextDouble() * 3.0);
            data.put("volume", 800000 + random.nextLong() % 7000000);
            data.put("marketCap", 300000000000L + random.nextLong() % 800000000000L);
            data.put("lastUpdated", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            indexData.add(data);
        }
    }
    
    private static void generateInnovationIndexData() {
        Random random = new Random();
        
        String[] innovationIndices = {"创新指数", "科技创新指数", "金融创新指数", "产品创新指数"};
        
        for (String indexName : innovationIndices) {
            Map<String, Object> data = new HashMap<>();
            data.put("indexCode", "INNOV_" + indexName.hashCode());
            data.put("indexName", indexName);
            data.put("currentValue", 2200 + random.nextDouble() * 400);
            data.put("changePercent", -1.8 + random.nextDouble() * 3.6);
            data.put("volume", 600000 + random.nextLong() % 5000000);
            data.put("marketCap", 200000000000L + random.nextLong() % 600000000000L);
            data.put("lastUpdated", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            indexData.add(data);
        }
    }
    
    private static void generateDigitalIndexData() {
        Random random = new Random();
        
        String[] digitalIndices = {"数字经济指数", "数字金融指数", "数字银行指数", "数字支付指数"};
        
        for (String indexName : digitalIndices) {
            Map<String, Object> data = new HashMap<>();
            data.put("indexCode", "DIGITAL_" + indexName.hashCode());
            data.put("indexName", indexName);
            data.put("currentValue", 2500 + random.nextDouble() * 350);
            data.put("changePercent", -2.2 + random.nextDouble() * 4.4);
            data.put("volume", 700000 + random.nextLong() % 6000000);
            data.put("marketCap", 250000000000L + random.nextLong() % 700000000000L);
            data.put("lastUpdated", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            indexData.add(data);
        }
    }
    
    private static void updateDataStatistics() {
        int totalIndices = indexData.size();
        double jianIndexValue = 0;
        double fintechIndexValue = 0;
        int positiveCount = 0;
        int negativeCount = 0;
        
        for (Map<String, Object> data : indexData) {
            String indexName = (String) data.get("indexName");
            double currentValue = (Double) data.get("currentValue");
            double changePercent = (Double) data.get("changePercent");
            
            if (indexName.contains("济安")) {
                jianIndexValue = currentValue;
            } else if (indexName.contains("金融科技")) {
                fintechIndexValue = currentValue;
            }
            
            if (changePercent > 0) {
                positiveCount++;
            } else {
                negativeCount++;
            }
        }
        
        String overallPerformance;
        if (positiveCount > negativeCount) {
            overallPerformance = "上涨";
        } else if (positiveCount < negativeCount) {
            overallPerformance = "下跌";
        } else {
            overallPerformance = "平稳";
        }
        
        dataStatistics.put("total_indices", totalIndices);
        dataStatistics.put("jian_index_value", String.format("%.2f", jianIndexValue));
        dataStatistics.put("fintech_index_value", String.format("%.2f", fintechIndexValue));
        dataStatistics.put("index_performance", overallPerformance);
        dataStatistics.put("last_update", 
            lastUpdateTime != null ? lastUpdateTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")) : 
            LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
    }
    
    public static List<Map<String, Object>> getIndexData() {
        return new ArrayList<>(indexData);
    }
    
    public static Map<String, Object> getDataStatistics() {
        return new HashMap<>(dataStatistics);
    }
}