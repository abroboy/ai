package com.windindustry.model;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 股票资金流向数据实体类
 * 记录股票的每日资金流向信息
 */
@Entity
@Table(name = "l1_stock_capital_flow")
@IdClass(StockCapitalFlowId.class)
public class StockCapitalFlow {
    
    @Id
    @Column(name = "stock_code")
    private String stockCode;
    
    @Id
    @Column(name = "trade_date")
    private LocalDate tradeDate;
    
    @Column(name = "stock_name")
    private String stockName;
    
    @Column(name = "market_type")
    private String marketType;
    
    @Column(name = "close_price", precision = 10, scale = 3)
    private BigDecimal closePrice; // 收盘价
    
    @Column(name = "price_change", precision = 10, scale = 3)
    private BigDecimal priceChange; // 涨跌额
    
    @Column(name = "price_change_ratio", precision = 8, scale = 4)
    private BigDecimal priceChangeRatio; // 涨跌幅
    
    @Column(name = "turnover_amount", precision = 20, scale = 2)
    private BigDecimal turnoverAmount; // 成交额(万元)
    
    @Column(name = "turnover_volume", precision = 20, scale = 2)
    private BigDecimal turnoverVolume; // 成交量(万股)
    
    @Column(name = "main_net_inflow", precision = 20, scale = 2)
    private BigDecimal mainNetInflow; // 主力净流入(万元)
    
    @Column(name = "main_net_inflow_ratio", precision = 8, scale = 4)
    private BigDecimal mainNetInflowRatio; // 主力净流入占比
    
    @Column(name = "super_large_net_inflow", precision = 20, scale = 2)
    private BigDecimal superLargeNetInflow; // 超大单净流入(万元)
    
    @Column(name = "large_net_inflow", precision = 20, scale = 2)
    private BigDecimal largeNetInflow; // 大单净流入(万元)
    
    @Column(name = "medium_net_inflow", precision = 20, scale = 2)
    private BigDecimal mediumNetInflow; // 中单净流入(万元)
    
    @Column(name = "small_net_inflow", precision = 20, scale = 2)
    private BigDecimal smallNetInflow; // 小单净流入(万元)
    
    @Column(name = "super_large_inflow", precision = 20, scale = 2)
    private BigDecimal superLargeInflow; // 超大单流入(万元)
    
    @Column(name = "super_large_outflow", precision = 20, scale = 2)
    private BigDecimal superLargeOutflow; // 超大单流出(万元)
    
    @Column(name = "large_inflow", precision = 20, scale = 2)
    private BigDecimal largeInflow; // 大单流入(万元)
    
    @Column(name = "large_outflow", precision = 20, scale = 2)
    private BigDecimal largeOutflow; // 大单流出(万元)
    
    @Column(name = "medium_inflow", precision = 20, scale = 2)
    private BigDecimal mediumInflow; // 中单流入(万元)
    
    @Column(name = "medium_outflow", precision = 20, scale = 2)
    private BigDecimal mediumOutflow; // 中单流出(万元)
    
    @Column(name = "small_inflow", precision = 20, scale = 2)
    private BigDecimal smallInflow; // 小单流入(万元)
    
    @Column(name = "small_outflow", precision = 20, scale = 2)
    private BigDecimal smallOutflow; // 小单流出(万元)
    
    @Column(name = "institutional_net_inflow", precision = 20, scale = 2)
    private BigDecimal institutionalNetInflow; // 机构净流入(万元)
    
    @Column(name = "retail_net_inflow", precision = 20, scale = 2)
    private BigDecimal retailNetInflow; // 散户净流入(万元)
    
    @Column(name = "northbound_net_inflow", precision = 20, scale = 2)
    private BigDecimal northboundNetInflow; // 北向资金净流入(万元)
    
    @Column(name = "southbound_net_inflow", precision = 20, scale = 2)
    private BigDecimal southboundNetInflow; // 南向资金净流入(万元)
    
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
    public StockCapitalFlow() {}
    
    public StockCapitalFlow(String stockCode, LocalDate tradeDate) {
        this.stockCode = stockCode;
        this.tradeDate = tradeDate;
    }
    
    // Getters and Setters
    public String getStockCode() { return stockCode; }
    public void setStockCode(String stockCode) { this.stockCode = stockCode; }
    
    public LocalDate getTradeDate() { return tradeDate; }
    public void setTradeDate(LocalDate tradeDate) { this.tradeDate = tradeDate; }
    
    public String getStockName() { return stockName; }
    public void setStockName(String stockName) { this.stockName = stockName; }
    
    public String getMarketType() { return marketType; }
    public void setMarketType(String marketType) { this.marketType = marketType; }
    
    public BigDecimal getClosePrice() { return closePrice; }
    public void setClosePrice(BigDecimal closePrice) { this.closePrice = closePrice; }
    
    public BigDecimal getPriceChange() { return priceChange; }
    public void setPriceChange(BigDecimal priceChange) { this.priceChange = priceChange; }
    
    public BigDecimal getPriceChangeRatio() { return priceChangeRatio; }
    public void setPriceChangeRatio(BigDecimal priceChangeRatio) { this.priceChangeRatio = priceChangeRatio; }
    
    public BigDecimal getTurnoverAmount() { return turnoverAmount; }
    public void setTurnoverAmount(BigDecimal turnoverAmount) { this.turnoverAmount = turnoverAmount; }
    
    public BigDecimal getTurnoverVolume() { return turnoverVolume; }
    public void setTurnoverVolume(BigDecimal turnoverVolume) { this.turnoverVolume = turnoverVolume; }
    
    public BigDecimal getMainNetInflow() { return mainNetInflow; }
    public void setMainNetInflow(BigDecimal mainNetInflow) { this.mainNetInflow = mainNetInflow; }
    
    public BigDecimal getMainNetInflowRatio() { return mainNetInflowRatio; }
    public void setMainNetInflowRatio(BigDecimal mainNetInflowRatio) { this.mainNetInflowRatio = mainNetInflowRatio; }
    
    public BigDecimal getSuperLargeNetInflow() { return superLargeNetInflow; }
    public void setSuperLargeNetInflow(BigDecimal superLargeNetInflow) { this.superLargeNetInflow = superLargeNetInflow; }
    
    public BigDecimal getLargeNetInflow() { return largeNetInflow; }
    public void setLargeNetInflow(BigDecimal largeNetInflow) { this.largeNetInflow = largeNetInflow; }
    
    public BigDecimal getMediumNetInflow() { return mediumNetInflow; }
    public void setMediumNetInflow(BigDecimal mediumNetInflow) { this.mediumNetInflow = mediumNetInflow; }
    
    public BigDecimal getSmallNetInflow() { return smallNetInflow; }
    public void setSmallNetInflow(BigDecimal smallNetInflow) { this.smallNetInflow = smallNetInflow; }
    
    public BigDecimal getSuperLargeInflow() { return superLargeInflow; }
    public void setSuperLargeInflow(BigDecimal superLargeInflow) { this.superLargeInflow = superLargeInflow; }
    
    public BigDecimal getSuperLargeOutflow() { return superLargeOutflow; }
    public void setSuperLargeOutflow(BigDecimal superLargeOutflow) { this.superLargeOutflow = superLargeOutflow; }
    
    public BigDecimal getLargeInflow() { return largeInflow; }
    public void setLargeInflow(BigDecimal largeInflow) { this.largeInflow = largeInflow; }
    
    public BigDecimal getLargeOutflow() { return largeOutflow; }
    public void setLargeOutflow(BigDecimal largeOutflow) { this.largeOutflow = largeOutflow; }
    
    public BigDecimal getMediumInflow() { return mediumInflow; }
    public void setMediumInflow(BigDecimal mediumInflow) { this.mediumInflow = mediumInflow; }
    
    public BigDecimal getMediumOutflow() { return mediumOutflow; }
    public void setMediumOutflow(BigDecimal mediumOutflow) { this.mediumOutflow = mediumOutflow; }
    
    public BigDecimal getSmallInflow() { return smallInflow; }
    public void setSmallInflow(BigDecimal smallInflow) { this.smallInflow = smallInflow; }
    
    public BigDecimal getSmallOutflow() { return smallOutflow; }
    public void setSmallOutflow(BigDecimal smallOutflow) { this.smallOutflow = smallOutflow; }
    
    public BigDecimal getInstitutionalNetInflow() { return institutionalNetInflow; }
    public void setInstitutionalNetInflow(BigDecimal institutionalNetInflow) { this.institutionalNetInflow = institutionalNetInflow; }
    
    public BigDecimal getRetailNetInflow() { return retailNetInflow; }
    public void setRetailNetInflow(BigDecimal retailNetInflow) { this.retailNetInflow = retailNetInflow; }
    
    public BigDecimal getNorthboundNetInflow() { return northboundNetInflow; }
    public void setNorthboundNetInflow(BigDecimal northboundNetInflow) { this.northboundNetInflow = northboundNetInflow; }
    
    public BigDecimal getSouthboundNetInflow() { return southboundNetInflow; }
    public void setSouthboundNetInflow(BigDecimal southboundNetInflow) { this.southboundNetInflow = southboundNetInflow; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}