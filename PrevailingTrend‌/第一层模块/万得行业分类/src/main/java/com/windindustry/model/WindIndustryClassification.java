package com.windindustry.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "l1_wind_industry_classification")
public class WindIndustryClassification {
    
    @Id
    @Column(name = "industry_code")
    private String industryCode;
    
    @Column(name = "industry_name", nullable = false)
    private String industryName;
    
    @Column(name = "industry_level")
    private Integer industryLevel;
    
    @Column(name = "parent_industry_code")
    private String parentIndustryCode;
    
    @Column(name = "industry_description")
    private String industryDescription;
    
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
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
    
    // Constructors
    public WindIndustryClassification() {}
    
    public WindIndustryClassification(String industryCode, String industryName, Integer industryLevel) {
        this.industryCode = industryCode;
        this.industryName = industryName;
        this.industryLevel = industryLevel;
    }
    
    // Getters and Setters
    public String getIndustryCode() { return industryCode; }
    public void setIndustryCode(String industryCode) { this.industryCode = industryCode; }
    
    public String getIndustryName() { return industryName; }
    public void setIndustryName(String industryName) { this.industryName = industryName; }
    
    public Integer getIndustryLevel() { return industryLevel; }
    public void setIndustryLevel(Integer industryLevel) { this.industryLevel = industryLevel; }
    
    public String getParentIndustryCode() { return parentIndustryCode; }
    public void setParentIndustryCode(String parentIndustryCode) { this.parentIndustryCode = parentIndustryCode; }
    
    public String getIndustryDescription() { return industryDescription; }
    public void setIndustryDescription(String industryDescription) { this.industryDescription = industryDescription; }
    
    public Boolean getIsActive() { return isActive; }
    public void setIsActive(Boolean isActive) { this.isActive = isActive; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}