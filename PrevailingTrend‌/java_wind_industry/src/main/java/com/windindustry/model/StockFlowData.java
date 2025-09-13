package com.windindustry.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

import java.util.Date;

@Entity
@Table(name = "stock_flow_data")
@Data
public class StockFlowData {
    @Id
    private String stockCode;
    private Date tradeDate;
    private double totalNet;
} 