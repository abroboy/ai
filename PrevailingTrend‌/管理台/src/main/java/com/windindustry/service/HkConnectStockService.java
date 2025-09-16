package com.windindustry.service;

import com.windindustry.model.HkConnectStock;
import com.windindustry.repository.HkConnectStockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

/**
 * 港股通服务层
 * 提供港股通股票信息的查询、统计和管理功能
 */
@Service
public class HkConnectStockService {
    
    @Autowired
    private HkConnectStockRepository hkConnectRepository;
    
    /**
     * 获取港股通统计数据
     */
    public Map<String, Object> getHkConnectStatistics() {
        Map<String, Object> stats = new HashMap<>();
        
        // 基础统计
        long totalStocks = hkConnectRepository.count();
        long activeStocks = hkConnectRepository.findByIsActiveTrue().size();
        long suspendedStocks = hkConnectRepository.findByIsSuspendedFalse().size();
        
        stats.put("total_stocks", totalStocks);
        stats.put("active_stocks", activeStocks);
        stats.put("suspended_stocks", suspendedStocks);
        
        // 港股通类型分布
        List<Object[]> connectTypeStats = hkConnectRepository.getConnectTypeStatistics();
        List<Map<String, Object>> connectTypeDistribution = new ArrayList<>();
        for (Object[] stat : connectTypeStats) {
            Map<String, Object> type = new HashMap<>();
            type.put("connect_type", stat[0]);
            type.put("count", stat[1]);
            connectTypeDistribution.add(type);
        }
        stats.put("connect_type_distribution", connectTypeDistribution);
        
        // 行业分布统计
        List<Object[]> industryStats = hkConnectRepository.getIndustryStatistics();
        List<Map<String, Object>> industryDistribution = new ArrayList<>();
        for (Object[] stat : industryStats) {
            Map<String, Object> industry = new HashMap<>();
            industry.put("industry_code", stat[0]);
            industry.put("industry_name", stat[1]);
            industry.put("count", stat[2]);
            industryDistribution.add(industry);
        }
        stats.put("industry_distribution", industryDistribution);
        
        // 板块分布
        List<Object[]> boardStats = hkConnectRepository.getBoardTypeStatistics();
        List<Map<String, Object>> boardDistribution = new ArrayList<>();
        for (Object[] stat : boardStats) {
            Map<String, Object> board = new HashMap<>();
            board.put("board_type", stat[0]);
            board.put("count", stat[1]);
            boardDistribution.add(board);
        }
        stats.put("board_distribution", boardDistribution);
        
        // 北向资金统计
        BigDecimal totalNorthboundInflowSh = hkConnectRepository.getTotalNorthboundInflowByConnectType("沪港通");
        BigDecimal totalNorthboundInflowSz = hkConnectRepository.getTotalNorthboundInflowByConnectType("深港通");
        
        stats.put("total_northbound_inflow_sh", totalNorthboundInflowSh != null ? totalNorthboundInflowSh : BigDecimal.ZERO);
        stats.put("total_northbound_inflow_sz", totalNorthboundInflowSz != null ? totalNorthboundInflowSz : BigDecimal.ZERO);
        
        return stats;
    }
    
    /**
     * 分页查询港股通股票
     */
    public Page<HkConnectStock> getHkConnectStocks(int page, int size, String sortBy, String sortDir,
                                                   String stockCode, String stockNameCn, String connectType,
                                                   String industryCode, Boolean isActive) {
        
        Sort sort = sortDir.equalsIgnoreCase("desc") ? 
                   Sort.by(sortBy).descending() : Sort.by(sortBy).ascending();
        Pageable pageable = PageRequest.of(page, size, sort);
        
        return hkConnectRepository.findByMultipleFilters(
                stockCode, stockNameCn, connectType, industryCode, isActive, pageable);
    }
    
    /**
     * 根据股票代码获取港股通股票信息
     */
    public Optional<HkConnectStock> getHkConnectStockByCode(String stockCode) {
        return hkConnectRepository.findByStockCode(stockCode);
    }
    
    /**
     * 获取市值排行榜
     */
    public List<HkConnectStock> getMarketValueRanking(int limit) {
        Pageable pageable = PageRequest.of(0, limit);
        return hkConnectRepository.findTopByMarketValue(pageable);
    }
    
    /**
     * 获取北向资金流入排行榜
     */
    public List<HkConnectStock> getNorthboundInflowRanking(int limit) {
        Pageable pageable = PageRequest.of(0, limit);
        return hkConnectRepository.findTopNorthboundInflows(pageable);
    }
    
    /**
     * 获取高股息股票
     */
    public List<HkConnectStock> getHighDividendStocks(BigDecimal minYield) {
        return hkConnectRepository.findByDividendYieldGreaterThan(minYield);
    }
    
    /**
     * 获取活跃交易股票
     */
    public List<HkConnectStock> getActivelyTradedStocks(BigDecimal minTurnover) {
        return hkConnectRepository.findByDailyTurnoverGreaterThan(minTurnover);
    }
    
    /**
     * 保存或更新港股通股票信息
     */
    public HkConnectStock saveHkConnectStock(HkConnectStock stock) {
        return hkConnectRepository.save(stock);
    }
    
    /**
     * 批量保存港股通股票信息
     */
    public List<HkConnectStock> saveAllHkConnectStocks(List<HkConnectStock> stocks) {
        return hkConnectRepository.saveAll(stocks);
    }
    
    /**
     * 刷新港股通数据
     */
    public void refreshHkConnectData() {
        System.out.println("开始刷新港股通数据...");
        
        try {
            // 获取所有活跃股票
            List<HkConnectStock> stocks = hkConnectRepository.findByIsActiveTrue();
            
            // 更新数据
            for (HkConnectStock stock : stocks) {
                updateHkConnectStockData(stock);
            }
            
            // 批量保存
            hkConnectRepository.saveAll(stocks);
            
            System.out.println("港股通数据刷新完成，共更新 " + stocks.size() + " 只股票");
            
        } catch (Exception e) {
            System.err.println("刷新港股通数据失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * 更新单只港股通股票的模拟数据
     */
    private void updateHkConnectStockData(HkConnectStock stock) {
        Random random = ThreadLocalRandom.current();
        
        // 更新汇率 (0.85-0.95之间波动)
        BigDecimal exchangeRate = BigDecimal.valueOf(0.85 + random.nextDouble() * 0.1);
        stock.setExchangeRateHkdRmb(exchangeRate);
        
        // 更新港币股价 (基于现有价格±15%波动)
        if (stock.getLatestPriceHkd() != null) {
            double currentPrice = stock.getLatestPriceHkd().doubleValue();
            double newPrice = currentPrice * (0.85 + random.nextDouble() * 0.3);
            stock.setLatestPriceHkd(BigDecimal.valueOf(Math.round(newPrice * 100.0) / 100.0));
            
            // 更新人民币股价
            BigDecimal rmbPrice = stock.getLatestPriceHkd().multiply(exchangeRate);
            stock.setLatestPriceRmb(rmbPrice);
            
            // 更新市值
            if (stock.getTotalShares() != null) {
                stock.setMarketValueHkd(stock.getLatestPriceHkd().multiply(stock.getTotalShares()));
                stock.setMarketValueRmb(stock.getLatestPriceRmb().multiply(stock.getTotalShares()));
            }
        }
        
        // 更新北向资金流入 (-50000 到 200000万元)
        double northboundInflow = -50000 + random.nextDouble() * 250000;
        stock.setNorthboundNetInflow(BigDecimal.valueOf(Math.round(northboundInflow * 100.0) / 100.0));
        
        // 更新北向持股比例 (0-30%)
        double holdingRatio = random.nextDouble() * 0.3;
        stock.setNorthboundHoldingRatio(BigDecimal.valueOf(Math.round(holdingRatio * 10000.0) / 10000.0));
        
        // 更新日成交额
        double turnoverHkd = 1000 + random.nextDouble() * 500000;
        stock.setDailyTurnoverHkd(BigDecimal.valueOf(Math.round(turnoverHkd * 100.0) / 100.0));
        stock.setDailyTurnoverRmb(stock.getDailyTurnoverHkd().multiply(exchangeRate));
        
        // 更新每日额度使用率 (0-100%)
        double quotaUsage = random.nextDouble();
        stock.setDailyQuotaUsage(BigDecimal.valueOf(Math.round(quotaUsage * 10000.0) / 10000.0));
        
        // 更新PE和PB
        stock.setPeRatio(BigDecimal.valueOf(3 + random.nextDouble() * 47));
        stock.setPbRatio(BigDecimal.valueOf(0.3 + random.nextDouble() * 9.7));
        
        // 更新股息率
        stock.setDividendYield(BigDecimal.valueOf(random.nextDouble() * 0.12));
    }
    
    /**
     * 初始化港股通测试数据
     */
    public void initializeHkConnectData() {
        System.out.println("初始化港股通数据...");
        
        // 检查是否已有数据
        if (hkConnectRepository.count() > 0) {
            System.out.println("港股通数据已存在，跳过初始化");
            return;
        }
        
        List<HkConnectStock> stocks = generateHkConnectTestData();
        hkConnectRepository.saveAll(stocks);
        
        System.out.println("成功初始化 " + stocks.size() + " 只港股通股票数据");
    }
    
    /**
     * 生成港股通测试数据
     */
    private List<HkConnectStock> generateHkConnectTestData() {
        List<HkConnectStock> stocks = new ArrayList<>();
        Random random = ThreadLocalRandom.current();
        
        // 港股通主要股票数据
        Object[][] stockData = {
            // {股票代码, 中文名称, 英文名称, 港股通类型, 板块类型, 行业代码, 行业名称}
            {"00700", "腾讯控股", "Tencent Holdings Ltd", "沪港通", "主板", "350000", "计算机"},
            {"00941", "中国移动", "China Mobile Ltd", "沪港通", "主板", "370000", "通信"},
            {"03690", "美团-W", "Meituan-W", "沪港通", "主板", "450000", "商业贸易"},
            {"01024", "快手-W", "Kuaishou Technology", "沪港通", "主板", "720000", "传媒"},
            {"09988", "阿里巴巴-SW", "Alibaba Group Holding Ltd", "沪港通", "主板", "350000", "计算机"},
            {"02318", "中国平安", "Ping An Insurance Group", "沪港通", "主板", "490000", "非银金融"},
            {"01398", "工商银行", "Industrial and Commercial Bank of China", "沪港通", "主板", "480000", "银行"},
            {"00388", "香港交易所", "Hong Kong Exchanges and Clearing", "沪港通", "主板", "490000", "非银金融"},
            {"01810", "小米集团-W", "Xiaomi Corporation-W", "深港通", "主板", "360000", "电子"},
            {"02020", "安踏体育", "ANTA Sports Products Ltd", "深港通", "主板", "620000", "纺织服装"},
            {"01211", "比亚迪股份", "BYD Company Ltd", "深港通", "主板", "420000", "交通运输"},
            {"06618", "京东集团-SW", "JD.com Inc", "深港通", "主板", "450000", "商业贸易"},
            {"09618", "京东健康", "JD Health International Inc", "深港通", "主板", "710000", "社服"},
            {"01093", "石药集团", "CSPC Pharmaceutical Group Ltd", "深港通", "主板", "710000", "社服"},
            {"02269", "药明生物", "WuXi Biologics Cayman Inc", "深港通", "主板", "710000", "社服"}
        };
        
        for (Object[] data : stockData) {
            HkConnectStock stock = new HkConnectStock();
            stock.setStockCode((String) data[0]);
            stock.setStockNameCn((String) data[1]);
            stock.setStockNameEn((String) data[2]);
            stock.setConnectType((String) data[3]);
            stock.setBoardType((String) data[4]);
            stock.setIndustryCode((String) data[5]);
            stock.setIndustryName((String) data[6]);
            
            // 设置基础信息
            stock.setMarketType("港股");
            stock.setTradingCurrency("HKD");
            stock.setIsActive(true);
            stock.setIsSuspended(false);
            
            // 随机生成上市和纳入日期
            stock.setListingDate(LocalDate.of(1990 + random.nextInt(30), 
                                              1 + random.nextInt(12), 
                                              1 + random.nextInt(28)));
            stock.setInclusionDate(LocalDate.of(2014 + random.nextInt(8), 
                                                1 + random.nextInt(12), 
                                                1 + random.nextInt(28)));
            
            // 股本信息 (1-500亿股)
            BigDecimal totalShares = BigDecimal.valueOf(10000 + random.nextDouble() * 4990000);
            stock.setTotalShares(totalShares);
            stock.setCirculatingShares(totalShares.multiply(BigDecimal.valueOf(0.7 + random.nextDouble() * 0.3)));
            
            // 股价信息 (5-800港币)
            BigDecimal priceHkd = BigDecimal.valueOf(5 + random.nextDouble() * 795);
            stock.setLatestPriceHkd(priceHkd);
            
            // 汇率 (0.85-0.95)
            BigDecimal exchangeRate = BigDecimal.valueOf(0.85 + random.nextDouble() * 0.1);
            stock.setExchangeRateHkdRmb(exchangeRate);
            stock.setLatestPriceRmb(priceHkd.multiply(exchangeRate));
            
            // 市值
            stock.setMarketValueHkd(totalShares.multiply(priceHkd));
            stock.setMarketValueRmb(totalShares.multiply(stock.getLatestPriceRmb()));
            
            // 财务指标
            stock.setPeRatio(BigDecimal.valueOf(3 + random.nextDouble() * 47));
            stock.setPbRatio(BigDecimal.valueOf(0.3 + random.nextDouble() * 9.7));
            stock.setDividendYield(BigDecimal.valueOf(random.nextDouble() * 0.12));
            
            // 北向资金数据
            double northboundInflow = -50000 + random.nextDouble() * 250000;
            stock.setNorthboundNetInflow(BigDecimal.valueOf(Math.round(northboundInflow * 100.0) / 100.0));
            stock.setNorthboundHoldingRatio(BigDecimal.valueOf(random.nextDouble() * 0.3));
            
            // 成交额数据
            double turnoverHkd = 1000 + random.nextDouble() * 500000;
            stock.setDailyTurnoverHkd(BigDecimal.valueOf(Math.round(turnoverHkd * 100.0) / 100.0));
            stock.setDailyTurnoverRmb(stock.getDailyTurnoverHkd().multiply(exchangeRate));
            
            // 额度使用率
            stock.setDailyQuotaUsage(BigDecimal.valueOf(random.nextDouble()));
            
            // 每手股数 (100-2000)
            stock.setLotSize(100 * (1 + random.nextInt(20)));
            
            stocks.add(stock);
        }
        
        return stocks;
    }
}