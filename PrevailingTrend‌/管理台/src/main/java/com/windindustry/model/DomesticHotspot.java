package com.windindustry.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * 国内热点数据实体类
 */
@Entity
@Table(name = "l1_domestic_hotspot")
public class DomesticHotspot {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "title", nullable = false, length = 200)
    private String title;
    
    @Column(name = "category", nullable = false, length = 50)
    private String category;
    
    @Column(name = "content", columnDefinition = "TEXT")
    private String content;
    
    @Column(name = "publish_time", nullable = false)
    private LocalDateTime publishTime;
    
    @Column(name = "source", length = 100)
    private String source;
    
    @Column(name = "heat_score", precision = 5, scale = 2)
    private Double heatScore;
    
    @Column(name = "sentiment", length = 10)
    private String sentiment; // 积极/中性/消极
    
    @Column(name = "keywords", length = 500)
    private String keywords; // 逗号分隔的关键词
    
    @Column(name = "url", length = 500)
    private String url;
    
    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at", nullable = false)
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
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    
    public LocalDateTime getPublishTime() { return publishTime; }
    public void setPublishTime(LocalDateTime publishTime) { this.publishTime = publishTime; }
    
    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }
    
    public Double getHeatScore() { return heatScore; }
    public void setHeatScore(Double heatScore) { this.heatScore = heatScore; }
    
    public String getSentiment() { return sentiment; }
    public void setSentiment(String sentiment) { this.sentiment = sentiment; }
    
    public String getKeywords() { return keywords; }
    public void setKeywords(String keywords) { this.keywords = keywords; }
    
    public String getUrl() { return url; }
    public void setUrl(String url) { this.url = url; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}