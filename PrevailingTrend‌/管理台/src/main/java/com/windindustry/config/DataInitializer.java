package com.windindustry.config;

import com.windindustry.service.DataCollectionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {
    
    @Autowired
    private DataCollectionService dataCollectionService;
    
    @Override
    public void run(String... args) throws Exception {
        System.out.println("应用启动完成，开始初始化数据...");
        dataCollectionService.initializeData();
        System.out.println("数据初始化完成");
    }
}
