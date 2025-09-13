package com.windindustry;

import com.windindustry.service.ListedCompanyInfoService;
import com.windindustry.service.HkConnectStockService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class WindIndustryApplication implements CommandLineRunner {
    
    @Autowired
    private ListedCompanyInfoService listedCompanyInfoService;
    
    @Autowired
    private HkConnectStockService hkConnectStockService;
    
    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("万得行业分类仪表盘启动中...");
        System.out.println("Java版本: " + System.getProperty("java.version"));
        System.out.println("工作目录: " + System.getProperty("user.dir"));
        System.out.println("========================================");
        
        try {
            // 设置系统属性
            System.setProperty("server.port", "5001");
            System.setProperty("spring.datasource.url", "jdbc:mysql://localhost:3306/pt?characterEncoding=utf8&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=Asia/Shanghai");
            System.setProperty("spring.datasource.driver-class-name", "com.mysql.cj.jdbc.Driver");
            System.setProperty("spring.datasource.username", "root");
            System.setProperty("spring.datasource.password", "rr1234RR");
            System.setProperty("spring.jpa.database-platform", "org.hibernate.dialect.MySQL8Dialect");
            System.setProperty("spring.jpa.hibernate.ddl-auto", "update");
            System.setProperty("spring.thymeleaf.cache", "false");
            System.setProperty("logging.level.com.windindustry", "DEBUG");
            
            SpringApplication.run(WindIndustryApplication.class, args);
            
            System.out.println("========================================");
            System.out.println("应用启动成功！");
            System.out.println("访问地址: http://localhost:5001");
            System.out.println("========================================");
        } catch (Exception e) {
            System.err.println("应用启动失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    @Override
    public void run(String... args) throws Exception {
        System.out.println("开始初始化应用数据...");
        
        try {
            // 初始化上市公司数据
            listedCompanyInfoService.initializeCompanyData();
            
            // 初始化港股通数据
            hkConnectStockService.initializeHkConnectData();
            
            System.out.println("应用数据初始化完成！");
        } catch (Exception e) {
            System.err.println("数据初始化失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
