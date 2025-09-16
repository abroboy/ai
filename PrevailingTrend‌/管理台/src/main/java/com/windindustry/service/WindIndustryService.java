package com.windindustry.service;

import com.windindustry.model.WindIndustryClassification;
import com.windindustry.repository.WindIndustryClassificationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class WindIndustryService {
    
    @Autowired
    private WindIndustryClassificationRepository windIndustryRepository;
    
    public Map<String, Object> getIndustryStatistics() {
        Map<String, Object> stats = new HashMap<>();
        
        Long totalIndustries = windIndustryRepository.count();
        Long level1Count = windIndustryRepository.countByIndustryLevel(1);
        Long level2Count = windIndustryRepository.countByIndustryLevel(2);
        Long level3Count = windIndustryRepository.countByIndustryLevel(3);
        
        stats.put("total_industries", totalIndustries != null ? totalIndustries : 0);
        stats.put("level_1_count", level1Count != null ? level1Count : 0);
        stats.put("level_2_count", level2Count != null ? level2Count : 0);
        stats.put("level_3_count", level3Count != null ? level3Count : 0);
        
        return stats;
    }
    
    public List<WindIndustryClassification> getAllIndustries() {
        return windIndustryRepository.findByIsActiveTrue();
    }
    
    public List<WindIndustryClassification> getIndustriesByLevel(Integer level) {
        return windIndustryRepository.findByIndustryLevel(level);
    }
    
    public List<WindIndustryClassification> getLevel1Industries() {
        return windIndustryRepository.findLevel1Industries();
    }
    
    public List<WindIndustryClassification> getLevel2Industries() {
        return windIndustryRepository.findLevel2Industries();
    }
    
    public List<WindIndustryClassification> getLevel3Industries() {
        return windIndustryRepository.findLevel3Industries();
    }
    
    public List<WindIndustryClassification> getSubIndustries(String parentIndustryCode) {
        return windIndustryRepository.findByParentIndustryCode(parentIndustryCode);
    }
    
    public Optional<WindIndustryClassification> getIndustryByCode(String industryCode) {
        return windIndustryRepository.findById(industryCode);
    }
    
    public List<WindIndustryClassification> searchIndustries(String keyword) {
        return windIndustryRepository.findByIndustryNameContaining(keyword);
    }
}