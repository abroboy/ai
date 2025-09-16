package com.windindustry.model;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "l1_wind_stock_mapping")
public class WindStockMapping {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "stock_code", unique = true, nullable = false)
    private String stockCode;
    
    @Column(name = "stock_name", nullable = false)
    private String stockName;
    
    @Column(name = "market_type")
    private String marketType = "A股";
    
    @Column(name = "industry_code")
    private String industryCode;
    
    @Column(name = "industry_name")
    private String industryName;
    
    @Column(name = "mapping_status")
    private String mappingStatus = "已映射";
    
    @Column(name = "total_market_value", precision = 20, scale = 2)
    private BigDecimal totalMarketValue;
    
    @Column(name = "daily_net_inflow", precision = 20, scale = 2)
    private BigDecimal dailyNetInflow;
    
    @Column(name = "net_inflow_ratio", precision = 8, scale = 4)
    private BigDecimal netInflowRatio;
    
    @Column(name = "recent_volatility", precision = 8, scale = 4)
    private BigDecimal recentVolatility;
    
    @Column(name = "latest_7d_inflow", precision = 20, scale = 2)
    private BigDecimal latest7dInflow;
    
    @Column(name = "last_updated")
    private LocalDateTime lastUpdated;
    
    @Column(name = "operation_status")
    private String operationStatus = "正常";
    
    @Column(name = "is_active")
    private Boolean isActive = true;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
        lastUpdated = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
        lastUpdated = LocalDateTime.now();
    }
    
    // Constructors
    public WindStockMapping() {}
    
    public WindStockMapping(String stockCode, String stockName) {
        this.stockCode = stockCode;
        this.stockName = stockName;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getStockCode() { return stockCode; }
    public void setStockCode(String stockCode) { this.stockCode = stockCode; }
    
    public String getStockName() { return stockName; }
    public void setStockName(String stockName) { this.stockName = stockName; }
    
    public String getMarketType() { return marketType; }
    public void setMarketType(String marketType) { this.marketType = marketType; }
    
    public String getIndustryCode() { return industryCode; }
    public void setIndustryCode(String industryCode) { this.industryCode = industryCode; }
    
    public String getIndustryName() { return industryName; }
    public void setIndustryName(String industryName) { this.industryName = industryName; }
    
    public String getMappingStatus() { return mappingStatus; }
    public void setMappingStatus(String mappingStatus) { this.mappingStatus = mappingStatus; }
    
    public BigDecimal getTotalMarketValue() { return totalMarketValue; }
    public void setTotalMarketValue(BigDecimal totalMarketValue) { this.totalMarketValue = totalMarketValue; }
    
    public BigDecimal getDailyNetInflow() { return dailyNetInflow; }
    public void setDailyNetInflow(BigDecimal dailyNetInflow) { this.dailyNetInflow = dailyNetInflow; }
    
    public BigDecimal getNetInflowRatio() { return netInflowRatio; }
    public void setNetInflowRatio(BigDecimal netInflowRatio) { this.netInflowRatio = netInflowRatio; }
    
    public BigDecimal getRecentVolatility() { return recentVolatility; }
    public void setRecentVolatility(BigDecimal recentVolatility) { this.recentVolatility = recentVolatility; }
    
    public BigDecimal getLatest7dInflow() { return latest7dInflow; }
    public void setLatest7dInflow(BigDecimal latest7dInflow) { this.latest7dInflow = latest7dInflow; }
    
    public LocalDateTime getLastUpdated() { return lastUpdated; }
    public void setLastUpdated(LocalDateTime lastUpdated) { this.lastUpdated = lastUpdated; }
    
    public String getOperationStatus() { return operationStatus; }
    public void setOperationStatus(String operationStatus) { this.operationStatus = operationStatus; }
    
    public Boolean getIsActive() { return isActive; }
    public void setIsActive(Boolean isActive) { this.isActive = isActive; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}