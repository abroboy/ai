@echo off
chcp 65001 > nul
echo 启动万得行业分类仪表盘...
echo.

REM 设置Java环境
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%

echo 执行数据库初始化...
python init_database.py
if errorlevel 1 (
    echo 数据库初始化失败，请检查配置
    pause
    exit /b 1
)

echo.
echo 使用Maven启动Spring Boot应用...
echo 如果Maven未安装，请先安装Maven或使用IDE运行
mvn spring-boot:run

pause