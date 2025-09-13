package com.windindustry.controller;

import com.windindustry.service.StockService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
public class StockApiController {

    @Autowired
    private StockService stockService;

    @GetMapping("/api/stocks")
    public Map<String, Object> getStocks(@RequestParam(defaultValue = "1") int page,
                                         @RequestParam(defaultValue = "20") int pageSize,
                                         @RequestParam(defaultValue = "stock_code") String sortBy,
                                         @RequestParam(defaultValue = "asc") String sortOrder) {
        List<Map<String, Object>> stocks = stockService.getStocks(page, pageSize, sortBy, sortOrder);
        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        Map<String, Object> data = new HashMap<>();
        data.put("page", page);
        data.put("page_size", pageSize);
        data.put("stocks", stocks);
        data.put("total", stocks.size()); // 简化，实际应查询总条数
        response.put("data", data);
        response.put("message", "success");
        return response;
    }
} 