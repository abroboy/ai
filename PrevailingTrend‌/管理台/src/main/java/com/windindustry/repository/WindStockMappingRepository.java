package com.windindustry.repository;

import com.windindustry.model.WindStockMapping;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface WindStockMappingRepository extends JpaRepository<WindStockMapping, Long> {
    
    Optional<WindStockMapping> findByStockCode(String stockCode);
    
    List<WindStockMapping> findByMarketType(String marketType);
    
    List<WindStockMapping> findByMappingStatus(String mappingStatus);
    
    List<WindStockMapping> findByIndustryCode(String industryCode);
    
    List<WindStockMapping> findByStockNameContaining(String stockName);
    
    Page<WindStockMapping> findByMarketType(String marketType, Pageable pageable);
    
    Page<WindStockMapping> findByMappingStatus(String mappingStatus, Pageable pageable);
    
    Page<WindStockMapping> findByIndustryCode(String industryCode, Pageable pageable);
    
    @Query("SELECT w FROM WindStockMapping w WHERE " +
           "(:stockCode IS NULL OR w.stockCode LIKE %:stockCode%) AND " +
           "(:stockName IS NULL OR w.stockName LIKE %:stockName%) AND " +
           "(:marketType IS NULL OR w.marketType = :marketType) AND " +
           "(:mappingStatus IS NULL OR w.mappingStatus = :mappingStatus) AND " +
           "(:industryCode IS NULL OR w.industryCode = :industryCode)")
    Page<WindStockMapping> findByFilters(@Param("stockCode") String stockCode,
                                       @Param("stockName") String stockName,
                                       @Param("marketType") String marketType,
                                       @Param("mappingStatus") String mappingStatus,
                                       @Param("industryCode") String industryCode,
                                       Pageable pageable);
    
    @Query("SELECT COUNT(w) FROM WindStockMapping w WHERE w.mappingStatus = :status")
    Long countByMappingStatus(@Param("status") String status);
    
    @Query("SELECT COUNT(w) FROM WindStockMapping w WHERE w.marketType = :marketType")
    Long countByMarketType(@Param("marketType") String marketType);
    
    @Query("SELECT w.mappingStatus, COUNT(w) FROM WindStockMapping w GROUP BY w.mappingStatus")
    List<Object[]> getMappingStatusStats();
    
    @Query("SELECT w.marketType, COUNT(w) FROM WindStockMapping w GROUP BY w.marketType")
    List<Object[]> getMarketTypeStats();
    
    @Query("SELECT w.industryName, COUNT(w) FROM WindStockMapping w WHERE w.industryName IS NOT NULL GROUP BY w.industryName ORDER BY COUNT(w) DESC")
    List<Object[]> getIndustryStats();
    
    // ========== 数据分析查询方法 ==========
    
    @Query("SELECT w.industryName, COUNT(w), SUM(w.dailyNetInflow), AVG(w.dailyNetInflow) " +
           "FROM WindStockMapping w WHERE w.industryName IS NOT NULL AND w.dailyNetInflow IS NOT NULL " +
           "GROUP BY w.industryName ORDER BY SUM(w.dailyNetInflow) DESC")
    List<Object[]> getIndustryFlowRanking(@Param("limit") int limit, @Param("order") String order);
    
    @Query("SELECT w FROM WindStockMapping w WHERE w.dailyNetInflow IS NOT NULL ORDER BY w.dailyNetInflow DESC")
    List<WindStockMapping> findTopByDailyNetInflowDesc(Pageable pageable);
    
    @Query("SELECT w FROM WindStockMapping w WHERE w.dailyNetInflow IS NOT NULL ORDER BY w.dailyNetInflow ASC")
    List<WindStockMapping> findTopByDailyNetInflowAsc(Pageable pageable);
    
    @Query("SELECT w FROM WindStockMapping w WHERE w.latest7dInflow IS NOT NULL ORDER BY w.latest7dInflow DESC")
    List<WindStockMapping> findTopByLatest7dInflowDesc(Pageable pageable);
    
    @Query("SELECT w FROM WindStockMapping w WHERE w.latest7dInflow IS NOT NULL ORDER BY w.latest7dInflow ASC")
    List<WindStockMapping> findTopByLatest7dInflowAsc(Pageable pageable);
}