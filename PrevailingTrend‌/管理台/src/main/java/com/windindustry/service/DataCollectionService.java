package com.windindustry.service;

import com.windindustry.model.StockIndustryMapping;
import com.windindustry.model.StockFlowData;
import com.windindustry.model.WindIndustryClassification;
import com.windindustry.model.ListedCompanyInfo;
import com.windindustry.model.HkConnectStock;
import com.windindustry.repository.StockIndustryRepository;
import com.windindustry.repository.StockFlowRepository;
import com.windindustry.repository.WindIndustryClassificationRepository;
import com.windindustry.repository.ListedCompanyInfoRepository;
import com.windindustry.repository.HkConnectStockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.LocalDate;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

@Service
public class DataCollectionService {
    
    @Autowired
    private StockIndustryRepository stockIndustryRepository;
    
    @Autowired
    private StockFlowRepository stockFlowRepository;
    
    @Autowired
    private WindIndustryClassificationRepository windIndustryRepository;
    
    @Autowired
    private ListedCompanyInfoRepository listedCompanyRepository;
    
    @Autowired
    private HkConnectStockRepository hkConnectRepository;
    
    private final WebClient webClient = WebClient.builder().build();
    
    public void initializeData() {
        System.out.println("开始初始化数据...");
        
        // 初始化行业分类数据
        long industryCount = windIndustryRepository.count();
        if (industryCount == 0) {
            System.out.println("行业分类数据库为空，开始拉取数据...");
            collectWindIndustryData();
        } else {
            System.out.println("数据库已有 " + industryCount + " 条行业分类数据");
        }
        
        // 初始化股票映射数据
        long stockCount = stockIndustryRepository.count();
        if (stockCount == 0) {
            System.out.println("股票映射数据库为空，开始拉取数据...");
            collectStockData();
            collectFlowData();
        } else {
            System.out.println("数据库已有 " + stockCount + " 条股票数据");
        }
        
        // 初始化上市公司数据
        long companyCount = listedCompanyRepository.count();
        if (companyCount == 0) {
            System.out.println("上市公司数据库为空，开始初始化数据...");
            initializeListedCompanyData();
        } else {
            System.out.println("数据库已有 " + companyCount + " 家上市公司数据");
        }
        
        // 初始化港股通数据
        long hkCount = hkConnectRepository.count();
        if (hkCount == 0) {
            System.out.println("港股通数据库为空，开始初始化数据...");
            initializeHkConnectData();
        } else {
            System.out.println("数据库已有 " + hkCount + " 只港股通股票数据");
        }
    }
    
    public void collectWindIndustryData() {
        System.out.println("正在获取上市公司或行业分类数据...");
        
        try {
            List<WindIndustryClassification> industries = generateWindIndustryData();
            windIndustryRepository.deleteAll();
            windIndustryRepository.saveAll(industries);
            System.out.println("成功保存 " + industries.size() + " 条行业分类数据");
        } catch (Exception e) {
            System.err.println("获取行业分类数据失败: " + e.getMessage());
        }
    }
    
    private List<WindIndustryClassification> generateWindIndustryData() {
        List<WindIndustryClassification> industries = new ArrayList<>();
        
        // 一级行业分类
        String[][] level1Industries = {
            {"110000", "石油石化"},
            {"210000", "有色金属"},
            {"220000", "钢铁"},
            {"230000", "基础化工"},
            {"240000", "建筑材料"},
            {"270000", "机械设备"},
            {"280000", "电力设备"},
            {"330000", "家用电器"},
            {"350000", "计算机"},
            {"360000", "电子"},
            {"370000", "通信"},
            {"410000", "电力及公用事业"},
            {"420000", "交通运输"},
            {"430000", "房地产"},
            {"450000", "商业贸易"},
            {"460000", "休闲服务"},
            {"480000", "银行"},
            {"490000", "非银金融"},
            {"510000", "综合"},
            {"610000", "食品饮料"},
            {"620000", "纺织服装"},
            {"630000", "轻工制造"},
            {"640000", "金融服务"},
            {"710000", "社服"},
            {"720000", "传媒"}
        };
        
        for (String[] industry : level1Industries) {
            WindIndustryClassification classification = new WindIndustryClassification();
            classification.setIndustryCode(industry[0]);
            classification.setIndustryName(industry[1]);
            classification.setIndustryLevel(1);
            classification.setParentIndustryCode(null);
            classification.setIndustryDescription("一级行业: " + industry[1]);
            classification.setIsActive(true);
            industries.add(classification);
        }
        
        // 二级行业分类 (示例数据)
        String[][] level2Industries = {
            {"110100", "石油开采", "110000"},
            {"110200", "石油加工", "110000"},
            {"110300", "化学原料", "110000"},
            {"210100", "黄金", "210000"},
            {"210200", "铜", "210000"},
            {"210300", "铝", "210000"},
            {"220100", "钢铁", "220000"},
            {"270100", "机械基础件", "270000"},
            {"270200", "通用机械", "270000"},
            {"280100", "电机", "280000"},
            {"330100", "白色家电", "330000"},
            {"350100", "计算机设备", "350000"},
            {"360100", "半导体", "360000"},
            {"370100", "通信设备", "370000"},
            {"410100", "电力", "410000"},
            {"430100", "房地产开发", "430000"},
            {"480100", "银行", "480000"},
            {"610100", "食品加工", "610000"},
            {"610200", "饮料制造", "610000"},
            {"610300", "白酒", "610000"}
        };
        
        for (String[] industry : level2Industries) {
            WindIndustryClassification classification = new WindIndustryClassification();
            classification.setIndustryCode(industry[0]);
            classification.setIndustryName(industry[1]);
            classification.setIndustryLevel(2);
            classification.setParentIndustryCode(industry[2]);
            classification.setIndustryDescription("二级行业: " + industry[1]);
            classification.setIsActive(true);
            industries.add(classification);
        }
        
        return industries;
    }
    
    public void collectStockData() {
        System.out.println("正在获取股票列表...");
        
        try {
            List<StockIndustryMapping> stocks = generateMockStockData();
            stockIndustryRepository.deleteAll();
            stockIndustryRepository.saveAll(stocks);
            System.out.println("成功保存 " + stocks.size() + " 条股票数据");
        } catch (Exception e) {
            System.err.println("获取股票数据失败: " + e.getMessage());
        }
    }
    
    public void collectFlowData() {
        System.out.println("正在获取资金流向数据...");
        
        try {
            List<StockIndustryMapping> stocks = stockIndustryRepository.findAll();
            stockFlowRepository.deleteAll();
            
            List<StockFlowData> flowDataList = new ArrayList<>();
            
            for (StockIndustryMapping stock : stocks) {
                for (int i = 0; i < 30; i++) {
                    LocalDate tradeDate = LocalDate.now().minusDays(i);
                    double baseAmount = ThreadLocalRandom.current().nextDouble(-1000000, 1000000);
                    double dailyNet = baseAmount + ThreadLocalRandom.current().nextDouble(-baseAmount * 0.5, baseAmount * 0.5);
                    
                    StockFlowData flowData = new StockFlowData(stock.getStockCode(), tradeDate, dailyNet);
                    flowDataList.add(flowData);
                }
            }
            
            stockFlowRepository.saveAll(flowDataList);
            System.out.println("成功保存资金流向数据");
            
        } catch (Exception e) {
            System.err.println("获取资金流向数据失败: " + e.getMessage());
        }
    }
    
    private List<StockIndustryMapping> generateMockStockData() {
        List<StockIndustryMapping> stocks = new ArrayList<>();
        
        String[][] mockData = {
            {"000001", "平安银行", "80101001", "银行"},
            {"000002", "万科A", "80102001", "房地产开发"},
            {"000858", "五粮液", "80103001", "白酒"},
            {"000725", "京东方A", "80104001", "科技"},
            {"000661", "长春高新", "80105001", "医药"},
            {"002594", "比亚迪", "80106001", "新能源汽车"},
            {"000166", "申万宏源", "80107001", "证券"},
            {"600900", "长江电力", "80108001", "电力"},
            {"000708", "中信特钢", "80109001", "钢铁"},
            {"600519", "贵州茅台", "80103001", "白酒"}
        };
        
        for (String[] data : mockData) {
            StockIndustryMapping stock = new StockIndustryMapping();
            stock.setStockCode(data[0]);
            stock.setStockName(data[1]);
            stock.setIndustryCode(data[2]);
            stock.setIndustryName(data[3]);
            stock.setConfidence(ThreadLocalRandom.current().nextDouble(0.7, 0.99));
            stocks.add(stock);
        }
        
        for (int i = 1; i <= 90; i++) {
            StockIndustryMapping stock = new StockIndustryMapping();
            stock.setStockCode(String.format("%06d", 100000 + i));
            stock.setStockName("股票" + i);
            
            String[] industries = {"80101001", "80102001", "80103001", "80104001", "80105001", "80106001", "80107001", "80108001", "80109001", "80110001"};
            String[] industryNames = {"银行", "房地产开发", "白酒", "科技", "医药", "新能源汽车", "证券", "电力", "钢铁", "其他"};
            
            int industryIndex = ThreadLocalRandom.current().nextInt(industries.length);
            stock.setIndustryCode(industries[industryIndex]);
            stock.setIndustryName(industryNames[industryIndex]);
            stock.setConfidence(ThreadLocalRandom.current().nextDouble(0.7, 0.99));
            
            stocks.add(stock);
        }
        
        return stocks;
    }
    
    public void refreshData() {
        System.out.println("开始刷新数据...");
        collectWindIndustryData();
        collectStockData();
        collectFlowData();
        System.out.println("数据刷新完成");
    }
    
    public void refreshWindIndustryData() {
        System.out.println("刷新上市公司或行业分类数据...");
        collectWindIndustryData();
        System.out.println("上市公司或行业数据刷新完成");
    }
    
    /**
     * 初始化上市公司数据
     */
    private void initializeListedCompanyData() {
        System.out.println("初始化上市公司数据...");
        System.out.println("请使用 ListedCompanyInfoService.initializeCompanyData() 方法初始化数据");
    }
    
    /**
     * 初始化港股通数据
     */
    private void initializeHkConnectData() {
        System.out.println("初始化港股通数据...");
        System.out.println("请使用 HkConnectStockService.initializeHkConnectData() 方法初始化数据");
    }
}
