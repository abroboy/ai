@echo off
echo ========================================
echo 全球资金流向监控服务器启动
echo ========================================

cd /d "%~dp0\.."

echo 检查编译文件...
if not exist "build\com\globalcapitalflow\api\GlobalCapitalFlowApiServer.class" (
    echo 编译文件不存在，开始编译...
    call scripts\compile.bat
    if %ERRORLEVEL% NEQ 0 (
        echo 编译失败，无法启动服务器
        pause
        exit /b 1
    )
)

echo 启动全球资金流向监控服务器...
cd build
java -cp "." com.globalcapitalflow.api.GlobalCapitalFlowApiServer

pause