package com.windindustry.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

import java.util.Date;

@Entity
@Table(name = "stock_industry_mapping")
@Data
public class StockIndustryMapping {
    @Id
    private String stockCode;
    private String stockName;
    private String industryCode;
    private String industryName;
    private String mappingStatus;
    private double confidence;
    private Date createdAt;
    private Date updatedAt;
} 