import com.domestichotspot.service.EnhancedDomesticHotspotDataService;
import java.util.List;
import java.util.Map;

public class TestEnhancedDataCount {
    public static void main(String[] args) {
        System.out.println("=== 增强版国内热点数据量测试 ===");
        
        // 初始化增强版服务
        EnhancedDomesticHotspotDataService.initialize();
        
        // 获取数据
        List<Map<String, Object>> hotspotData = EnhancedDomesticHotspotDataService.getHotspotData();
        Map<String, Object> stats = EnhancedDomesticHotspotDataService.getDataStatistics();
        
        System.out.println("总数据量: " + hotspotData.size());
        System.out.println("统计数据: " + stats);
        
        // 按类别统计
        int financeCount = 0;
        int policyCount = 0;
        int marketCount = 0;
        int industryCount = 0;
        int companyCount = 0;
        int macroCount = 0;
        int investmentCount = 0;
        
        for (Map<String, Object> data : hotspotData) {
            String category = (String) data.get("category");
            switch (category) {
                case "财经热点": financeCount++; break;
                case "政策动态": policyCount++; break;
                case "市场新闻": marketCount++; break;
                case "行业资讯": industryCount++; break;
                case "公司热点": companyCount++; break;
                case "宏观经济": macroCount++; break;
                case "投资热点": investmentCount++; break;
            }
        }
        
        System.out.println("\n=== 按类别统计 ===");
        System.out.println("财经热点: " + financeCount);
        System.out.println("政策动态: " + policyCount);
        System.out.println("市场新闻: " + marketCount);
        System.out.println("行业资讯: " + industryCount);
        System.out.println("公司热点: " + companyCount);
        System.out.println("宏观经济: " + macroCount);
        System.out.println("投资热点: " + investmentCount);
        
        System.out.println("\n=== 情感分析统计 ===");
        System.out.println("积极: " + stats.get("positive_count"));
        System.out.println("中性: " + stats.get("neutral_count"));
        System.out.println("消极: " + stats.get("negative_count"));
        System.out.println("整体情绪: " + stats.get("market_sentiment"));
        
        System.out.println("\n=== 数据样本 ===");
        for (int i = 0; i < Math.min(10, hotspotData.size()); i++) {
            Map<String, Object> data = hotspotData.get(i);
            System.out.println((i+1) + ". " + data.get("title") + " [" + data.get("category") + "]");
        }
    }
}
