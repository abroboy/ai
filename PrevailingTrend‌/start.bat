@echo off
echo ========================================
echo 大势所趋风险框架 - 编译和启动脚本
echo PrevailingTrend Risk Framework
echo ========================================

echo 1. 下载依赖库...
if not exist "gson-2.10.1.jar" (
    echo 下载 Gson 库...
    powershell -Command "Invoke-WebRequest -Uri 'https://repo1.maven.org/maven2/com/google/code/gson/gson/2.10.1/gson-2.10.1.jar' -OutFile 'gson-2.10.1.jar'"
)

if not exist "mysql-connector-java-8.0.33.jar" (
    echo 下载 MySQL 连接器...
    powershell -Command "Invoke-WebRequest -Uri 'https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.33/mysql-connector-java-8.0.33.jar' -OutFile 'mysql-connector-java-8.0.33.jar'"
)

echo 2. 编译Java文件...
javac -encoding UTF-8 -cp ".;gson-2.10.1.jar;mysql-connector-java-8.0.33.jar" *.java

if %ERRORLEVEL% NEQ 0 (
    echo ❌ 编译失败！
    pause
    exit /b 1
)

echo ✅ 编译成功！

echo 3. 启动服务器...
echo 访问地址: http://localhost:80
echo ========================================

java -cp ".;gson-2.10.1.jar;mysql-connector-java-8.0.33.jar" com.prevailingtrend.PrevailingTrendMainServer

pause