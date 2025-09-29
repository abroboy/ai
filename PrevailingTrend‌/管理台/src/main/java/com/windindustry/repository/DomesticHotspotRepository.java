package com.windindustry.repository;

import com.windindustry.model.DomesticHotspot;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface DomesticHotspotRepository extends JpaRepository<DomesticHotspot, Long> {
    
    List<DomesticHotspot> findByPublishTimeAfterOrderByHeatScoreDesc(LocalDateTime publishTime);
    
    List<DomesticHotspot> findByCategoryOrderByHeatScoreDesc(String category);
    
    List<DomesticHotspot> findTop50ByOrderByHeatScoreDesc();
}