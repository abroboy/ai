package com.windindustry.config;

import com.windindustry.model.DomesticHotspot;
import com.windindustry.repository.DomesticHotspotRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.LocalDateTime;
import java.util.Arrays;

@Configuration
public class DataInitializer {
    
    @Bean
    public CommandLineRunner initData(DomesticHotspotRepository repository) {
        return args -> {
            // 如果数据库中没有数据，则初始化测试数据
            if (repository.count() == 0) {
                // 初始化国内热点数据
                DomesticHotspot[] hotspots = {
                    createHotspot("央行货币政策调整分析", "财经热点", "央行货币政策调整分析内容...", "新华财经", 85.5, "积极"),
                    createHotspot("金融监管新政策", "政策动态", "金融监管新政策内容...", "人民日报", 92.3, "积极"),
                    createHotspot("股市收盘分析", "市场新闻", "股市收盘分析内容...", "财新网", 78.9, "中性"),
                    createHotspot("科技行业发展", "行业资讯", "科技行业发展内容...", "中国产经新闻", 88.7, "积极"),
                    createHotspot("上市公司业绩", "公司热点", "上市公司业绩内容...", "公司公告", 75.2, "积极"),
                    createHotspot("GDP增长数据", "宏观经济", "GDP增长数据内容...", "国家统计局", 90.1, "积极"),
                    createHotspot("投资策略分析", "投资热点", "投资策略分析内容...", "投资机构", 82.6, "中性")
                };
                
                repository.saveAll(Arrays.asList(hotspots));
            }
        };
    }
    
    private DomesticHotspot createHotspot(String title, String category, String content, 
                                         String source, double heatScore, String sentiment) {
        DomesticHotspot hotspot = new DomesticHotspot();
        hotspot.setTitle(title);
        hotspot.setCategory(category);
        hotspot.setContent(content);
        hotspot.setSource(source);
        hotspot.setHeatScore(heatScore);
        hotspot.setSentiment(sentiment);
        hotspot.setPublishTime(LocalDateTime.now().minusDays(1));
        return hotspot;
    }
}