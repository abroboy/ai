package com.windindustry.repository;

import com.windindustry.model.HkConnectStock;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

/**
 * 港股通数据访问层
 */
@Repository
public interface HkConnectStockRepository extends JpaRepository<HkConnectStock, String> {
    
    // 基础查询
    Optional<HkConnectStock> findByStockCode(String stockCode);
    
    List<HkConnectStock> findByStockNameCnContaining(String stockNameCn);
    
    List<HkConnectStock> findByConnectType(String connectType);
    
    List<HkConnectStock> findByBoardType(String boardType);
    
    List<HkConnectStock> findByIndustryCode(String industryCode);
    
    List<HkConnectStock> findByIsActiveTrue();
    
    List<HkConnectStock> findByIsSuspendedFalse();
    
    // 分页查询
    Page<HkConnectStock> findByConnectType(String connectType, Pageable pageable);
    
    Page<HkConnectStock> findByIndustryCode(String industryCode, Pageable pageable);
    
    Page<HkConnectStock> findByIsActiveTrue(Pageable pageable);
    
    // 复杂查询
    @Query("SELECT h FROM HkConnectStock h WHERE " +
           "(:stockCode IS NULL OR h.stockCode = :stockCode) AND " +
           "(:stockNameCn IS NULL OR h.stockNameCn LIKE %:stockNameCn%) AND " +
           "(:connectType IS NULL OR h.connectType = :connectType) AND " +
           "(:industryCode IS NULL OR h.industryCode = :industryCode) AND " +
           "(:isActive IS NULL OR h.isActive = :isActive)")
    Page<HkConnectStock> findByMultipleFilters(@Param("stockCode") String stockCode,
                                                @Param("stockNameCn") String stockNameCn,
                                                @Param("connectType") String connectType,
                                                @Param("industryCode") String industryCode,
                                                @Param("isActive") Boolean isActive,
                                                Pageable pageable);
    
    // 统计查询
    @Query("SELECT COUNT(h) FROM HkConnectStock h WHERE h.connectType = :connectType AND h.isActive = true")
    Long countByConnectTypeAndIsActiveTrue(@Param("connectType") String connectType);
    
    @Query("SELECT h.connectType, COUNT(h) FROM HkConnectStock h WHERE h.isActive = true GROUP BY h.connectType")
    List<Object[]> getConnectTypeStatistics();
    
    @Query("SELECT h.industryCode, h.industryName, COUNT(h) FROM HkConnectStock h WHERE h.isActive = true GROUP BY h.industryCode, h.industryName ORDER BY COUNT(h) DESC")
    List<Object[]> getIndustryStatistics();
    
    @Query("SELECT h.boardType, COUNT(h) FROM HkConnectStock h WHERE h.isActive = true GROUP BY h.boardType")
    List<Object[]> getBoardTypeStatistics();
    
    // 市值相关查询
    @Query("SELECT AVG(h.marketValueRmb) FROM HkConnectStock h WHERE h.connectType = :connectType AND h.marketValueRmb IS NOT NULL")
    BigDecimal getAverageMarketValueByConnectType(@Param("connectType") String connectType);
    
    @Query("SELECT h FROM HkConnectStock h WHERE h.marketValueRmb >= :minValue AND h.marketValueRmb <= :maxValue AND h.isActive = true ORDER BY h.marketValueRmb DESC")
    List<HkConnectStock> findByMarketValueRange(@Param("minValue") BigDecimal minValue, @Param("maxValue") BigDecimal maxValue);
    
    @Query("SELECT h FROM HkConnectStock h WHERE h.isActive = true ORDER BY h.marketValueRmb DESC")
    List<HkConnectStock> findTopByMarketValue(Pageable pageable);
    
    // 北向资金相关查询
    @Query("SELECT h FROM HkConnectStock h WHERE h.northboundNetInflow > 0 AND h.isActive = true ORDER BY h.northboundNetInflow DESC")
    List<HkConnectStock> findTopNorthboundInflows(Pageable pageable);
    
    @Query("SELECT h FROM HkConnectStock h WHERE h.northboundHoldingRatio >= :minRatio AND h.northboundHoldingRatio IS NOT NULL ORDER BY h.northboundHoldingRatio DESC")
    List<HkConnectStock> findByNorthboundHoldingRatio(@Param("minRatio") BigDecimal minRatio);
    
    @Query("SELECT SUM(h.northboundNetInflow) FROM HkConnectStock h WHERE h.connectType = :connectType AND h.northboundNetInflow IS NOT NULL")
    BigDecimal getTotalNorthboundInflowByConnectType(@Param("connectType") String connectType);
    
    // 成交额查询
    @Query("SELECT h FROM HkConnectStock h WHERE h.dailyTurnoverRmb >= :minTurnover AND h.isActive = true ORDER BY h.dailyTurnoverRmb DESC")
    List<HkConnectStock> findByDailyTurnoverGreaterThan(@Param("minTurnover") BigDecimal minTurnover);
    
    @Query("SELECT AVG(h.dailyTurnoverRmb) FROM HkConnectStock h WHERE h.connectType = :connectType AND h.dailyTurnoverRmb IS NOT NULL")
    BigDecimal getAverageDailyTurnoverByConnectType(@Param("connectType") String connectType);
    
    // 财务指标查询
    @Query("SELECT h FROM HkConnectStock h WHERE h.peRatio >= :minPe AND h.peRatio <= :maxPe AND h.peRatio IS NOT NULL ORDER BY h.peRatio")
    List<HkConnectStock> findByPeRatioRange(@Param("minPe") BigDecimal minPe, @Param("maxPe") BigDecimal maxPe);
    
    @Query("SELECT h FROM HkConnectStock h WHERE h.dividendYield >= :minYield AND h.dividendYield IS NOT NULL ORDER BY h.dividendYield DESC")
    List<HkConnectStock> findByDividendYieldGreaterThan(@Param("minYield") BigDecimal minYield);
}