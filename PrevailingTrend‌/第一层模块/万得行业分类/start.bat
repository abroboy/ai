@echo off
echo ========================================
echo 万得行业分类仪表盘启动脚本
echo ========================================
echo.

REM 检查Java是否可用
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Java，请安装Java 17+
    pause
    exit /b 1
)

echo Java版本检查通过
echo.

REM 尝试使用Maven启动
echo 尝试使用Maven启动应用...
if exist "apache-maven-3.9.6\bin\mvn.cmd" (
    echo 使用本地Maven启动...
    apache-maven-3.9.6\bin\mvn.cmd spring-boot:run
) else (
    echo 本地Maven不可用，请安装Maven或使用IDE运行项目
    echo.
    echo 安装Maven步骤:
    echo 1. 下载: https://maven.apache.org/download.cgi
    echo 2. 解压到: C:\apache-maven
    echo 3. 添加 C:\apache-maven\bin 到PATH
    echo 4. 重新运行此脚本
    echo.
    echo 或者使用IDE (IntelliJ IDEA/Eclipse) 打开项目运行
    pause
    exit /b 1
)

echo.
echo 应用启动完成！
echo 访问地址: http://localhost:5001
echo.
pause
