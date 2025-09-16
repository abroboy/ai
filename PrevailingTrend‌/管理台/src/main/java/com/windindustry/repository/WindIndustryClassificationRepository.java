package com.windindustry.repository;

import com.windindustry.model.WindIndustryClassification;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface WindIndustryClassificationRepository extends JpaRepository<WindIndustryClassification, String> {
    
    List<WindIndustryClassification> findByIndustryLevel(Integer industryLevel);
    
    List<WindIndustryClassification> findByParentIndustryCode(String parentIndustryCode);
    
    List<WindIndustryClassification> findByIndustryNameContaining(String industryName);
    
    List<WindIndustryClassification> findByIsActiveTrue();
    
    @Query("SELECT COUNT(w) FROM WindIndustryClassification w WHERE w.industryLevel = :level AND w.isActive = true")
    Long countByIndustryLevel(@Param("level") Integer level);
    
    @Query("SELECT w FROM WindIndustryClassification w WHERE w.industryLevel = 1 AND w.isActive = true ORDER BY w.industryCode")
    List<WindIndustryClassification> findLevel1Industries();
    
    @Query("SELECT w FROM WindIndustryClassification w WHERE w.industryLevel = 2 AND w.isActive = true ORDER BY w.industryCode")
    List<WindIndustryClassification> findLevel2Industries();
    
    @Query("SELECT w FROM WindIndustryClassification w WHERE w.industryLevel = 3 AND w.isActive = true ORDER BY w.industryCode")
    List<WindIndustryClassification> findLevel3Industries();
}