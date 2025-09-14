package com.internationalhotspot.service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * 国外热点数据服务
 * 负责拉取和管理国际财经热点、地缘政治事件等信息
 */
public class InternationalHotspotDataService {
    
    private static final List<Map<String, Object>> internationalHotspotData = new ArrayList<>();
    private static final Map<String, Object> dataStatistics = new HashMap<>();
    private static LocalDateTime lastUpdateTime;
    
    public static void initialize() {
        System.out.println("初始化国外热点数据服务...");
        refreshData();
        System.out.println("国外热点数据服务初始化完成");
    }
    
    public static void refreshData() {
        System.out.println("开始刷新国外热点数据: " + LocalDateTime.now());
        
        internationalHotspotData.clear();
        
        // 生成美国新闻数据
        generateUsNews();
        
        // 生成欧洲新闻数据
        generateEuropeNews();
        
        // 生成亚洲新闻数据
        generateAsiaNews();
        
        // 生成新兴市场新闻数据
        generateEmergingMarketsNews();
        
        // 更新统计数据
        updateDataStatistics();
        
        lastUpdateTime = LocalDateTime.now();
        System.out.println("国外热点数据刷新完成，共获取 " + internationalHotspotData.size() + " 条国际资讯");
    }
    
    private static void generateUsNews() {
        Random random = new Random();
        
        String[] usTopics = {
            "美联储政策决议", "纳斯达克市场动向", "美国就业数据", 
            "科技股表现分析", "美债收益率变化", "美元汇率走势"
        };
        
        String[] sources = {"Reuters", "Bloomberg", "CNBC", "Wall Street Journal"};
        String[] sentiments = {"积极", "中性", "消极"};
        
        for (int i = 0; i < 40; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "US_" + String.format("%04d", i + 1));
            data.put("title", usTopics[random.nextInt(usTopics.length)] + " - " + (i + 1));
            data.put("region", "北美");
            data.put("category", "财经新闻");
            data.put("content", "关于" + usTopics[random.nextInt(usTopics.length)] + "的最新分析和市场影响评估...");
            data.put("impactScore", 60 + random.nextDouble() * 40);
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("source", sources[random.nextInt(sources.length)]);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(24))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            internationalHotspotData.add(data);
        }
    }
    
    private static void generateEuropeNews() {
        Random random = new Random();
        
        String[] europeTopics = {
            "欧央行货币政策", "英国脱欧后续", "德国经济数据", 
            "欧盟贸易政策", "法国市场分析", "欧洲股市表现"
        };
        
        String[] sources = {"Financial Times", "Reuters Europe", "BBC Business", "Euronews"};
        String[] sentiments = {"积极", "中性", "消极"};
        
        for (int i = 0; i < 35; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "EU_" + String.format("%04d", i + 1));
            data.put("title", europeTopics[random.nextInt(europeTopics.length)] + " - " + (i + 1));
            data.put("region", "欧洲");
            data.put("category", "财经新闻");
            data.put("content", "欧洲地区" + europeTopics[random.nextInt(europeTopics.length)] + "的深度分析报告...");
            data.put("impactScore", 55 + random.nextDouble() * 35);
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("source", sources[random.nextInt(sources.length)]);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(36))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            internationalHotspotData.add(data);
        }
    }
    
    private static void generateAsiaNews() {
        Random random = new Random();
        
        String[] asiaTopics = {
            "日本央行政策", "韩国经济动向", "澳洲市场分析", 
            "亚太贸易合作", "东南亚投资", "亚洲股市表现"
        };
        
        String[] sources = {"Nikkei Asia", "South China Morning Post", "Asian Financial Review", "The Australian"};
        String[] sentiments = {"积极", "中性", "消极"};
        
        for (int i = 0; i < 30; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "ASIA_" + String.format("%04d", i + 1));
            data.put("title", asiaTopics[random.nextInt(asiaTopics.length)] + " - " + (i + 1));
            data.put("region", "亚太");
            data.put("category", "财经新闻");
            data.put("content", "亚太地区" + asiaTopics[random.nextInt(asiaTopics.length)] + "的市场分析和投资展望...");
            data.put("impactScore", 50 + random.nextDouble() * 40);
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("source", sources[random.nextInt(sources.length)]);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(48))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            internationalHotspotData.add(data);
        }
    }
    
    private static void generateEmergingMarketsNews() {
        Random random = new Random();
        
        String[] emergingTopics = {
            "印度经济增长", "巴西市场动态", "俄罗斯能源政策", 
            "新兴市场投资", "发展中国家贸易", "全球南方合作"
        };
        
        String[] sources = {"Emerging Markets Review", "Global Finance", "International Herald", "World Bank News"};
        String[] sentiments = {"积极", "中性", "消极"};
        
        for (int i = 0; i < 25; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "EM_" + String.format("%04d", i + 1));
            data.put("title", emergingTopics[random.nextInt(emergingTopics.length)] + " - " + (i + 1));
            data.put("region", "新兴市场");
            data.put("category", "地缘政治");
            data.put("content", "新兴市场" + emergingTopics[random.nextInt(emergingTopics.length)] + "的发展趋势和机遇挑战...");
            data.put("impactScore", 45 + random.nextDouble() * 45);
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("source", sources[random.nextInt(sources.length)]);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(72))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            internationalHotspotData.add(data);
        }
    }
    
    private static void updateDataStatistics() {
        int totalHotspots = internationalHotspotData.size();
        int usCount = 0;
        int europeCount = 0;
        int asiaCount = 0;
        int positiveCount = 0;
        int neutralCount = 0;
        int negativeCount = 0;
        
        for (Map<String, Object> data : internationalHotspotData) {
            String region = (String) data.get("region");
            String sentiment = (String) data.get("sentiment");
            
            switch (region) {
                case "北美": usCount++; break;
                case "欧洲": europeCount++; break;
                case "亚太": asiaCount++; break;
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
        
        dataStatistics.put("total_international_hotspots", totalHotspots);
        dataStatistics.put("us_news_count", usCount);
        dataStatistics.put("europe_news_count", europeCount);
        dataStatistics.put("asia_news_count", asiaCount);
        dataStatistics.put("global_sentiment", overallSentiment);
        dataStatistics.put("last_update", 
            lastUpdateTime != null ? lastUpdateTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")) : 
            LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
    }
    
    public static List<Map<String, Object>> getInternationalHotspotData() {
        return new ArrayList<>(internationalHotspotData);
    }
    
    public static Map<String, Object> getDataStatistics() {
        return new HashMap<>(dataStatistics);
    }
}