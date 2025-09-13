package com.windindustry;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.server.ConfigurableWebServerFactory;
import org.springframework.boot.web.server.WebServerFactoryCustomizer;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class WindIndustryApplication {

    public static void main(String[] args) {
        SpringApplication.run(WindIndustryApplication.class, args);
        System.out.println("Starting Wind Industry Dashboard...");
        System.out.println("Access URL: http://localhost:5001");
    }

    @Bean
    public WebServerFactoryCustomizer<ConfigurableWebServerFactory> webServerFactoryCustomizer() {
        return factory -> factory.setPort(5001);
    }
}
