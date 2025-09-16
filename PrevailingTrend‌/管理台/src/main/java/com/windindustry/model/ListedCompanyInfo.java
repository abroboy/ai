package com.windindustry.model;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 上市公司基本信息实体类
 * 包含上市公司的基础信息、财务指标等
 */
@Entity
@Table(name = "l1_listed_company_info")
public class ListedCompanyInfo {
    
    @Id
    @Column(name = "stock_code")
    private String stockCode;
    
    @Column(name = "company_name", nullable = false)
    private String companyName;
    
    @Column(name = "stock_name", nullable = false)
    private String stockName;
    
    @Column(name = "market_type")
    private String marketType; // A股、港股、科创板、创业板等
    
    @Column(name = "exchange_code")
    private String exchangeCode; // SH、SZ、HK等
    
    @Column(name = "industry_code")
    private String industryCode;
    
    @Column(name = "industry_name")
    private String industryName;
    
    @Column(name = "sector_code")
    private String sectorCode; // 板块代码
    
    @Column(name = "sector_name")
    private String sectorName; // 板块名称
    
    @Column(name = "listing_date")
    private LocalDate listingDate; // 上市日期
    
    @Column(name = "total_share_capital", precision = 20, scale = 2)
    private BigDecimal totalShareCapital; // 总股本(万股)
    
    @Column(name = "circulating_share_capital", precision = 20, scale = 2)
    private BigDecimal circulatingShareCapital; // 流通股本(万股)
    
    @Column(name = "total_market_value", precision = 20, scale = 2)
    private BigDecimal totalMarketValue; // 总市值(万元)
    
    @Column(name = "circulating_market_value", precision = 20, scale = 2)
    private BigDecimal circulatingMarketValue; // 流通市值(万元)
    
    @Column(name = "latest_price", precision = 10, scale = 3)
    private BigDecimal latestPrice; // 最新价格
    
    @Column(name = "pe_ratio", precision = 8, scale = 2)
    private BigDecimal peRatio; // 市盈率
    
    @Column(name = "pb_ratio", precision = 8, scale = 2)
    private BigDecimal pbRatio; // 市净率
    
    @Column(name = "eps", precision = 8, scale = 3)
    private BigDecimal eps; // 每股收益
    
    @Column(name = "bps", precision = 8, scale = 3)
    private BigDecimal bps; // 每股净资产
    
    @Column(name = "roe", precision = 8, scale = 4)
    private BigDecimal roe; // 净资产收益率
    
    @Column(name = "roa", precision = 8, scale = 4)
    private BigDecimal roa; // 资产收益率
    
    @Column(name = "dividend_yield", precision = 8, scale = 4)
    private BigDecimal dividendYield; // 股息率
    
    @Column(name = "is_st")
    private Boolean isSt = false; // 是否ST股票
    
    @Column(name = "is_suspended")
    private Boolean isSuspended = false; // 是否停牌
    
    @Column(name = "is_active")
    private Boolean isActive = true; // 是否活跃
    
    @Column(name = "business_scope", columnDefinition = "TEXT")
    private String businessScope; // 经营范围
    
    @Column(name = "company_address")
    private String companyAddress; // 公司地址
    
    @Column(name = "registered_capital", precision = 20, scale = 2)
    private BigDecimal registeredCapital; // 注册资本(万元)
    
    @Column(name = "employee_count")
    private Integer employeeCount; // 员工人数
    
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
    public ListedCompanyInfo() {}
    
    public ListedCompanyInfo(String stockCode, String companyName, String stockName) {
        this.stockCode = stockCode;
        this.companyName = companyName;
        this.stockName = stockName;
    }
    
    // Getters and Setters
    public String getStockCode() { return stockCode; }
    public void setStockCode(String stockCode) { this.stockCode = stockCode; }
    
    public String getCompanyName() { return companyName; }
    public void setCompanyName(String companyName) { this.companyName = companyName; }
    
    public String getStockName() { return stockName; }
    public void setStockName(String stockName) { this.stockName = stockName; }
    
    public String getMarketType() { return marketType; }
    public void setMarketType(String marketType) { this.marketType = marketType; }
    
    public String getExchangeCode() { return exchangeCode; }
    public void setExchangeCode(String exchangeCode) { this.exchangeCode = exchangeCode; }
    
    public String getIndustryCode() { return industryCode; }
    public void setIndustryCode(String industryCode) { this.industryCode = industryCode; }
    
    public String getIndustryName() { return industryName; }
    public void setIndustryName(String industryName) { this.industryName = industryName; }
    
    public String getSectorCode() { return sectorCode; }
    public void setSectorCode(String sectorCode) { this.sectorCode = sectorCode; }
    
    public String getSectorName() { return sectorName; }
    public void setSectorName(String sectorName) { this.sectorName = sectorName; }
    
    public LocalDate getListingDate() { return listingDate; }
    public void setListingDate(LocalDate listingDate) { this.listingDate = listingDate; }
    
    public BigDecimal getTotalShareCapital() { return totalShareCapital; }
    public void setTotalShareCapital(BigDecimal totalShareCapital) { this.totalShareCapital = totalShareCapital; }
    
    public BigDecimal getCirculatingShareCapital() { return circulatingShareCapital; }
    public void setCirculatingShareCapital(BigDecimal circulatingShareCapital) { this.circulatingShareCapital = circulatingShareCapital; }
    
    public BigDecimal getTotalMarketValue() { return totalMarketValue; }
    public void setTotalMarketValue(BigDecimal totalMarketValue) { this.totalMarketValue = totalMarketValue; }
    
    public BigDecimal getCirculatingMarketValue() { return circulatingMarketValue; }
    public void setCirculatingMarketValue(BigDecimal circulatingMarketValue) { this.circulatingMarketValue = circulatingMarketValue; }
    
    public BigDecimal getLatestPrice() { return latestPrice; }
    public void setLatestPrice(BigDecimal latestPrice) { this.latestPrice = latestPrice; }
    
    public BigDecimal getPeRatio() { return peRatio; }
    public void setPeRatio(BigDecimal peRatio) { this.peRatio = peRatio; }
    
    public BigDecimal getPbRatio() { return pbRatio; }
    public void setPbRatio(BigDecimal pbRatio) { this.pbRatio = pbRatio; }
    
    public BigDecimal getEps() { return eps; }
    public void setEps(BigDecimal eps) { this.eps = eps; }
    
    public BigDecimal getBps() { return bps; }
    public void setBps(BigDecimal bps) { this.bps = bps; }
    
    public BigDecimal getRoe() { return roe; }
    public void setRoe(BigDecimal roe) { this.roe = roe; }
    
    public BigDecimal getRoa() { return roa; }
    public void setRoa(BigDecimal roa) { this.roa = roa; }
    
    public BigDecimal getDividendYield() { return dividendYield; }
    public void setDividendYield(BigDecimal dividendYield) { this.dividendYield = dividendYield; }
    
    public Boolean getIsSt() { return isSt; }
    public void setIsSt(Boolean isSt) { this.isSt = isSt; }
    
    public Boolean getIsSuspended() { return isSuspended; }
    public void setIsSuspended(Boolean isSuspended) { this.isSuspended = isSuspended; }
    
    public Boolean getIsActive() { return isActive; }
    public void setIsActive(Boolean isActive) { this.isActive = isActive; }
    
    public String getBusinessScope() { return businessScope; }
    public void setBusinessScope(String businessScope) { this.businessScope = businessScope; }
    
    public String getCompanyAddress() { return companyAddress; }
    public void setCompanyAddress(String companyAddress) { this.companyAddress = companyAddress; }
    
    public BigDecimal getRegisteredCapital() { return registeredCapital; }
    public void setRegisteredCapital(BigDecimal registeredCapital) { this.registeredCapital = registeredCapital; }
    
    public Integer getEmployeeCount() { return employeeCount; }
    public void setEmployeeCount(Integer employeeCount) { this.employeeCount = employeeCount; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}