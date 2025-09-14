package com.forumhotspot.service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * 论坛热点数据服务
 * 负责拉取和管理各大金融论坛的热点数据
 */
public class ForumHotspotDataService {
    
    private static final List<Map<String, Object>> forumHotspotData = new ArrayList<>();
    private static final Map<String, Object> dataStatistics = new HashMap<>();
    private static LocalDateTime lastUpdateTime;
    
    public static void initialize() {
        System.out.println("初始化论坛热点数据服务...");
        refreshData();
        System.out.println("论坛热点数据服务初始化完成");
    }
    
    public static void refreshData() {
        System.out.println("开始刷新论坛热点数据: " + LocalDateTime.now());
        
        forumHotspotData.clear();
        
        // 生成雪球热帖数据
        generateXueqiuPosts();
        
        // 生成东方财富热帖数据
        generateEastmoneyPosts();
        
        // 生成同花顺热帖数据
        generateTonghuashunPosts();
        
        // 更新统计数据
        updateDataStatistics();
        
        lastUpdateTime = LocalDateTime.now();
        System.out.println("论坛热点数据刷新完成，共获取 " + forumHotspotData.size() + " 条热帖数据");
    }
    
    private static void generateXueqiuPosts() {
        Random random = new Random();
        
        String[] stockTopics = {"贵州茅台", "宁德时代", "比亚迪", "腾讯控股", "阿里巴巴", "美团"};
        String[] postTypes = {"买入分析", "卖出观点", "持有建议", "技术分析", "基本面分析"};
        String[] sentiments = {"看多", "看空", "中性"};
        
        for (int i = 0; i < 60; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("postId", "XQ_" + String.format("%06d", i + 1));
            data.put("platform", "雪球");
            data.put("title", stockTopics[random.nextInt(stockTopics.length)] + postTypes[random.nextInt(postTypes.length)]);
            data.put("content", "关于" + stockTopics[random.nextInt(stockTopics.length)] + "的详细分析...");
            data.put("author", "雪球用户" + (i + 1));
            data.put("likeCount", random.nextInt(1000));
            data.put("commentCount", random.nextInt(200));
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("heatScore", 50 + random.nextDouble() * 50);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(24))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            forumHotspotData.add(data);
        }
    }
    
    private static void generateEastmoneyPosts() {
        Random random = new Random();
        
        String[] marketTopics = {"大盘走势", "板块轮动", "个股推荐", "技术指标", "资金流向"};
        String[] sentiments = {"看多", "看空", "中性"};
        
        for (int i = 0; i < 45; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("postId", "EM_" + String.format("%06d", i + 1));
            data.put("platform", "东方财富");
            data.put("title", marketTopics[random.nextInt(marketTopics.length)] + "讨论 - " + (i + 1));
            data.put("content", "今日" + marketTopics[random.nextInt(marketTopics.length)] + "的深度分析和观点分享...");
            data.put("author", "东财股友" + (i + 1));
            data.put("likeCount", random.nextInt(800));
            data.put("commentCount", random.nextInt(150));
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("heatScore", 40 + random.nextDouble() * 45);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(36))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            forumHotspotData.add(data);
        }
    }
    
    private static void generateTonghuashunPosts() {
        Random random = new Random();
        
        String[] investmentTopics = {"价值投资", "短线操作", "长线持有", "风险控制", "仓位管理"};
        String[] sentiments = {"看多", "看空", "中性"};
        
        for (int i = 0; i < 35; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("postId", "THS_" + String.format("%06d", i + 1));
            data.put("platform", "同花顺");
            data.put("title", investmentTopics[random.nextInt(investmentTopics.length)] + "心得 - " + (i + 1));
            data.put("content", "分享" + investmentTopics[random.nextInt(investmentTopics.length)] + "的实战经验和策略...");
            data.put("author", "同花顺用户" + (i + 1));
            data.put("likeCount", random.nextInt(600));
            data.put("commentCount", random.nextInt(120));
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("heatScore", 35 + random.nextDouble() * 40);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(48))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            forumHotspotData.add(data);
        }
    }
    
    private static void updateDataStatistics() {
        int totalPosts = forumHotspotData.size();
        int xueqiuCount = 0;
        int eastmoneyCount = 0;
        int positiveCount = 0;
        int neutralCount = 0;
        int negativeCount = 0;
        
        for (Map<String, Object> data : forumHotspotData) {
            String platform = (String) data.get("platform");
            String sentiment = (String) data.get("sentiment");
            
            switch (platform) {
                case "雪球": xueqiuCount++; break;
                case "东方财富": eastmoneyCount++; break;
            }
            
            switch (sentiment) {
                case "看多": positiveCount++; break;
                case "中性": neutralCount++; break;
                case "看空": negativeCount++; break;
            }
        }
        
        String overallSentiment;
        if (positiveCount > negativeCount) {
            overallSentiment = "乐观";
        } else if (positiveCount < negativeCount) {
            overallSentiment = "悲观";
        } else {
            overallSentiment = "中性";
        }
        
        dataStatistics.put("total_posts", totalPosts);
        dataStatistics.put("xueqiu_posts", xueqiuCount);
        dataStatistics.put("eastmoney_posts", eastmoneyCount);
        dataStatistics.put("forum_sentiment", overallSentiment);
        dataStatistics.put("last_update", 
            lastUpdateTime != null ? lastUpdateTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")) : 
            LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
    }
    
    public static List<Map<String, Object>> getForumHotspotData() {
        return new ArrayList<>(forumHotspotData);
    }
    
    public static Map<String, Object> getDataStatistics() {
        return new HashMap<>(dataStatistics);
    }
}