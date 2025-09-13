package com.windindustry.model;

import java.io.Serializable;
import java.time.LocalDate;

/**
 * 股票资金流向复合主键类
 */
public class StockCapitalFlowId implements Serializable {
    
    private String stockCode;
    private LocalDate tradeDate;
    
    public StockCapitalFlowId() {}
    
    public StockCapitalFlowId(String stockCode, LocalDate tradeDate) {
        this.stockCode = stockCode;
        this.tradeDate = tradeDate;
    }
    
    public String getStockCode() { return stockCode; }
    public void setStockCode(String stockCode) { this.stockCode = stockCode; }
    
    public LocalDate getTradeDate() { return tradeDate; }
    public void setTradeDate(LocalDate tradeDate) { this.tradeDate = tradeDate; }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        StockCapitalFlowId that = (StockCapitalFlowId) o;
        return stockCode.equals(that.stockCode) && tradeDate.equals(that.tradeDate);
    }
    
    @Override
    public int hashCode() {
        return stockCode.hashCode() + tradeDate.hashCode();
    }
}