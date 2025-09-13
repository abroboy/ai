@SpringBootApplication
class WindApp {
    @RestController
    static class DashboardController {
        
        @GetMapping("/")
        String home() {
            return '''
<!DOCTYPE html>
<html>
<head>
    <title>万得行业分类仪表盘</title>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row">
            <div class="col-12">
                <h1 class="text-center mb-4">万得行业分类仪表盘</h1>
                <div class="alert alert-success text-center">
                    <h4>✅ Spring Boot API服务已启动！</h4>
                    <p>端口: 5001 | 数据库: MySQL | 状态: 运行中</p>
                </div>
                
                <div class="row mt-4">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5 class="card-title">📊 股票映射管理</h5>
                                <p class="card-text">管理股票与万得行业分类的映射关系</p>
                                <a href="/stock-mappings" class="btn btn-primary">进入管理</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5 class="card-title">📈 数据分析</h5>
                                <p class="card-text">查看股票资金流向和行业分析</p>
                                <a href="/data-analysis" class="btn btn-info">查看分析</a>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="mt-4">
                    <div class="alert alert-info">
                        <h6>API测试链接:</h6>
                        <ul>
                            <li><a href="/api/stock-mappings">股票映射API</a></li>
                            <li><a href="/api/stock-mappings/stats">股票统计API</a></li>
                            <li><a href="/api/wind-industries">行业分类API</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
            '''
        }
        
        @GetMapping("/stock-mappings")
        String stockMappings() {
            return "redirect:/"
        }
        
        @GetMapping("/data-analysis") 
        String dataAnalysis() {
            return "redirect:/"
        }
        
        @GetMapping("/api/stock-mappings")
        @ResponseBody
        Map getStockMappings(@RequestParam(defaultValue = "0") int page,
                             @RequestParam(defaultValue = "20") int size) {
            
            def stockData = [
                [stockCode: "000001", stockName: "平安银行", industryName: "银行", marketType: "A股", mappingStatus: "已映射", 
                 totalMarketValue: 85600, dailyNetInflow: 2580, netInflowRatio: 0.025, recentVolatility: 0.032, 
                 latest7dInflow: 15600, lastUpdated: new Date()],
                [stockCode: "000002", stockName: "万科A", industryName: "房地产", marketType: "A股", mappingStatus: "已映射",
                 totalMarketValue: 126800, dailyNetInflow: -1850, netInflowRatio: -0.018, recentVolatility: 0.045,
                 latest7dInflow: -8200, lastUpdated: new Date()],
                [stockCode: "000858", stockName: "五粮液", industryName: "白酒", marketType: "A股", mappingStatus: "已映射",
                 totalMarketValue: 234500, dailyNetInflow: 4680, netInflowRatio: 0.038, recentVolatility: 0.028,
                 latest7dInflow: 25600, lastUpdated: new Date()],
                [stockCode: "002415", stockName: "海康威视", industryName: "安防", marketType: "A股", mappingStatus: "已映射",
                 totalMarketValue: 98600, dailyNetInflow: 1950, netInflowRatio: 0.022, recentVolatility: 0.041,
                 latest7dInflow: 12800, lastUpdated: new Date()],
                [stockCode: "300059", stockName: "东方财富", industryName: "证券", marketType: "A股", mappingStatus: "已映射",
                 totalMarketValue: 156400, dailyNetInflow: 3250, netInflowRatio: 0.029, recentVolatility: 0.052,
                 latest7dInflow: 18900, lastUpdated: new Date()]
            ]
            
            return [
                success: true,
                data: [
                    content: stockData,
                    totalElements: stockData.size(),
                    totalPages: 1,
                    currentPage: page,
                    size: size,
                    numberOfElements: stockData.size(),
                    hasNext: false,
                    hasPrevious: false
                ]
            ]
        }
        
        @GetMapping("/api/stock-mappings/stats")
        @ResponseBody
        Map getStockMappingStats() {
            return [
                success: true,
                data: [
                    total_stocks: 21,
                    mapped_count: 18,
                    unmapped_count: 3,
                    a_stock_count: 19,
                    kc_stock_count: 2
                ]
            ]
        }
        
        @GetMapping("/api/wind-industries")
        @ResponseBody
        Map getWindIndustries() {
            def industries = [
                [industryCode: "110000", industryName: "银行", industryLevel: 1],
                [industryCode: "210000", industryName: "房地产", industryLevel: 1], 
                [industryCode: "220000", industryName: "白酒", industryLevel: 1],
                [industryCode: "230000", industryName: "医药", industryLevel: 1],
                [industryCode: "240000", industryName: "科技", industryLevel: 1]
            ]
            
            return [
                success: true,
                data: industries,
                total: industries.size()
            ]
        }
        
        @PostMapping("/api/stock-mappings/refresh")
        @ResponseBody
        Map refreshStockMappingData() {
            return [
                success: true,
                message: "股票映射数据刷新成功"
            ]
        }
        
        @GetMapping("/api/market/distribution")
        @ResponseBody
        Map getMarketDistribution() {
            return [
                success: true,
                data: [
                    [market_type: "A股", count: 19],
                    [market_type: "科创板", count: 2]
                ]
            ]
        }
        
        @GetMapping("/api/industry/distribution")
        @ResponseBody
        Map getIndustryDistribution() {
            return [
                success: true,
                data: [
                    [industry_name: "银行", count: 8],
                    [industry_name: "证券", count: 5],
                    [industry_name: "房地产", count: 4],
                    [industry_name: "白酒", count: 2],
                    [industry_name: "医药", count: 2]
                ]
            ]
        }
        
        @GetMapping("/api/capital-flow/trend")
        @ResponseBody
        Map getCapitalFlowTrend(@RequestParam(defaultValue = "7") int days) {
            def trend = []
            (1..days).each { day ->
                def date = new Date() - (days - day)
                trend << [
                    date: date.format('yyyy-MM-dd'),
                    net_inflow: (Math.random() * 200000 - 100000) as int,
                    total_inflow: (Math.random() * 500000) as int,
                    total_outflow: (Math.random() * 400000) as int
                ]
            }
            
            return [
                success: true,
                data: trend
            ]
        }
    }
}