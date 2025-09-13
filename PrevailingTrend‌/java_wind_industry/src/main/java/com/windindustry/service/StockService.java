package com.windindustry.service;

import com.windindustry.model.StockIndustryMapping;
import com.windindustry.repository.StockIndustryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class StockService {

    @Autowired
    private StockIndustryRepository repository;

    public List<Map<String, Object>> getStocks(int page, int pageSize, String sortBy, String sortOrder) {
        int offset = (page - 1) * pageSize;
        List<Object[]> results = repository.getStocksWithFlow(sortBy, sortOrder, pageSize, offset);
        return results.stream().map(this::convertToMap).collect(Collectors.toList());
    }

    private Map<String, Object> convertToMap(Object[] row) {
        // Convert array to map with keys
        return Map.of(
                "stock_code", row[0],
                "stock_name", row[1],
                "industry_code", row[2],
                "industry_name", row[3],
                "mapping_status", row[4],
                "confidence", row[5],
                "created_at", row[6],
                "updated_at", row[7],
                "total_net_flow", row[8],
                "avg_net_flow", row[9],
                "flow_ratio", row[10],
                "prediction_score", calculatePredictionScore((Double) row[9], (Double) row[10]), // 自定义预测公式
                "recent_flow", row[12],
                "flow_days", row[13]
        );
    }

    private double calculatePredictionScore(double avgNetFlow, double flowRatio) {
        // 自定义公式：预测分数 = (avgNetFlow / 1000000) * flowRatio * 0.5 (范围0-1)
        double score = (avgNetFlow / 1000000) * flowRatio * 0.5;
        return Math.min(1.0, Math.max(0.0, score));
    }

    // 其他方法，如从AKShare替代库获取数据
    public void fetchAndSaveData() {
        // 使用HttpClient或Tushare Java SDK获取数据并保存到数据库
        // 实现略
    }
} 