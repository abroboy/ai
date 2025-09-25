import com.domestichotspot.service.DomesticHotspotDataService;
import java.util.List;
import java.util.Map;

public class TestDataCount {
    public static void main(String[] args) {
        System.out.println("=== 国内热点数据量测试 ===");
        
        // 初始化服务
        DomesticHotspotDataService.initialize();
        
        // 获取数据
        List<Map<String, Object>> hotspotData = DomesticHotspotDataService.getHotspotData();
        Map<String, Object> stats = DomesticHotspotDataService.getDataStatistics();
        
        System.out.println("总数据量: " + hotspotData.size());
        System.out.println("统计数据: " + stats);
        
        // 按类别统计
        int financeCount = 0;
        int policyCount = 0;
        int marketCount = 0;
        int industryCount = 0;
        
        for (Map<String, Object> data : hotspotData) {
            String category = (String) data.get("category");
            switch (category) {
                case "财经热点": financeCount++; break;
                case "政策动态": policyCount++; break;
                case "市场新闻": marketCount++; break;
                case "行业资讯": industryCount++; break;
            }
        }
        
        System.out.println("\n=== 按类别统计 ===");
        System.out.println("财经热点: " + financeCount);
        System.out.println("政策动态: " + policyCount);
        System.out.println("市场新闻: " + marketCount);
        System.out.println("行业资讯: " + industryCount);
        
        System.out.println("\n=== 数据样本 ===");
        for (int i = 0; i < Math.min(5, hotspotData.size()); i++) {
            Map<String, Object> data = hotspotData.get(i);
            System.out.println((i+1) + ". " + data.get("title") + " [" + data.get("category") + "]");
        }
    }
}
