@echo off
chcp 65001
echo ========================================
echo 万得行业分类仪表盘启动中...
echo ========================================

REM 设置Java环境
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%

REM 进入项目目录
cd /d "c:\work\AI\PrevailingTrend‌\第一层模块\万得行业分类"

echo 正在启动Spring Boot应用...
echo 服务端口: 5001
echo 数据库: MySQL (localhost:3306/pt)
echo ========================================

REM 使用内置的Spring Boot启动
java -Dserver.port=5001 ^
     -Dspring.datasource.url="jdbc:mysql://localhost:3306/pt?characterEncoding=utf8&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=Asia/Shanghai" ^
     -Dspring.datasource.driver-class-name="com.mysql.cj.jdbc.Driver" ^
     -Dspring.datasource.username="root" ^
     -Dspring.datasource.password="rr1234RR" ^
     -Dspring.jpa.database-platform="org.hibernate.dialect.MySQL8Dialect" ^
     -Dspring.jpa.hibernate.ddl-auto="update" ^
     -Dspring.thymeleaf.cache="false" ^
     -Dlogging.level.com.windindustry="DEBUG" ^
     -cp "spring-3.2.0/*" ^
     org.springframework.boot.loader.JarLauncher

pause