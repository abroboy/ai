package com.windindustry.repository;

import com.windindustry.model.StockIndustryMapping;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

public interface StockIndustryRepository extends JpaRepository<StockIndustryMapping, String> {

    @Query(value = "SELECT s.stock_code, s.stock_name, s.industry_code, s.industry_name, s.mapping_status, s.confidence, s.created_at, s.updated_at, " +
            "COALESCE(f.total_net_flow, 0) as total_net_flow, COALESCE(f.avg_net_flow, 0) as avg_net_flow, COALESCE(f.flow_ratio, 0) as flow_ratio, " +
            "COALESCE(0, 0) as prediction_score, COALESCE(f.recent_flow, 0) as recent_flow, COALESCE(f.flow_days, 0) as flow_days " +
            "FROM stock_industry_mapping s " +
            "LEFT JOIN (SELECT CASE WHEN stock_code LIKE '%.SZ' THEN SUBSTRING(stock_code, 1, LOCATE('.', stock_code) - 1) ELSE stock_code END as clean_stock_code, " +
            "SUM(total_net) as total_net_flow, AVG(total_net) as avg_net_flow, (AVG(total_net) / 10000) as flow_ratio, " +
            "SUM(CASE WHEN trade_date >= CURDATE() - INTERVAL 7 DAY THEN total_net ELSE 0 END) as recent_flow, COUNT(*) as flow_days " +
            "FROM stock_flow_data GROUP BY clean_stock_code) f ON s.stock_code = f.clean_stock_code " +
            "ORDER BY :sortBy :sortOrder LIMIT :pageSize OFFSET :offset", nativeQuery = true)
    List<Object[]> getStocksWithFlow(@Param("sortBy") String sortBy, @Param("sortOrder") String sortOrder, @Param("pageSize") int pageSize, @Param("offset") int offset);
} 