package com.admin;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@SpringBootApplication
@Controller
public class AdminApplication {
    
    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("Admin Console Starting...");
        System.out.println("Java Version: " + System.getProperty("java.version"));
        System.out.println("Working Directory: " + System.getProperty("user.dir"));
        System.out.println("========================================");
        
        try {
            System.setProperty("server.port", "8090");
            System.setProperty("spring.thymeleaf.cache", "false");
            System.setProperty("logging.level.com.admin", "DEBUG");
            
            SpringApplication.run(AdminApplication.class, args);
            
            System.out.println("========================================");
            System.out.println("Admin Console Started Successfully!");
            System.out.println("Access URL: http://localhost:8090");
            System.out.println("========================================");
        } catch (Exception e) {
            System.err.println("Admin Console Startup Failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    @RequestMapping("/")
    public String index() {
        return "index";
    }
}
