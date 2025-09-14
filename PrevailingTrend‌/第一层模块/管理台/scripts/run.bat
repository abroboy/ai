@echo off
echo ========================================
echo 趋势科技数据统一管理台启动
echo ========================================

cd /d "%~dp0\.."

echo 检查编译文件...
if not exist "build\com\managementportal\api\ManagementPortalServer.class" (
    echo 编译文件不存在，开始编译...
    call scripts\compile.bat
    if %ERRORLEVEL% NEQ 0 (
        echo 编译失败，无法启动服务器
        pause
        exit /b 1
    )
)

echo 启动趋势科技数据统一管理台...
cd build
java -cp "." com.managementportal.api.ManagementPortalServer

pause