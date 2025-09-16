package com.windindustry.repository;

import com.windindustry.model.StockFlowData;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.List;

@Repository
public interface StockFlowRepository extends JpaRepository<StockFlowData, String> {
    
    List<StockFlowData> findByStockCodeOrderByTradeDateDesc(String stockCode);
    
    List<StockFlowData> findByStockCodeAndTradeDateBetween(String stockCode, LocalDate startDate, LocalDate endDate);
    
    @Query("SELECT AVG(s.totalNet) FROM StockFlowData s WHERE s.stockCode = :stockCode")
    Double getAverageNetFlowByStockCode(@Param("stockCode") String stockCode);
    
    @Query("SELECT s FROM StockFlowData s WHERE s.stockCode = :stockCode ORDER BY s.tradeDate DESC")
    List<StockFlowData> findRecentFlowDataByStockCode(@Param("stockCode") String stockCode);
}
