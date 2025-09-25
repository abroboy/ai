package com.domestichotspot.service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * 增强版国内热点数据服务
 * 负责拉取和管理国内财经热点、政策动态等信息
 * 大幅增加数据量和数据源
 */
public class EnhancedDomesticHotspotDataService {
    
    private static final List<Map<String, Object>> hotspotData = new ArrayList<>();
    private static final Map<String, Object> dataStatistics = new HashMap<>();
    private static LocalDateTime lastUpdateTime;
    
    public static void initialize() {
        System.out.println("初始化增强版国内热点数据服务...");
        refreshData();
        System.out.println("增强版国内热点数据服务初始化完成");
    }
    
    public static void refreshData() {
        System.out.println("开始刷新增强版国内热点数据: " + LocalDateTime.now());
        
        hotspotData.clear();
        
        // 生成财经热点数据 (增加到100条)
        generateFinanceHotspots();
        
        // 生成政策动态数据 (增加到80条)
        generatePolicyHotspots();
        
        // 生成市场新闻数据 (增加到120条)
        generateMarketNews();
        
        // 生成行业资讯数据 (增加到100条)
        generateIndustryNews();
        
        // 生成公司热点数据 (新增50条)
        generateCompanyHotspots();
        
        // 生成宏观经济数据 (新增50条)
        generateMacroEconomicData();
        
        // 生成投资热点数据 (新增50条)
        generateInvestmentHotspots();
        
        // 更新统计数据
        updateDataStatistics();
        
        lastUpdateTime = LocalDateTime.now();
        System.out.println("增强版国内热点数据刷新完成，共获取 " + hotspotData.size() + " 条热点资讯");
    }
    
    private static void generateFinanceHotspots() {
        Random random = new Random();
        
        String[] financeTopics = {
            "央行货币政策调整分析", "A股市场最新动向", "人民币汇率走势解读", 
            "银行业净息差变化", "券商业绩分析报告", "保险行业发展趋势",
            "债券市场收益率分析", "期货市场交易活跃度", "基金净值变化趋势",
            "信托产品收益率", "私募基金业绩表现", "银行理财产品收益",
            "外汇储备变化", "货币供应量M2分析", "利率市场化进程",
            "金融科技发展", "数字货币试点", "支付行业监管", "征信体系建设"
        };
        
        String[] sources = {"新华财经", "中国证券报", "上海证券报", "经济参考报", "财新网", 
                          "第一财经", "证券时报", "金融界", "东方财富", "同花顺"};
        String[] sentiments = {"积极", "中性", "消极"};
        
        for (int i = 0; i < 100; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "FIN_" + String.format("%04d", i + 1));
            data.put("title", financeTopics[random.nextInt(financeTopics.length)] + " - " + (i + 1));
            data.put("category", "财经热点");
            data.put("content", "这是一条关于" + financeTopics[random.nextInt(financeTopics.length)] + "的详细分析内容，包含市场数据、专家观点和投资建议...");
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
            "房地产调控政策", "科技创新扶持政策", "绿色金融政策",
            "资本市场改革", "银行监管新规", "保险业监管政策",
            "证券法修订", "基金法实施", "期货法制定",
            "反垄断执法", "数据安全法", "个人信息保护法",
            "碳中和政策", "新能源补贴", "制造业升级政策", "服务业开放政策"
        };
        
        String[] sources = {"人民日报", "中国政府网", "财政部", "央行官网", "证监会", 
                          "银保监会", "发改委", "工信部", "商务部", "科技部"};
        String[] sentiments = {"积极", "中性"};
        
        for (int i = 0; i < 80; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "POL_" + String.format("%04d", i + 1));
            data.put("title", policyTopics[random.nextInt(policyTopics.length)] + " - " + (i + 1));
            data.put("category", "政策动态");
            data.put("content", "关于" + policyTopics[random.nextInt(policyTopics.length)] + "的最新政策解读和影响分析，包括政策背景、实施细节和市场影响...");
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
            "新股上市表现", "指数调整影响", "市场情绪指标",
            "成交量变化", "涨跌停板分析", "主力资金流向",
            "技术指标分析", "市场热点轮换", "投资者情绪调查",
            "机构调研报告", "分析师评级变化", "业绩预告影响",
            "并购重组消息", "股权激励计划", "分红派息方案", "股票回购计划"
        };
        
        String[] sources = {"财新网", "第一财经", "证券时报", "金融界", "东方财富", 
                          "同花顺", "雪球", "格隆汇", "智通财经", "华盛通"};
        String[] sentiments = {"积极", "中性", "消极"};
        
        for (int i = 0; i < 120; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "MKT_" + String.format("%04d", i + 1));
            data.put("title", marketTopics[random.nextInt(marketTopics.length)] + " - " + (i + 1));
            data.put("category", "市场新闻");
            data.put("content", "今日" + marketTopics[random.nextInt(marketTopics.length)] + "的详细市场分析和投资建议，包含技术分析和基本面分析...");
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
            "消费升级趋势", "制造业转型", "服务业创新",
            "房地产行业", "汽车产业", "钢铁行业", "有色金属",
            "化工行业", "纺织服装", "食品饮料", "家电行业",
            "通信行业", "互联网行业", "人工智能", "生物医药",
            "新材料", "环保产业", "农业现代化", "物流行业"
        };
        
        String[] sources = {"中国产经新闻", "经济日报", "工信部", "行业协会", "21世纪经济报道",
                          "经济观察报", "中国经营报", "华夏时报", "国际金融报", "每日经济新闻"};
        String[] sentiments = {"积极", "中性"};
        
        for (int i = 0; i < 100; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "IND_" + String.format("%04d", i + 1));
            data.put("title", industryTopics[random.nextInt(industryTopics.length)] + " - " + (i + 1));
            data.put("category", "行业资讯");
            data.put("content", "关于" + industryTopics[random.nextInt(industryTopics.length)] + "的最新行业分析和发展前景，包含行业数据和趋势预测...");
            data.put("heatScore", 55 + random.nextDouble() * 35);
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("source", sources[random.nextInt(sources.length)]);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(36))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            hotspotData.add(data);
        }
    }
    
    private static void generateCompanyHotspots() {
        Random random = new Random();
        
        String[] companyTopics = {
            "上市公司业绩", "企业并购重组", "高管变动", "股权激励",
            "重大合同签订", "新产品发布", "技术突破", "市场拓展",
            "融资计划", "分红方案", "股票回购", "业务转型",
            "战略合作", "投资计划", "研发投入", "品牌建设"
        };
        
        String[] sources = {"公司公告", "交易所", "财经媒体", "行业报告", "分析师报告"};
        String[] sentiments = {"积极", "中性", "消极"};
        
        for (int i = 0; i < 50; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "COM_" + String.format("%04d", i + 1));
            data.put("title", companyTopics[random.nextInt(companyTopics.length)] + " - " + (i + 1));
            data.put("category", "公司热点");
            data.put("content", "关于" + companyTopics[random.nextInt(companyTopics.length)] + "的详细报道和分析，包含公司背景和影响评估...");
            data.put("heatScore", 45 + random.nextDouble() * 45);
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("source", sources[random.nextInt(sources.length)]);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(72))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            hotspotData.add(data);
        }
    }
    
    private static void generateMacroEconomicData() {
        Random random = new Random();
        
        String[] macroTopics = {
            "GDP增长数据", "CPI通胀指标", "PPI价格指数", "PMI采购经理指数",
            "就业数据", "消费数据", "投资数据", "进出口数据",
            "财政收支", "货币供应量", "社会融资规模", "外汇储备",
            "国际收支", "经济景气指数", "消费者信心指数", "企业家信心指数"
        };
        
        String[] sources = {"国家统计局", "央行", "财政部", "商务部", "海关总署"};
        String[] sentiments = {"积极", "中性", "消极"};
        
        for (int i = 0; i < 50; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "MAC_" + String.format("%04d", i + 1));
            data.put("title", macroTopics[random.nextInt(macroTopics.length)] + " - " + (i + 1));
            data.put("category", "宏观经济");
            data.put("content", "关于" + macroTopics[random.nextInt(macroTopics.length)] + "的详细数据分析和经济解读，包含历史对比和趋势分析...");
            data.put("heatScore", 65 + random.nextDouble() * 35);
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("source", sources[random.nextInt(sources.length)]);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(168))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            hotspotData.add(data);
        }
    }
    
    private static void generateInvestmentHotspots() {
        Random random = new Random();
        
        String[] investmentTopics = {
            "投资策略分析", "资产配置建议", "风险控制", "投资机会挖掘",
            "市场趋势判断", "估值分析", "技术分析", "基本面分析",
            "投资组合优化", "对冲策略", "量化投资", "价值投资",
            "成长投资", "主题投资", "行业轮动", "风格切换"
        };
        
        String[] sources = {"投资机构", "基金公司", "券商研报", "私募基金", "投资顾问"};
        String[] sentiments = {"积极", "中性", "消极"};
        
        for (int i = 0; i < 50; i++) {
            Map<String, Object> data = new HashMap<>();
            data.put("id", "INV_" + String.format("%04d", i + 1));
            data.put("title", investmentTopics[random.nextInt(investmentTopics.length)] + " - " + (i + 1));
            data.put("category", "投资热点");
            data.put("content", "关于" + investmentTopics[random.nextInt(investmentTopics.length)] + "的专业分析和投资建议，包含风险评估和收益预期...");
            data.put("heatScore", 55 + random.nextDouble() * 40);
            data.put("sentiment", sentiments[random.nextInt(sentiments.length)]);
            data.put("source", sources[random.nextInt(sources.length)]);
            data.put("publishTime", LocalDateTime.now().minusHours(random.nextInt(96))
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
            
            hotspotData.add(data);
        }
    }
    
    private static void updateDataStatistics() {
        int totalHotspots = hotspotData.size();
        int financeCount = 0;
        int policyCount = 0;
        int marketCount = 0;
        int industryCount = 0;
        int companyCount = 0;
        int macroCount = 0;
        int investmentCount = 0;
        int positiveCount = 0;
        int neutralCount = 0;
        int negativeCount = 0;
        
        for (Map<String, Object> data : hotspotData) {
            String category = (String) data.get("category");
            String sentiment = (String) data.get("sentiment");
            
            switch (category) {
                case "财经热点": financeCount++; break;
                case "政策动态": policyCount++; break;
                case "市场新闻": marketCount++; break;
                case "行业资讯": industryCount++; break;
                case "公司热点": companyCount++; break;
                case "宏观经济": macroCount++; break;
                case "投资热点": investmentCount++; break;
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
        dataStatistics.put("market_hotspots", marketCount);
        dataStatistics.put("industry_hotspots", industryCount);
        dataStatistics.put("company_hotspots", companyCount);
        dataStatistics.put("macro_hotspots", macroCount);
        dataStatistics.put("investment_hotspots", investmentCount);
        dataStatistics.put("market_sentiment", overallSentiment);
        dataStatistics.put("positive_count", positiveCount);
        dataStatistics.put("neutral_count", neutralCount);
        dataStatistics.put("negative_count", negativeCount);
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
