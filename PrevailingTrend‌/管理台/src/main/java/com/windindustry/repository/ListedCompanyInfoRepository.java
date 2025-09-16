package com.windindustry.repository;

import com.windindustry.model.ListedCompanyInfo;
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
 * 上市公司信息数据访问层
 */
@Repository
public interface ListedCompanyInfoRepository extends JpaRepository<ListedCompanyInfo, String> {
    
    // 基础查询
    Optional<ListedCompanyInfo> findByStockCode(String stockCode);
    
    List<ListedCompanyInfo> findByCompanyNameContaining(String companyName);
    
    List<ListedCompanyInfo> findByStockNameContaining(String stockName);
    
    List<ListedCompanyInfo> findByMarketType(String marketType);
    
    List<ListedCompanyInfo> findByIndustryCode(String industryCode);
    
    List<ListedCompanyInfo> findByIsActiveTrue();
    
    List<ListedCompanyInfo> findByIsSuspendedFalse();
    
    // 分页查询
    Page<ListedCompanyInfo> findByMarketType(String marketType, Pageable pageable);
    
    Page<ListedCompanyInfo> findByIndustryCode(String industryCode, Pageable pageable);
    
    Page<ListedCompanyInfo> findByIsActiveTrue(Pageable pageable);
    
    // 复杂查询
    @Query("SELECT c FROM ListedCompanyInfo c WHERE " +
           "(:stockCode IS NULL OR c.stockCode = :stockCode) AND " +
           "(:stockName IS NULL OR c.stockName LIKE %:stockName%) AND " +
           "(:companyName IS NULL OR c.companyName LIKE %:companyName%) AND " +
           "(:marketType IS NULL OR c.marketType = :marketType) AND " +
           "(:industryCode IS NULL OR c.industryCode = :industryCode) AND " +
           "(:isActive IS NULL OR c.isActive = :isActive)")
    Page<ListedCompanyInfo> findByMultipleFilters(@Param("stockCode") String stockCode,
                                                   @Param("stockName") String stockName,
                                                   @Param("companyName") String companyName,
                                                   @Param("marketType") String marketType,
                                                   @Param("industryCode") String industryCode,
                                                   @Param("isActive") Boolean isActive,
                                                   Pageable pageable);
    
    // 统计查询
    @Query("SELECT COUNT(c) FROM ListedCompanyInfo c WHERE c.marketType = :marketType AND c.isActive = true")
    Long countByMarketTypeAndIsActiveTrue(@Param("marketType") String marketType);
    
    @Query("SELECT COUNT(c) FROM ListedCompanyInfo c WHERE c.industryCode = :industryCode AND c.isActive = true")
    Long countByIndustryCodeAndIsActiveTrue(@Param("industryCode") String industryCode);
    
    @Query("SELECT c.marketType, COUNT(c) FROM ListedCompanyInfo c WHERE c.isActive = true GROUP BY c.marketType")
    List<Object[]> getMarketTypeStatistics();
    
    @Query("SELECT c.industryCode, c.industryName, COUNT(c) FROM ListedCompanyInfo c WHERE c.isActive = true GROUP BY c.industryCode, c.industryName ORDER BY COUNT(c) DESC")
    List<Object[]> getIndustryStatistics();
    
    // 市值相关查询
    @Query("SELECT AVG(c.totalMarketValue) FROM ListedCompanyInfo c WHERE c.marketType = :marketType AND c.totalMarketValue IS NOT NULL")
    BigDecimal getAverageMarketValueByMarketType(@Param("marketType") String marketType);
    
    @Query("SELECT c FROM ListedCompanyInfo c WHERE c.totalMarketValue >= :minValue AND c.totalMarketValue <= :maxValue AND c.isActive = true ORDER BY c.totalMarketValue DESC")
    List<ListedCompanyInfo> findByMarketValueRange(@Param("minValue") BigDecimal minValue, @Param("maxValue") BigDecimal maxValue);
    
    @Query("SELECT c FROM ListedCompanyInfo c WHERE c.isActive = true ORDER BY c.totalMarketValue DESC")
    List<ListedCompanyInfo> findTopByMarketValue(Pageable pageable);
    
    // ST股票查询
    @Query("SELECT c FROM ListedCompanyInfo c WHERE c.isSt = true AND c.isActive = true")
    List<ListedCompanyInfo> findStStocks();
    
    // 停牌股票查询
    @Query("SELECT c FROM ListedCompanyInfo c WHERE c.isSuspended = true")
    List<ListedCompanyInfo> findSuspendedStocks();
    
    // 财务指标查询
    @Query("SELECT c FROM ListedCompanyInfo c WHERE c.peRatio >= :minPe AND c.peRatio <= :maxPe AND c.peRatio IS NOT NULL ORDER BY c.peRatio")
    List<ListedCompanyInfo> findByPeRatioRange(@Param("minPe") BigDecimal minPe, @Param("maxPe") BigDecimal maxPe);
    
    @Query("SELECT c FROM ListedCompanyInfo c WHERE c.roe >= :minRoe AND c.roe IS NOT NULL ORDER BY c.roe DESC")
    List<ListedCompanyInfo> findByRoeGreaterThan(@Param("minRoe") BigDecimal minRoe);
}