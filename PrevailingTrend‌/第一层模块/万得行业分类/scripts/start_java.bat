@echo off
echo 启动万得行业分类仪表盘...
echo.

REM 设置Java环境
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%

REM 创建lib目录并下载必要的JAR文件
if not exist lib mkdir lib

echo 下载Spring Boot依赖...
powershell -Command "Invoke-WebRequest -Uri 
https://repo1.maven.org/maven2/org/springframework/boot/spring-boot-starter-web/3.2.0/spring-boot-starter-web-3.2.0.jar -OutFile lib/spring-boot-starter-web.jar"
powershell -Command "Invoke-WebRequest -Uri https://repo1.maven.org/maven2/org/springframework/boot/spring-boot-starter-data-jpa/3.2.0/spring-boot-starter-data-jpa-3.2.0.jar -OutFile lib/spring-boot-starter-data-jpa.jar"
powershell -Command "Invoke-WebRequest -Uri https://repo1.maven.org/maven2/org/springframework/boot/spring-boot-starter-thymeleaf/3.2.0/spring-boot-starter-thymeleaf-3.2.0.jar -OutFile lib/spring-boot-starter-thymeleaf.jar"
powershell -Command "Invoke-WebRequest -Uri https://repo1.maven.org/maven2/org/sqlite/sqlite-jdbc/3.44.1.0/sqlite-jdbc-3.44.1.0.jar -OutFile lib/sqlite-jdbc.jar"

echo.
echo 编译Java源代码...
javac -cp "lib/*" -d target/classes src/main/java/com/windindustry/*.java src/main/java/com/windindustry/*/*.java

echo.
echo 启动应用...
java -cp "target/classes;lib/*" com.windindustry.WindIndustryApplication

pause
