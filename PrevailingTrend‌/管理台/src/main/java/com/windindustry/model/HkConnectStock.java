package com.windindustry.model;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 港股通股票信息实体类
 * 包含港股通标的股票的详细信息
 */
@Entity
@Table(name = "l1_hk_connect_stock")
public class HkConnectStock {
    
    @Id
    @Column(name = "stock_code")
    private String stockCode; // 港股代码，如 00700
    
    @Column(name = "stock_name_cn")
    private String stockNameCn; // 中文名称
    
    @Column(name = "stock_name_en")
    private String stockNameEn; // 英文名称
    
    @Column(name = "connect_type")
    private String connectType; // 沪港通、深港通
    
    @Column(name = "inclusion_date")
    private LocalDate inclusionDate; // 纳入日期
    
    @Column(name = "market_type")
    private String marketType = "港股"; // 市场类型
    
    @Column(name = "board_type")
    private String boardType; // 主板、创业板等
    
    @Column(name = "industry_code")
    private String industryCode;
    
    @Column(name = "industry_name")
    private String industryName;
    
    @Column(name = "sector_code")
    private String sectorCode;
    
    @Column(name = "sector_name")
    private String sectorName;
    
    @Column(name = "listing_date")
    private LocalDate listingDate; // 港交所上市日期
    
    @Column(name = "total_shares", precision = 20, scale = 2)
    private BigDecimal totalShares; // 总股本(万股)
    
    @Column(name = "circulating_shares", precision = 20, scale = 2)
    private BigDecimal circulatingShares; // 流通股本(万股)
    
    @Column(name = "latest_price_hkd", precision = 10, scale = 3)
    private BigDecimal latestPriceHkd; // 最新价格(港币)
    
    @Column(name = "latest_price_rmb", precision = 10, scale = 3)
    private BigDecimal latestPriceRmb; // 最新价格(人民币)
    
    @Column(name = "market_value_hkd", precision = 20, scale = 2)
    private BigDecimal marketValueHkd; // 市值(港币万元)
    
    @Column(name = "market_value_rmb", precision = 20, scale = 2)
    private BigDecimal marketValueRmb; // 市值(人民币万元)
    
    @Column(name = "pe_ratio", precision = 8, scale = 2)
    private BigDecimal peRatio; // 市盈率
    
    @Column(name = "pb_ratio", precision = 8, scale = 2)
    private BigDecimal pbRatio; // 市净率
    
    @Column(name = "dividend_yield", precision = 8, scale = 4)
    private BigDecimal dividendYield; // 股息率
    
    @Column(name = "northbound_net_inflow", precision = 20, scale = 2)
    private BigDecimal northboundNetInflow; // 北向资金净流入(万元)
    
    @Column(name = "northbound_holding_ratio", precision = 8, scale = 4)
    private BigDecimal northboundHoldingRatio; // 北向持股比例
    
    @Column(name = "daily_turnover_hkd", precision = 20, scale = 2)
    private BigDecimal dailyTurnoverHkd; // 日成交额(港币万元)
    
    @Column(name = "daily_turnover_rmb", precision = 20, scale = 2)
    private BigDecimal dailyTurnoverRmb; // 日成交额(人民币万元)
    
    @Column(name = "daily_quota_usage", precision = 8, scale = 4)
    private BigDecimal dailyQuotaUsage; // 每日额度使用率
    
    @Column(name = "exchange_rate_hkd_rmb", precision = 8, scale = 4)
    private BigDecimal exchangeRateHkdRmb; // 港币人民币汇率
    
    @Column(name = "is_active")
    private Boolean isActive = true; // 是否在港股通名单中
    
    @Column(name = "is_suspended")
    private Boolean isSuspended = false; // 是否停牌
    
    @Column(name = "risk_warning")
    private String riskWarning; // 风险警示
    
    @Column(name = "trading_currency")
    private String tradingCurrency = "HKD"; // 交易货币
    
    @Column(name = "lot_size")
    private Integer lotSize; // 每手股数
    
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
    public HkConnectStock() {}
    
    public HkConnectStock(String stockCode, String stockNameCn, String connectType) {
        this.stockCode = stockCode;
        this.stockNameCn = stockNameCn;
        this.connectType = connectType;
    }
    
    // Getters and Setters
    public String getStockCode() { return stockCode; }
    public void setStockCode(String stockCode) { this.stockCode = stockCode; }
    
    public String getStockNameCn() { return stockNameCn; }
    public void setStockNameCn(String stockNameCn) { this.stockNameCn = stockNameCn; }
    
    public String getStockNameEn() { return stockNameEn; }
    public void setStockNameEn(String stockNameEn) { this.stockNameEn = stockNameEn; }
    
    public String getConnectType() { return connectType; }
    public void setConnectType(String connectType) { this.connectType = connectType; }
    
    public LocalDate getInclusionDate() { return inclusionDate; }
    public void setInclusionDate(LocalDate inclusionDate) { this.inclusionDate = inclusionDate; }
    
    public String getMarketType() { return marketType; }
    public void setMarketType(String marketType) { this.marketType = marketType; }
    
    public String getBoardType() { return boardType; }
    public void setBoardType(String boardType) { this.boardType = boardType; }
    
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
    
    public BigDecimal getTotalShares() { return totalShares; }
    public void setTotalShares(BigDecimal totalShares) { this.totalShares = totalShares; }
    
    public BigDecimal getCirculatingShares() { return circulatingShares; }
    public void setCirculatingShares(BigDecimal circulatingShares) { this.circulatingShares = circulatingShares; }
    
    public BigDecimal getLatestPriceHkd() { return latestPriceHkd; }
    public void setLatestPriceHkd(BigDecimal latestPriceHkd) { this.latestPriceHkd = latestPriceHkd; }
    
    public BigDecimal getLatestPriceRmb() { return latestPriceRmb; }
    public void setLatestPriceRmb(BigDecimal latestPriceRmb) { this.latestPriceRmb = latestPriceRmb; }
    
    public BigDecimal getMarketValueHkd() { return marketValueHkd; }
    public void setMarketValueHkd(BigDecimal marketValueHkd) { this.marketValueHkd = marketValueHkd; }
    
    public BigDecimal getMarketValueRmb() { return marketValueRmb; }
    public void setMarketValueRmb(BigDecimal marketValueRmb) { this.marketValueRmb = marketValueRmb; }
    
    public BigDecimal getPeRatio() { return peRatio; }
    public void setPeRatio(BigDecimal peRatio) { this.peRatio = peRatio; }
    
    public BigDecimal getPbRatio() { return pbRatio; }
    public void setPbRatio(BigDecimal pbRatio) { this.pbRatio = pbRatio; }
    
    public BigDecimal getDividendYield() { return dividendYield; }
    public void setDividendYield(BigDecimal dividendYield) { this.dividendYield = dividendYield; }
    
    public BigDecimal getNorthboundNetInflow() { return northboundNetInflow; }
    public void setNorthboundNetInflow(BigDecimal northboundNetInflow) { this.northboundNetInflow = northboundNetInflow; }
    
    public BigDecimal getNorthboundHoldingRatio() { return northboundHoldingRatio; }
    public void setNorthboundHoldingRatio(BigDecimal northboundHoldingRatio) { this.northboundHoldingRatio = northboundHoldingRatio; }
    
    public BigDecimal getDailyTurnoverHkd() { return dailyTurnoverHkd; }
    public void setDailyTurnoverHkd(BigDecimal dailyTurnoverHkd) { this.dailyTurnoverHkd = dailyTurnoverHkd; }
    
    public BigDecimal getDailyTurnoverRmb() { return dailyTurnoverRmb; }
    public void setDailyTurnoverRmb(BigDecimal dailyTurnoverRmb) { this.dailyTurnoverRmb = dailyTurnoverRmb; }
    
    public BigDecimal getDailyQuotaUsage() { return dailyQuotaUsage; }
    public void setDailyQuotaUsage(BigDecimal dailyQuotaUsage) { this.dailyQuotaUsage = dailyQuotaUsage; }
    
    public BigDecimal getExchangeRateHkdRmb() { return exchangeRateHkdRmb; }
    public void setExchangeRateHkdRmb(BigDecimal exchangeRateHkdRmb) { this.exchangeRateHkdRmb = exchangeRateHkdRmb; }
    
    public Boolean getIsActive() { return isActive; }
    public void setIsActive(Boolean isActive) { this.isActive = isActive; }
    
    public Boolean getIsSuspended() { return isSuspended; }
    public void setIsSuspended(Boolean isSuspended) { this.isSuspended = isSuspended; }
    
    public String getRiskWarning() { return riskWarning; }
    public void setRiskWarning(String riskWarning) { this.riskWarning = riskWarning; }
    
    public String getTradingCurrency() { return tradingCurrency; }
    public void setTradingCurrency(String tradingCurrency) { this.tradingCurrency = tradingCurrency; }
    
    public Integer getLotSize() { return lotSize; }
    public void setLotSize(Integer lotSize) { this.lotSize = lotSize; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}