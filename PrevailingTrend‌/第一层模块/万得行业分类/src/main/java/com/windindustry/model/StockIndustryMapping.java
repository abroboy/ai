package com.windindustry.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "l1_wind_stock_industry_mapping")
public class StockIndustryMapping {
    
    @Id
    @Column(name = "stock_code")
    private String stockCode;
    
    @Column(name = "stock_name", nullable = false)
    private String stockName;
    
    @Column(name = "industry_code")
    private String industryCode;
    
    @Column(name = "industry_name")
    private String industryName;
    
    @Column(name = "mapping_status")
    private String mappingStatus = "active";
    
    @Column(name = "confidence")
    private Double confidence = 0.0;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
    
    // Constructors
    public StockIndustryMapping() {}
    
    public StockIndustryMapping(String stockCode, String stockName, String industryCode, String industryName) {
        this.stockCode = stockCode;
        this.stockName = stockName;
        this.industryCode = industryCode;
        this.industryName = industryName;
    }
    
    // Getters and Setters
    public String getStockCode() { return stockCode; }
    public void setStockCode(String stockCode) { this.stockCode = stockCode; }
    
    public String getStockName() { return stockName; }
    public void setStockName(String stockName) { this.stockName = stockName; }
    
    public String getIndustryCode() { return industryCode; }
    public void setIndustryCode(String industryCode) { this.industryCode = industryCode; }
    
    public String getIndustryName() { return industryName; }
    public void setIndustryName(String industryName) { this.industryName = industryName; }
    
    public String getMappingStatus() { return mappingStatus; }
    public void setMappingStatus(String mappingStatus) { this.mappingStatus = mappingStatus; }
    
    public Double getConfidence() { return confidence; }
    public void setConfidence(Double confidence) { this.confidence = confidence; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
