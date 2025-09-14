@echo off
echo ========================================
echo 大势所趋风险框架 - Java版本编译和启动脚本
echo PrevailingTrend Risk Framework - Java Version
echo ========================================

echo 1. 检查Java环境...
java -version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Java环境未找到！请安装Java 17或更高版本
    pause
    exit /b 1
)

echo.
echo 2. 下载MySQL驱动...
if not exist "mysql-connector-java-8.0.33.jar" (
    echo 下载 MySQL 连接器...
    powershell -Command "Invoke-WebRequest -Uri 'https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.33/mysql-connector-java-8.0.33.jar' -OutFile 'mysql-connector-java-8.0.33.jar'"
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ MySQL驱动下载失败！
        pause
        exit /b 1
    )
) else (
    echo ✅ MySQL驱动已存在
)

echo.
echo 3. 编译Java文件...
javac -encoding UTF-8 -cp ".;mysql-connector-java-8.0.33.jar" ^
    PrevailingTrendMainServer.java ^
    数据库配置\DatabaseConfig.java ^
    数据库配置\DatabaseInitializer.java ^
    数据库配置\DatabaseTester.java ^
    第一层模块\万得行业分类\StockDataGenerator.java

if %ERRORLEVEL% NEQ 0 (
    echo ❌ 编译失败！
    pause
    exit /b 1
)

echo ✅ 编译成功！

echo.
echo 4. 初始化数据库（可选）...
echo 是否要初始化数据库？(y/n)
set /p choice=
if /i "%choice%"=="y" (
    echo 正在初始化数据库...
    java -cp ".;mysql-connector-java-8.0.33.jar" com.prevailingtrend.database.DatabaseInitializer
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ 数据库初始化失败！
        pause
        exit /b 1
    )
    echo ✅ 数据库初始化成功！
)

echo.
echo 5. 启动主服务器...
echo 访问地址: http://localhost:80
echo ========================================
java -cp ".;mysql-connector-java-8.0.33.jar" com.prevailingtrend.PrevailingTrendMainServer

pause