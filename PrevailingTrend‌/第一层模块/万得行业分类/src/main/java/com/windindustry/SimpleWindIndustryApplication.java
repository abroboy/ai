package com.windindustry;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * 万得行业分类应用启动类
 * 简化版本，专注于核心功能
 */
@SpringBootApplication
public class SimpleWindIndustryApplication {
    
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
            
            SpringApplication.run(SimpleWindIndustryApplication.class, args);
            
            System.out.println("========================================");
            System.out.println("应用启动成功！");
            System.out.println("访问地址: http://localhost:5001");
            System.out.println("股票映射管理: http://localhost:5001/stock-mappings");
            System.out.println("========================================");
        } catch (Exception e) {
            System.err.println("应用启动失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
}