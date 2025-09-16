package com.windindustry.repository;

import com.windindustry.model.StockCapitalFlow;
import com.windindustry.model.StockCapitalFlowId;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * 股票资金流向数据访问层
 */
@Repository
public interface StockCapitalFlowRepository extends JpaRepository<StockCapitalFlow, StockCapitalFlowId> {
    
    // 按股票代码查询
    List<StockCapitalFlow> findByStockCodeOrderByTradeDateDesc(String stockCode);
    
    List<StockCapitalFlow> findByStockCodeAndTradeDateBetween(String stockCode, LocalDate startDate, LocalDate endDate);
    
    Page<StockCapitalFlow> findByStockCode(String stockCode, Pageable pageable);
    
    // 按交易日期查询
    List<StockCapitalFlow> findByTradeDate(LocalDate tradeDate);
    
    List<StockCapitalFlow> findByTradeDateBetween(LocalDate startDate, LocalDate endDate);
    
    Page<StockCapitalFlow> findByTradeDate(LocalDate tradeDate, Pageable pageable);
    
    // 按市场类型查询
    List<StockCapitalFlow> findByMarketType(String marketType);
    
    Page<StockCapitalFlow> findByMarketType(String marketType, Pageable pageable);
    
    // 复杂查询
    @Query("SELECT s FROM StockCapitalFlow s WHERE " +
           "(:stockCode IS NULL OR s.stockCode = :stockCode) AND " +
           "(:stockName IS NULL OR s.stockName LIKE %:stockName%) AND " +
           "(:marketType IS NULL OR s.marketType = :marketType) AND " +
           "(:startDate IS NULL OR s.tradeDate >= :startDate) AND " +
           "(:endDate IS NULL OR s.tradeDate <= :endDate)")
    Page<StockCapitalFlow> findByMultipleFilters(@Param("stockCode") String stockCode,
                                                  @Param("stockName") String stockName,
                                                  @Param("marketType") String marketType,
                                                  @Param("startDate") LocalDate startDate,
                                                  @Param("endDate") LocalDate endDate,
                                                  Pageable pageable);
    
    // 主力资金流入查询
    @Query("SELECT s FROM StockCapitalFlow s WHERE s.mainNetInflow > 0 AND s.tradeDate = :tradeDate ORDER BY s.mainNetInflow DESC")
    List<StockCapitalFlow> findTopMainInflowsByDate(@Param("tradeDate") LocalDate tradeDate, Pageable pageable);
    
    @Query("SELECT s FROM StockCapitalFlow s WHERE s.mainNetInflow < 0 AND s.tradeDate = :tradeDate ORDER BY s.mainNetInflow ASC")
    List<StockCapitalFlow> findTopMainOutflowsByDate(@Param("tradeDate") LocalDate tradeDate, Pageable pageable);
    
    @Query("SELECT s FROM StockCapitalFlow s WHERE s.stockCode = :stockCode AND s.mainNetInflow > 0 ORDER BY s.tradeDate DESC")
    List<StockCapitalFlow> findPositiveMainInflowsByStock(@Param("stockCode") String stockCode);
    
    // 超大单资金流入查询
    @Query("SELECT s FROM StockCapitalFlow s WHERE s.superLargeNetInflow > 0 AND s.tradeDate = :tradeDate ORDER BY s.superLargeNetInflow DESC")
    List<StockCapitalFlow> findTopSuperLargeInflowsByDate(@Param("tradeDate") LocalDate tradeDate, Pageable pageable);
    
    // 北向资金查询
    @Query("SELECT s FROM StockCapitalFlow s WHERE s.northboundNetInflow IS NOT NULL AND s.tradeDate = :tradeDate ORDER BY s.northboundNetInflow DESC")
    List<StockCapitalFlow> findNorthboundFlowsByDate(@Param("tradeDate") LocalDate tradeDate);
    
    @Query("SELECT s FROM StockCapitalFlow s WHERE s.stockCode = :stockCode AND s.northboundNetInflow IS NOT NULL ORDER BY s.tradeDate DESC")
    List<StockCapitalFlow> findNorthboundFlowsByStock(@Param("stockCode") String stockCode);
    
    // 统计查询
    @Query("SELECT AVG(s.mainNetInflow) FROM StockCapitalFlow s WHERE s.stockCode = :stockCode AND s.mainNetInflow IS NOT NULL")
    BigDecimal getAverageMainNetInflowByStock(@Param("stockCode") String stockCode);
    
    @Query("SELECT SUM(s.mainNetInflow) FROM StockCapitalFlow s WHERE s.stockCode = :stockCode AND s.tradeDateBetween(:startDate, :endDate)")
    BigDecimal getTotalMainNetInflowByStockAndPeriod(@Param("stockCode") String stockCode, 
                                                      @Param("startDate") LocalDate startDate, 
                                                      @Param("endDate") LocalDate endDate);
    
    @Query("SELECT SUM(s.mainNetInflow) FROM StockCapitalFlow s WHERE s.tradeDate = :tradeDate AND s.marketType = :marketType")
    BigDecimal getTotalMainNetInflowByDateAndMarket(@Param("tradeDate") LocalDate tradeDate, 
                                                     @Param("marketType") String marketType);
    
    // 市场统计
    @Query("SELECT s.marketType, COUNT(s), AVG(s.mainNetInflow), SUM(s.mainNetInflow) " +
           "FROM StockCapitalFlow s WHERE s.tradeDate = :tradeDate " +
           "GROUP BY s.marketType")
    List<Object[]> getMarketStatisticsByDate(@Param("tradeDate") LocalDate tradeDate);
    
    // 时间序列查询
    @Query("SELECT s.tradeDate, SUM(s.mainNetInflow), COUNT(s) " +
           "FROM StockCapitalFlow s WHERE s.stockCode = :stockCode " +
           "AND s.tradeDate BETWEEN :startDate AND :endDate " +
           "GROUP BY s.tradeDate ORDER BY s.tradeDate")
    List<Object[]> getTimeSeriesDataByStock(@Param("stockCode") String stockCode,
                                             @Param("startDate") LocalDate startDate,
                                             @Param("endDate") LocalDate endDate);
    
    // 资金流向排行榜
    @Query("SELECT s.stockCode, s.stockName, s.mainNetInflow, s.mainNetInflowRatio " +
           "FROM StockCapitalFlow s WHERE s.tradeDate = :tradeDate " +
           "ORDER BY s.mainNetInflow DESC")
    List<Object[]> getMainInflowRankingByDate(@Param("tradeDate") LocalDate tradeDate, Pageable pageable);
    
    @Query("SELECT s.stockCode, s.stockName, s.superLargeNetInflow " +
           "FROM StockCapitalFlow s WHERE s.tradeDate = :tradeDate " +
           "ORDER BY s.superLargeNetInflow DESC")
    List<Object[]> getSuperLargeInflowRankingByDate(@Param("tradeDate") LocalDate tradeDate, Pageable pageable);
    
    // 涨跌幅与资金流向关联查询
    @Query("SELECT s FROM StockCapitalFlow s WHERE s.priceChangeRatio >= :minChangeRatio " +
           "AND s.mainNetInflow > 0 AND s.tradeDate = :tradeDate " +
           "ORDER BY s.priceChangeRatio DESC")
    List<StockCapitalFlow> findRisingStocksWithInflow(@Param("tradeDate") LocalDate tradeDate,
                                                       @Param("minChangeRatio") BigDecimal minChangeRatio);
    
    // 最新资金流向数据
    @Query("SELECT s FROM StockCapitalFlow s WHERE s.stockCode = :stockCode ORDER BY s.tradeDate DESC LIMIT 1")
    StockCapitalFlow findLatestByStockCode(@Param("stockCode") String stockCode);
    
    @Query("SELECT s FROM StockCapitalFlow s WHERE s.tradeDate = (SELECT MAX(f.tradeDate) FROM StockCapitalFlow f)")
    List<StockCapitalFlow> findLatestDataForAllStocks();
}