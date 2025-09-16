package com.admin;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@SpringBootApplication
@Controller
public class AdminApplication {
    
    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("大势所趋风险框架 - 管理台启动中...");
        System.out.println("Java版本: " + System.getProperty("java.version"));
        System.out.println("工作目录: " + System.getProperty("user.dir"));
        System.out.println("========================================");
        
        try {
            // 设置系统属性
            System.setProperty("server.port", "8090");
            System.setProperty("spring.thymeleaf.cache", "false");
            System.setProperty("logging.level.com.admin", "DEBUG");
            
            SpringApplication.run(AdminApplication.class, args);
            
            System.out.println("========================================");
            System.out.println("管理台启动成功！");
            System.out.println("访问地址: http://localhost:8090");
            System.out.println("========================================");
        } catch (Exception e) {
            System.err.println("管理台启动失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    @RequestMapping("/")
    public String index() {
        return "index";
    }
}
