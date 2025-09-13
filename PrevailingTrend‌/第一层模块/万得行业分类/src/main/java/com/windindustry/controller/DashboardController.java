package com.windindustry.controller;

import com.windindustry.service.StockService;
import com.windindustry.service.DataCollectionService;
import com.windindustry.service.WindIndustryService;
import com.windindustry.service.WindStockMappingService;
import com.windindustry.service.ListedCompanyInfoService;
import com.windindustry.service.HkConnectStockService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
public class DashboardController {
    
    @Autowired
    private StockService stockService;
    
    @Autowired
    private DataCollectionService dataCollectionService;
    
    @Autowired
    private WindIndustryService windIndustryService;
    
    @Autowired
    private WindStockMappingService windStockMappingService;
    
    @Autowired
    private ListedCompanyInfoService listedCompanyInfoService;
    
    @Autowired
    private HkConnectStockService hkConnectStockService;
    
    @GetMapping("/")
    public String dashboard(Model model) {
        return "dashboard";
    }
    
    @GetMapping("/stock-mappings")
    public String stockMappings(Model model) {
        return "stock-mappings";
    }
    
    @GetMapping("/data-analysis")
    public String dataAnalysis(Model model) {
        return "data-analysis";
    }
    
    @GetMapping("/api/stats")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getStats() {
        try {
            Map<String, Object> stats = stockService.getStatistics();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", stats);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/industries")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getIndustries() {
        try {
            List<Map<String, Object>> industries = stockService.getIndustryStatistics();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", industries);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/stocks")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getStocks(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int page_size,
            @RequestParam(defaultValue = "stock_code") String sort_by,
            @RequestParam(defaultValue = "asc") String sort_order) {
        try {
            List<Map<String, Object>> stocks = stockService.getStocksWithFlowData(page, page_size, sort_by, sort_order);
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            
            Map<String, Object> data = new HashMap<>();
            data.put("stocks", stocks);
            data.put("total", stockService.getStatistics().get("total_stocks"));
            data.put("page", page);
            data.put("page_size", page_size);
            
            response.put("data", data);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/stock/{stockCode}")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getStockDetail(@PathVariable String stockCode) {
        try {
            Map<String, Object> stockDetail = stockService.getStockDetail(stockCode);
            if (stockDetail == null) {
                Map<String, Object> response = new HashMap<>();
                response.put("success", false);
                response.put("error", "股票不存在");
                return ResponseEntity.ok(response);
            }
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", stockDetail);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @PostMapping("/api/refresh")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> refreshData() {
        try {
            dataCollectionService.refreshData();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "数据刷新成功");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/wind-industries")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getWindIndustries() {
        try {
            List<com.windindustry.model.WindIndustryClassification> industries = windIndustryService.getAllIndustries();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", industries);
            response.put("total", industries.size());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/wind-industries/level/{level}")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getWindIndustriesByLevel(@PathVariable Integer level) {
        try {
            List<com.windindustry.model.WindIndustryClassification> industries = windIndustryService.getIndustriesByLevel(level);
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", industries);
            response.put("total", industries.size());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/wind-industries/stats")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getWindIndustryStats() {
        try {
            Map<String, Object> stats = windIndustryService.getIndustryStatistics();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", stats);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @PostMapping("/api/wind-industries/refresh")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> refreshWindIndustryData() {
        try {
            dataCollectionService.refreshWindIndustryData();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "万得行业数据刷新成功");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/health")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> healthCheck() {
        Map<String, Object> response = new HashMap<>();
        response.put("status", "ok");
        response.put("message", "万得行业分类仪表盘运行正常");
        return ResponseEntity.ok(response);
    }
    
    // ========== 股票映射管理 API ==========
    
    @GetMapping("/api/stock-mappings")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getStockMappings(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String sortDir,
            @RequestParam(required = false) String stockCode,
            @RequestParam(required = false) String stockName,
            @RequestParam(required = false) String marketType,
            @RequestParam(required = false) String mappingStatus,
            @RequestParam(required = false) String industryCode) {
        try {
            org.springframework.data.domain.Page<com.windindustry.model.WindStockMapping> stocks = 
                windStockMappingService.getStockMappings(page, size, sortBy, sortDir, 
                                                       stockCode, stockName, marketType, mappingStatus, industryCode);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            
            Map<String, Object> data = new HashMap<>();
            data.put("content", stocks.getContent());
            data.put("totalElements", stocks.getTotalElements());
            data.put("totalPages", stocks.getTotalPages());
            data.put("currentPage", stocks.getNumber());
            data.put("size", stocks.getSize());
            data.put("numberOfElements", stocks.getNumberOfElements());
            data.put("hasNext", stocks.hasNext());
            data.put("hasPrevious", stocks.hasPrevious());
            
            response.put("data", data);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/stock-mappings/stats")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getStockMappingStats() {
        try {
            Map<String, Object> stats = windStockMappingService.getStockMappingStats();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", stats);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @PostMapping("/api/stock-mappings/refresh")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> refreshStockMappingData() {
        try {
            windStockMappingService.refreshStockMappingData();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "股票映射数据刷新成功");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/stock-mappings/{stockCode}")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getStockMapping(@PathVariable String stockCode) {
        try {
            Optional<com.windindustry.model.WindStockMapping> stockOpt = windStockMappingService.getStockMappingByCode(stockCode);
            
            if (stockOpt.isPresent()) {
                Map<String, Object> response = new HashMap<>();
                response.put("success", true);
                response.put("data", stockOpt.get());
                return ResponseEntity.ok(response);
            } else {
                Map<String, Object> response = new HashMap<>();
                response.put("success", false);
                response.put("error", "股票不存在");
                return ResponseEntity.ok(response);
            }
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @PutMapping("/api/stock-mappings/{stockCode}")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> updateStockMapping(@PathVariable String stockCode, @RequestBody Map<String, Object> stockData) {
        try {
            Optional<com.windindustry.model.WindStockMapping> stockOpt = windStockMappingService.getStockMappingByCode(stockCode);
            
            if (stockOpt.isPresent()) {
                com.windindustry.model.WindStockMapping stock = stockOpt.get();
                
                // 更新字段
                if (stockData.containsKey("stockName")) {
                    stock.setStockName((String) stockData.get("stockName"));
                }
                if (stockData.containsKey("marketType")) {
                    stock.setMarketType((String) stockData.get("marketType"));
                }
                if (stockData.containsKey("mappingStatus")) {
                    stock.setMappingStatus((String) stockData.get("mappingStatus"));
                }
                if (stockData.containsKey("industryCode") && stockData.get("industryCode") != null) {
                    String industryCode = (String) stockData.get("industryCode");
                    stock.setIndustryCode(industryCode);
                    
                    // 同时更新行业名称
                    Optional<com.windindustry.model.WindIndustryClassification> industryOpt = 
                        windIndustryService.getIndustryByCode(industryCode);
                    if (industryOpt.isPresent()) {
                        stock.setIndustryName(industryOpt.get().getIndustryName());
                    }
                }
                if (stockData.containsKey("totalMarketValue") && stockData.get("totalMarketValue") != null) {
                    Object value = stockData.get("totalMarketValue");
                    if (value instanceof Number) {
                        stock.setTotalMarketValue(java.math.BigDecimal.valueOf(((Number) value).doubleValue()));
                    }
                }
                if (stockData.containsKey("dailyNetInflow") && stockData.get("dailyNetInflow") != null) {
                    Object value = stockData.get("dailyNetInflow");
                    if (value instanceof Number) {
                        stock.setDailyNetInflow(java.math.BigDecimal.valueOf(((Number) value).doubleValue()));
                    }
                }
                
                stock.setLastUpdated(java.time.LocalDateTime.now());
                
                com.windindustry.model.WindStockMapping savedStock = windStockMappingService.saveStockMapping(stock);
                
                Map<String, Object> response = new HashMap<>();
                response.put("success", true);
                response.put("message", "股票信息更新成功");
                response.put("data", savedStock);
                return ResponseEntity.ok(response);
            } else {
                Map<String, Object> response = new HashMap<>();
                response.put("success", false);
                response.put("error", "股票不存在");
                return ResponseEntity.ok(response);
            }
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @DeleteMapping("/api/stock-mappings/{stockCode}")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> deleteStockMapping(@PathVariable String stockCode) {
        try {
            Optional<com.windindustry.model.WindStockMapping> stockOpt = windStockMappingService.getStockMappingByCode(stockCode);
            
            if (stockOpt.isPresent()) {
                windStockMappingService.deleteStockMapping(stockOpt.get().getId());
                
                Map<String, Object> response = new HashMap<>();
                response.put("success", true);
                response.put("message", "股票删除成功");
                return ResponseEntity.ok(response);
            } else {
                Map<String, Object> response = new HashMap<>();
                response.put("success", false);
                response.put("error", "股票不存在");
                return ResponseEntity.ok(response);
            }
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    // ========== 上市公司信息 API ==========
    
    @GetMapping("/api/listed-companies")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getListedCompanies(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(defaultValue = "stockCode") String sortBy,
            @RequestParam(defaultValue = "asc") String sortDir,
            @RequestParam(required = false) String stockCode,
            @RequestParam(required = false) String stockName,
            @RequestParam(required = false) String companyName,
            @RequestParam(required = false) String marketType,
            @RequestParam(required = false) String industryCode,
            @RequestParam(required = false) Boolean isActive) {
        try {
            org.springframework.data.domain.Page<com.windindustry.model.ListedCompanyInfo> companies = 
                listedCompanyInfoService.getCompanies(page, size, sortBy, sortDir, 
                                                     stockCode, stockName, companyName, marketType, industryCode, isActive);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            
            Map<String, Object> data = new HashMap<>();
            data.put("content", companies.getContent());
            data.put("totalElements", companies.getTotalElements());
            data.put("totalPages", companies.getTotalPages());
            data.put("currentPage", companies.getNumber());
            data.put("size", companies.getSize());
            
            response.put("data", data);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/listed-companies/stats")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getListedCompanyStats() {
        try {
            Map<String, Object> stats = listedCompanyInfoService.getCompanyStatistics();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", stats);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @PostMapping("/api/listed-companies/refresh")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> refreshListedCompanyData() {
        try {
            listedCompanyInfoService.refreshCompanyData();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "上市公司数据刷新成功");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    // ========== 港股通 API ==========
    
    @GetMapping("/api/hk-connect-stocks")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getHkConnectStocks(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(defaultValue = "stockCode") String sortBy,
            @RequestParam(defaultValue = "asc") String sortDir,
            @RequestParam(required = false) String stockCode,
            @RequestParam(required = false) String stockNameCn,
            @RequestParam(required = false) String connectType,
            @RequestParam(required = false) String industryCode,
            @RequestParam(required = false) Boolean isActive) {
        try {
            org.springframework.data.domain.Page<com.windindustry.model.HkConnectStock> stocks = 
                hkConnectStockService.getHkConnectStocks(page, size, sortBy, sortDir, 
                                                       stockCode, stockNameCn, connectType, industryCode, isActive);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            
            Map<String, Object> data = new HashMap<>();
            data.put("content", stocks.getContent());
            data.put("totalElements", stocks.getTotalElements());
            data.put("totalPages", stocks.getTotalPages());
            data.put("currentPage", stocks.getNumber());
            data.put("size", stocks.getSize());
            
            response.put("data", data);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/hk-connect-stocks/stats")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getHkConnectStats() {
        try {
            Map<String, Object> stats = hkConnectStockService.getHkConnectStatistics();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", stats);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @PostMapping("/api/hk-connect-stocks/refresh")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> refreshHkConnectData() {
        try {
            hkConnectStockService.refreshHkConnectData();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "港股通数据刷新成功");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    // ========== 数据分析 API ==========
    
    @GetMapping("/api/capital-flow/stats")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getCapitalFlowStats() {
        try {
            Map<String, Object> stats = windStockMappingService.getCapitalFlowStatistics();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", stats);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/industry/flow-ranking")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getIndustryFlowRanking(
            @RequestParam(defaultValue = "10") int limit,
            @RequestParam(defaultValue = "desc") String order) {
        try {
            List<Map<String, Object>> ranking = windStockMappingService.getIndustryFlowRanking(limit, order);
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", ranking);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/stock/flow-ranking")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getStockFlowRanking(
            @RequestParam(defaultValue = "20") int limit,
            @RequestParam(defaultValue = "desc") String order,
            @RequestParam(defaultValue = "daily") String period) {
        try {
            List<Map<String, Object>> ranking = windStockMappingService.getStockFlowRanking(limit, order, period);
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", ranking);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/market/distribution")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getMarketDistribution() {
        try {
            List<Map<String, Object>> distribution = windStockMappingService.getMarketTypeStats();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", distribution);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/industry/distribution")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getIndustryDistribution() {
        try {
            List<Map<String, Object>> distribution = windStockMappingService.getIndustryStats();
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", distribution);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
    
    @GetMapping("/api/capital-flow/trend")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getCapitalFlowTrend(
            @RequestParam(defaultValue = "7") int days) {
        try {
            List<Map<String, Object>> trend = windStockMappingService.getCapitalFlowTrend(days);
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("data", trend);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.ok(response);
        }
    }
}
