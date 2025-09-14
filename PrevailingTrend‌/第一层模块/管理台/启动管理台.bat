@echo off
echo ========================================
echo 盛行趋势科技 - 统一管理台启动
echo PrevailingTrend Technology Management Portal
echo ========================================

:: 检查Java是否安装
java -version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 错误: 未找到Java，请确保Java已正确安装
    pause
    exit /b 1
)

:: 进入管理台目录
cd /d "%~dp0"

:: 检查是否已编译
if not exist "build\com\managementportal\api\ManagementPortalServer.class" (
    echo 🔨 编译管理台代码...
    if not exist "build" mkdir build
    javac -encoding UTF-8 -d build java\com\managementportal\api\ManagementPortalServer.java
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ 编译失败
        pause
        exit /b 1
    )
    copy index.html build\ >nul 2>&1
    echo ✅ 编译完成
)

echo 🚀 启动管理台服务器...
cd build
start "盛行趋势科技-管理台" java -cp . com.managementportal.api.ManagementPortalServer

echo.
echo ✅ 管理台正在启动...
echo 📱 请等待几秒后访问: http://localhost:8090
echo 💡 如果8090端口被占用，系统会自动尝试8091-8099端口
echo.
echo ========================================
echo © 2025 盛行趋势科技 (PrevailingTrend Technology)
echo ========================================

timeout /t 3 /nobreak >nul
start http://localhost:8090

pause