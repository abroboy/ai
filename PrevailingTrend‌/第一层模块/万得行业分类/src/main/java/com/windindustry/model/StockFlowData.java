package com.windindustry.model;

import jakarta.persistence.*;
import java.io.Serializable;
import java.time.LocalDate;

@Entity
@Table(name = "stock_flow_data")
@IdClass(StockFlowDataId.class)
public class StockFlowData {
    
    @Id
    @Column(name = "stock_code")
    private String stockCode;
    
    @Id
    @Column(name = "trade_date")
    private LocalDate tradeDate;
    
    @Column(name = "total_net")
    private Double totalNet;
    
    // Constructors
    public StockFlowData() {}
    
    public StockFlowData(String stockCode, LocalDate tradeDate, Double totalNet) {
        this.stockCode = stockCode;
        this.tradeDate = tradeDate;
        this.totalNet = totalNet;
    }
    
    // Getters and Setters
    public String getStockCode() { return stockCode; }
    public void setStockCode(String stockCode) { this.stockCode = stockCode; }
    
    public LocalDate getTradeDate() { return tradeDate; }
    public void setTradeDate(LocalDate tradeDate) { this.tradeDate = tradeDate; }
    
    public Double getTotalNet() { return totalNet; }
    public void setTotalNet(Double totalNet) { this.totalNet = totalNet; }
}

// Composite Key Class
class StockFlowDataId implements Serializable {
    private String stockCode;
    private LocalDate tradeDate;
    
    public StockFlowDataId() {}
    
    public StockFlowDataId(String stockCode, LocalDate tradeDate) {
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
        StockFlowDataId that = (StockFlowDataId) o;
        return stockCode.equals(that.stockCode) && tradeDate.equals(that.tradeDate);
    }
    
    @Override
    public int hashCode() {
        return stockCode.hashCode() + tradeDate.hashCode();
    }
}
