package com.windindustry.service;

import com.windindustry.model.DomesticHotspot;
import com.windindustry.repository.DomesticHotspotRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class DomesticHotspotService {
    
    @Autowired
    private DomesticHotspotRepository repository;
    
    public List<DomesticHotspot> getLatestHotspots() {
        return repository.findTop50ByOrderByHeatScoreDesc();
    }
    
    public List<DomesticHotspot> getHotspotsByCategory(String category) {
        return repository.findByCategoryOrderByHeatScoreDesc(category);
    }
    
    public List<DomesticHotspot> getRecentHotspots(int hours) {
        LocalDateTime threshold = LocalDateTime.now().minusHours(hours);
        return repository.findByPublishTimeAfterOrderByHeatScoreDesc(threshold);
    }
}