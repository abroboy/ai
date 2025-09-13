package com.windindustry.service;

import com.windindustry.model.WindStockMapping;
import com.windindustry.model.WindIndustryClassification;
import com.windindustry.repository.WindStockMappingRepository;
import com.windindustry.repository.WindIndustryClassificationRepository;
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

@Service
public class WindStockMappingService {
    
    @Autowired
    private WindStockMappingRepository windStockMappingRepository;
    
    @Autowired
    private WindIndustryClassificationRepository windIndustryRepository;
    
    public Map<String, Object> getStockMappingStats() {
        Map<String, Object> stats = new HashMap<>();
        
        long totalStocks = windStockMappingRepository.count();
        Long mappedCount = windStockMappingRepository.countByMappingStatus("已映射");
        Long unmappedCount = windStockMappingRepository.countByMappingStatus("未映射");
        Long aStockCount = windStockMappingRepository.countByMarketType("A股");
        Long kcStockCount = windStockMappingRepository.countByMarketType("科创板");
        
        stats.put("total_stocks", totalStocks);
        stats.put("mapped_count", mappedCount != null ? mappedCount : 0);
        stats.put("unmapped_count", unmappedCount != null ? unmappedCount : 0);
        stats.put("a_stock_count", aStockCount != null ? aStockCount : 0);
        stats.put("kc_stock_count", kcStockCount != null ? kcStockCount : 0);
        
        return stats;
    }
    
    public Page<WindStockMapping> getStockMappings(int page, int size, String sortBy, String sortDir, 
                                                   String stockCode, String stockName, String marketType, 
                                                   String mappingStatus, String industryCode) {
        
        Sort sort = Sort.by(Sort.Direction.fromString(sortDir), sortBy != null ? sortBy : "id");
        Pageable pageable = PageRequest.of(page, size, sort);
        
        return windStockMappingRepository.findByFilters(stockCode, stockName, marketType, mappingStatus, industryCode, pageable);
    }
    
    public List<Map<String, Object>> getMappingStatusStats() {
        List<Object[]> results = windStockMappingRepository.getMappingStatusStats();
        List<Map<String, Object>> stats = new ArrayList<>();
        
        for (Object[] result : results) {
            Map<String, Object> stat = new HashMap<>();
            stat.put("status", result[0]);
            stat.put("count", result[1]);
            stats.add(stat);
        }
        
        return stats;
    }
    
    public List<Map<String, Object>> getMarketTypeStats() {
        List<Object[]> results = windStockMappingRepository.getMarketTypeStats();
        List<Map<String, Object>> stats = new ArrayList<>();
        
        for (Object[] result : results) {
            Map<String, Object> stat = new HashMap<>();
            stat.put("market_type", result[0]);
            stat.put("count", result[1]);
            stats.add(stat);
        }
        
        return stats;
    }
    
    public List<Map<String, Object>> getIndustryStats() {
        List<Object[]> results = windStockMappingRepository.getIndustryStats();
        List<Map<String, Object>> stats = new ArrayList<>();
        
        for (Object[] result : results) {
            Map<String, Object> stat = new HashMap<>();
            stat.put("industry_name", result[0]);
            stat.put("count", result[1]);
            stats.add(stat);
        }
        
        return stats;
    }
    
    public Optional<WindStockMapping> getStockMappingByCode(String stockCode) {
        return windStockMappingRepository.findByStockCode(stockCode);
    }
    
    public WindStockMapping saveStockMapping(WindStockMapping stockMapping) {
        return windStockMappingRepository.save(stockMapping);
    }
    
    public void deleteStockMapping(Long id) {
        windStockMappingRepository.deleteById(id);
    }
    
    public void refreshStockMappingData() {
        System.out.println("开始刷新股票映射数据...");
        
        try {
            // 获取所有活跃的行业分类
            List<WindIndustryClassification> industries = windIndustryRepository.findByIsActiveTrue();
            
            // 获取所有股票映射
            List<WindStockMapping> stocks = windStockMappingRepository.findAll();
            
            // 更新资金流向数据
            for (WindStockMapping stock : stocks) {
                updateStockFlowData(stock);
                windStockMappingRepository.save(stock);
            }
            
            System.out.println("股票映射数据刷新完成，共更新 " + stocks.size() + " 只股票");
            
        } catch (Exception e) {
            System.err.println("刷新股票映射数据失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private void updateStockFlowData(WindStockMapping stock) {
        // 模拟更新资金流向数据
        Random random = ThreadLocalRandom.current();
        
        // 更新日资金净流入 (-10000 到 50000)
        double dailyInflow = -10000 + random.nextDouble() * 60000;
        stock.setDailyNetInflow(BigDecimal.valueOf(Math.round(dailyInflow * 100.0) / 100.0));
        
        // 更新流入比例 (-5% 到 8%)
        double inflowRatio = -5.0 + random.nextDouble() * 13.0;
        stock.setNetInflowRatio(BigDecimal.valueOf(Math.round(inflowRatio * 10000.0) / 10000.0));
        
        // 更新波动率 (1% 到 8%)
        double volatility = 0.01 + random.nextDouble() * 0.07;
        stock.setRecentVolatility(BigDecimal.valueOf(Math.round(volatility * 10000.0) / 10000.0));
        
        // 更新7日流入
        double weeklyInflow = dailyInflow * 7 + random.nextDouble() * 100000 - 50000;
        stock.setLatest7dInflow(BigDecimal.valueOf(Math.round(weeklyInflow * 100.0) / 100.0));
        
        // 更新总市值 (基于现有值进行小幅调整)
        if (stock.getTotalMarketValue() != null) {
            double currentValue = stock.getTotalMarketValue().doubleValue();
            double newValue = currentValue * (0.95 + random.nextDouble() * 0.1); // ±5%的变化
            stock.setTotalMarketValue(BigDecimal.valueOf(Math.round(newValue * 100.0) / 100.0));
        }
    }
    
    public void mapStockToIndustry(String stockCode, String industryCode) {
        Optional<WindStockMapping> stockOpt = windStockMappingRepository.findByStockCode(stockCode);
        if (stockOpt.isPresent()) {
            WindStockMapping stock = stockOpt.get();
            
            Optional<WindIndustryClassification> industryOpt = windIndustryRepository.findById(industryCode);
            if (industryOpt.isPresent()) {
                WindIndustryClassification industry = industryOpt.get();
                stock.setIndustryCode(industryCode);
                stock.setIndustryName(industry.getIndustryName());
                stock.setMappingStatus("已映射");
                windStockMappingRepository.save(stock);
            }
        }
    }
    
    // ========== 数据分析相关方法 ==========
    
    public Map<String, Object> getCapitalFlowStatistics() {
        Map<String, Object> stats = new HashMap<>();
        
        List<WindStockMapping> allStocks = windStockMappingRepository.findAll();
        
        double totalDailyInflow = 0;
        double totalWeeklyInflow = 0;
        int positiveFlowCount = 0;
        int negativeFlowCount = 0;
        
        for (WindStockMapping stock : allStocks) {
            if (stock.getDailyNetInflow() != null) {
                double dailyFlow = stock.getDailyNetInflow().doubleValue();
                totalDailyInflow += dailyFlow;
                
                if (dailyFlow > 0) {
                    positiveFlowCount++;
                } else if (dailyFlow < 0) {
                    negativeFlowCount++;
                }
            }
            
            if (stock.getLatest7dInflow() != null) {
                totalWeeklyInflow += stock.getLatest7dInflow().doubleValue();
            }
        }
        
        stats.put("total_daily_inflow", totalDailyInflow);
        stats.put("total_weekly_inflow", totalWeeklyInflow);
        stats.put("positive_flow_count", positiveFlowCount);
        stats.put("negative_flow_count", negativeFlowCount);
        stats.put("total_stocks", allStocks.size());
        stats.put("average_daily_inflow", allStocks.size() > 0 ? totalDailyInflow / allStocks.size() : 0);
        
        return stats;
    }
    
    public List<Map<String, Object>> getIndustryFlowRanking(int limit, String order) {
        List<Object[]> results = windStockMappingRepository.getIndustryFlowRanking(limit, order);
        List<Map<String, Object>> ranking = new ArrayList<>();
        
        for (Object[] result : results) {
            Map<String, Object> item = new HashMap<>();
            item.put("industry_name", result[0]);
            item.put("stock_count", result[1]);
            item.put("total_inflow", result[2]);
            item.put("average_inflow", result[3]);
            ranking.add(item);
        }
        
        return ranking;
    }
    
    public List<Map<String, Object>> getStockFlowRanking(int limit, String order, String period) {
        List<WindStockMapping> stocks;
        
        if ("weekly".equals(period)) {
            if ("desc".equals(order)) {
                stocks = windStockMappingRepository.findTopByLatest7dInflowDesc(PageRequest.of(0, limit));
            } else {
                stocks = windStockMappingRepository.findTopByLatest7dInflowAsc(PageRequest.of(0, limit));
            }
        } else {
            if ("desc".equals(order)) {
                stocks = windStockMappingRepository.findTopByDailyNetInflowDesc(PageRequest.of(0, limit));
            } else {
                stocks = windStockMappingRepository.findTopByDailyNetInflowAsc(PageRequest.of(0, limit));
            }
        }
        
        List<Map<String, Object>> ranking = new ArrayList<>();
        
        for (int i = 0; i < stocks.size(); i++) {
            WindStockMapping stock = stocks.get(i);
            Map<String, Object> item = new HashMap<>();
            item.put("rank", i + 1);
            item.put("stock_code", stock.getStockCode());
            item.put("stock_name", stock.getStockName());
            item.put("industry_name", stock.getIndustryName());
            item.put("market_type", stock.getMarketType());
            item.put("daily_net_inflow", stock.getDailyNetInflow());
            item.put("latest_7d_inflow", stock.getLatest7dInflow());
            item.put("net_inflow_ratio", stock.getNetInflowRatio());
            ranking.add(item);
        }
        
        return ranking;
    }
    
    public List<Map<String, Object>> getCapitalFlowTrend(int days) {
        // 模拟生成资金流向趋势数据
        List<Map<String, Object>> trend = new ArrayList<>();
        Random random = ThreadLocalRandom.current();
        
        LocalDate endDate = LocalDate.now();
        LocalDate startDate = endDate.minusDays(days - 1);
        
        for (LocalDate date = startDate; !date.isAfter(endDate); date = date.plusDays(1)) {
            Map<String, Object> item = new HashMap<>();
            item.put("date", date.toString());
            
            // 模拟数据
            double baseInflow = 50000 + random.nextDouble() * 200000 - 100000;
            double totalInflow = baseInflow + (random.nextDouble() - 0.5) * 50000;
            double totalOutflow = Math.abs(baseInflow) * 0.8 + (random.nextDouble() - 0.5) * 30000;
            
            item.put("total_inflow", Math.round(totalInflow * 100.0) / 100.0);
            item.put("total_outflow", Math.round(totalOutflow * 100.0) / 100.0);
            item.put("net_inflow", Math.round((totalInflow - totalOutflow) * 100.0) / 100.0);
            
            trend.add(item);
        }
        
        return trend;
    }
}