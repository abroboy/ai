package com.windindustry.controller;

import com.windindustry.model.DomesticHotspot;
import com.windindustry.service.DomesticHotspotService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/domestic-hotspot")
public class DomesticHotspotController {
    
    @Autowired
    private DomesticHotspotService service;
    
    @GetMapping
    public Map<String, Object> getHotspots() {
        Map<String, Object> response = new HashMap<>();
        try {
            List<DomesticHotspot> data = service.getLatestHotspots();
            response.put("success", true);
            response.put("data", data);
        } catch (Exception e) {
            response.put("success", false);
            response.put("message", e.getMessage());
        }
        return response;
    }
    
    @GetMapping("/by-category")
    public Map<String, Object> getHotspotsByCategory(@RequestParam String category) {
        Map<String, Object> response = new HashMap<>();
        try {
            List<DomesticHotspot> data = service.getHotspotsByCategory(category);
            response.put("success", true);
            response.put("data", data);
        } catch (Exception e) {
            response.put("success", false);
            response.put("message", e.getMessage());
        }
        return response;
    }
}