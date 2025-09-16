package com.windindustry.service;

import com.windindustry.model.StockIndustryMapping;
import com.windindustry.model.StockFlowData;
import com.windindustry.repository.StockIndustryRepository;
import com.windindustry.repository.StockFlowRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class StockService {
    
    @Autowired
    private StockIndustryRepository stockIndustryRepository;
    
    @Autowired
    private StockFlowRepository stockFlowRepository;
    
    public Map<String, Object> getStatistics() {
        Map<String, Object> stats = new HashMap<>();
        
        long totalStocks = stockIndustryRepository.count();
        Long totalIndustries = stockIndustryRepository.countDistinctIndustries();
        Long level1Count = stockIndustryRepository.countLevel1Industries();
        Long level2Count = stockIndustryRepository.countLevel2Industries();
        
        stats.put("total_stocks", totalStocks);
        stats.put("total_industries", totalIndustries != null ? totalIndustries : 0);
        stats.put("level_1_count", level1Count != null ? level1Count : 0);
        stats.put("level_2_count", level2Count != null ? level2Count : 0);
        
        return stats;
    }
    
    public List<Map<String, Object>> getIndustryStatistics() {
        List<Object[]> results = stockIndustryRepository.getIndustryStatistics();
        List<Map<String, Object>> industries = new ArrayList<>();
        
        for (Object[] result : results) {
            Map<String, Object> industry = new HashMap<>();
            industry.put("industry_code", result[0]);
            industry.put("industry_name", result[1]);
            industry.put("stock_count", result[2]);
            industry.put("level", result[3]);
            industries.add(industry);
        }
        
        return industries;
    }
    
    public List<Map<String, Object>> getStocksWithFlowData(int page, int size, String sortBy, String sortOrder) {
        List<StockIndustryMapping> stocks = stockIndustryRepository.findAll();
        List<Map<String, Object>> result = new ArrayList<>();
        
        for (StockIndustryMapping stock : stocks) {
            Map<String, Object> stockData = new HashMap<>();
            stockData.put("stock_code", stock.getStockCode());
            stockData.put("stock_name", stock.getStockName());
            stockData.put("industry_name", stock.getIndustryName());
            stockData.put("confidence", stock.getConfidence());
            
            Double avgNetFlow = stockFlowRepository.getAverageNetFlowByStockCode(stock.getStockCode());
            if (avgNetFlow == null) avgNetFlow = 0.0;
            stockData.put("avg_net_flow", Math.round(avgNetFlow * 100.0) / 100.0);
            
            double predictionScore = calculatePredictionScore(avgNetFlow, stock.getConfidence());
            stockData.put("prediction_score", Math.round(predictionScore * 100.0) / 100.0);
            
            result.add(stockData);
        }
        
        // 简单排序
        if ("prediction_score".equals(sortBy)) {
            result.sort((a, b) -> {
                double scoreA = (Double) a.get("prediction_score");
                double scoreB = (Double) b.get("prediction_score");
                return "desc".equals(sortOrder) ? Double.compare(scoreB, scoreA) : Double.compare(scoreA, scoreB);
            });
        }
        
        // 分页
        int start = (page - 1) * size;
        int end = Math.min(start + size, result.size());
        
        if (start >= result.size()) {
            return new ArrayList<>();
        }
        
        return result.subList(start, end);
    }
    
    public Map<String, Object> getStockDetail(String stockCode) {
        Optional<StockIndustryMapping> stockOpt = stockIndustryRepository.findById(stockCode);
        if (!stockOpt.isPresent()) {
            return null;
        }
        
        StockIndustryMapping stock = stockOpt.get();
        List<StockFlowData> flowData = stockFlowRepository.findByStockCodeOrderByTradeDateDesc(stockCode);
        Double avgNetFlow = stockFlowRepository.getAverageNetFlowByStockCode(stockCode);
        
        Map<String, Object> result = new HashMap<>();
        result.put("stock_info", stock);
        result.put("flow_data", flowData);
        result.put("avg_net_flow", avgNetFlow != null ? avgNetFlow : 0.0);
        
        return result;
    }
    
    private double calculatePredictionScore(double avgNetFlow, double confidence) {
        double baseScore;
        if (avgNetFlow > 0) {
            baseScore = 0.8;
        } else if (avgNetFlow < 0) {
            baseScore = 0.3;
        } else {
            baseScore = 0.5;
        }
        
        double adjustedScore = baseScore * confidence;
        return Math.max(0.0, Math.min(1.0, adjustedScore));
    }
}
