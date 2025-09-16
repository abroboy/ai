package com.windindustry.repository;

import com.windindustry.model.StockIndustryMapping;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface StockIndustryRepository extends JpaRepository<StockIndustryMapping, String> {
    
    List<StockIndustryMapping> findByIndustryCode(String industryCode);
    
    List<StockIndustryMapping> findByIndustryNameContaining(String industryName);
    
    @Query("SELECT COUNT(DISTINCT s.industryCode) FROM StockIndustryMapping s")
    Long countDistinctIndustries();
    
    @Query("SELECT COUNT(DISTINCT s.industryCode) FROM StockIndustryMapping s WHERE s.industryCode LIKE 
801%")
    Long countLevel1Industries();
    
    @Query("SELECT COUNT(DISTINCT s.industryCode) FROM StockIndustryMapping s WHERE s.industryCode LIKE 8010%")
    Long countLevel2Industries();
    
    @Query("SELECT s.industryCode, s.industryName, COUNT(s) as stockCount, " +
           "CASE WHEN s.industryCode LIKE 801% THEN 1 ELSE 2 END as level " +
           "FROM StockIndustryMapping s " +
           "GROUP BY s.industryCode, s.industryName " +
           "ORDER BY stockCount DESC")
    List<Object[]> getIndustryStatistics();
}
