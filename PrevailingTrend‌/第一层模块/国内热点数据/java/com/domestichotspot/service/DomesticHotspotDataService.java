package com.domestichotspot.service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * 国内热点数据服务
 * 负责拉取和管理国内财经热点、政策动态等信息
 */
public class DomesticHotspotDataService {
    
    private static final List<Map<String, Object>> hotspotData = new ArrayList<>();
    private static final Map<String, Object> dataStatistics = new HashMap<>();
    private static LocalDateTime lastUpdateTime;
    
    public static void initialize() {
        System.out.println("初始化国内热点数据服务...");
        refreshData();
        System.out.println("国内热点数据服务初始化完成");
    }
    
    public static void refreshData() {
        System.out.println("开始刷新国内热点数据: " + LocalDateTime.now());
        
        hotspotData.clear();
        
        // 生成财经热点数据
        generateFinanceHotspots();
        
        // 生成政策动态数据
        generatePolicyHotspots();
        
        // 生成市场新闻数据
        generateMarketNews();
        
        // 生成行业资讯数据
        generateIndustryNews();
        
        // 更新统计数据
        updateDataStatistics();
        
        lastUpdateTime = LocalDateTime.now();
        System.out.println("国内热点数据刷新完成，共获取 " + hotspotData.size() + " 条热点资讯");
    }
    
    private static void generateFinanceHotspots() {
        Random random = new Random();
        
        String[] financeTopics = {
            "央行货币政策调整分析", "A股市场最新动向", "人民币汇率走势解读", 
            "银行业净息差变化", "券商业绩分析报告", "保险行业发展趋势"
        };
        
        String[] sources = {"新华财经", "中国证券报", "上海证券报", "经济参考报"};
        String[] sentiments = {"积极", "中性", "消极"};
        
        for (int i = 0; i < 50; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "FIN_" + String.format("%04d", i + 1));
            data.put("title", financeTopics[random.nextInt(financeTopics.length)] + " - " + (i + 1));
            data.put("category", "财经热点");
            data.put("content", "这是一条关于" + financeTopics[random.nextInt(financeTopics.length)] + "的详细分析内容...");
            data.put("heatScore", 60 + random.nextDouble() * 40);
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("source", sources[random.nextInt(sources.length)]);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(24))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            hotspotData.add(data);
        }
    }
    
    private static void generatePolicyHotspots() {
        Random random = new Random();
        
        String[] policyTopics = {
            "金融监管新政策", "税收政策调整", "货币政策解读", 
            "房地产调控政策", "科技创新扶持政策", "绿色金融政策"
        };
        
        String[] sources = {"人民日报", "中国政府网", "财政部", "央行官网"};
        String[] sentiments = {"积极", "中性"};
        
        for (int i = 0; i < 30; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "POL_" + String.format("%04d", i + 1));
            data.put("title", policyTopics[random.nextInt(policyTopics.length)] + " - " + (i + 1));
            data.put("category", "政策动态");
            data.put("content", "关于" + policyTopics[random.nextInt(policyTopics.length)] + "的最新政策解读和影响分析...");
            data.put("heatScore", 70 + random.nextDouble() * 30);
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("source", sources[random.nextInt(sources.length)]);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(48))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            hotspotData.add(data);
        }
    }
    
    private static void generateMarketNews() {
        Random random = new Random();
        
        String[] marketTopics = {
            "股市收盘分析", "板块轮动观察", "外资流入动向", 
            "新股上市表现", "指数调整影响", "市场情绪指标"
        };
        
        String[] sources = {"财新网", "第一财经", "证券时报", "金融界"};
        String[] sentiments = {"积极", "中性", "消极"};
        
        for (int i = 0; i < 40; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "MKT_" + String.format("%04d", i + 1));
            data.put("title", marketTopics[random.nextInt(marketTopics.length)] + " - " + (i + 1));
            data.put("category", "市场新闻");
            data.put("content", "今日" + marketTopics[random.nextInt(marketTopics.length)] + "的详细市场分析和投资建议...");
            data.put("heatScore", 50 + random.nextDouble() * 50);
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("source", sources[random.nextInt(sources.length)]);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(12))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            hotspotData.add(data);
        }
    }
    
    private static void generateIndustryNews() {
        Random random = new Random();
        
        String[] industryTopics = {
            "科技行业发展", "新能源产业动态", "医药行业前景", 
            "消费升级趋势", "制造业转型", "服务业创新"
        };
        
        String[] sources = {"中国产经新闻", "经济日报", "工信部", "行业协会"};
        String[] sentiments = {"积极", "中性"};
        
        for (int i = 0; i < 25; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "IND_" + String.format("%04d", i + 1));
            data.put("title", industryTopics[random.nextInt(industryTopics.length)] + " - " + (i + 1));
            data.put("category", "行业资讯");
            data.put("content", "关于" + industryTopics[random.nextInt(industryTopics.length)] + "的最新行业分析和发展前景...");
            data.put("heatScore", 55 + random.nextDouble() * 35);
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("source", sources[random.nextInt(sources.length)]);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(36))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            hotspotData.add(data);
        }
    }
    
    private static void updateDataStatistics() {
        int totalHotspots = hotspotData.size();
        int financeCount = 0;
        int policyCount = 0;
        int positiveCount = 0;
        int neutralCount = 0;
        int negativeCount = 0;
        
        for (Map<String, Object> data : hotspotData) {
            String category = (String) data.get("category");
            String sentiment = (String) data.get("sentiment");
            
            if ("财经热点".equals(category)) {
                financeCount++;
            } else if ("政策动态".equals(category)) {
                policyCount++;
            }
            
            switch (sentiment) {
                case "积极": positiveCount++; break;
                case "中性": neutralCount++; break;
                case "消极": negativeCount++; break;
            }
        }
        
        String overallSentiment;
        if (positiveCount > negativeCount) {
            overallSentiment = "积极";
        } else if (positiveCount < negativeCount) {
            overallSentiment = "消极";
        } else {
            overallSentiment = "中性";
        }
        
        dataStatistics.put("total_hotspots", totalHotspots);
        dataStatistics.put("finance_hotspots", financeCount);
        dataStatistics.put("policy_hotspots", policyCount);
        dataStatistics.put("market_sentiment", overallSentiment);
        dataStatistics.put("last_update", 
            lastUpdateTime != null ? lastUpdateTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")) : 
            LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
    }
    
    public static List<Map<String, Object>> getHotspotData() {
        return new ArrayList<>(hotspotData);
    }
    
    public static Map<String, Object> getDataStatistics() {
        return new HashMap<>(dataStatistics);
    }
}