package com.windindustry.controller;

import com.windindustry.service.StockService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class DashboardController {

    @Autowired
    private StockService stockService;

    @GetMapping("/")
    public String dashboard(Model model) {
        // 添加模型数据
        return "dashboard";
    }
} 