@echo off
chcp 65001
echo ========================================
echo 大势所趋风险框架 - 简化版启动
echo PrevailingTrend Risk Framework
echo ========================================

echo 编译Java文件...
javac -encoding UTF-8 PrevailingTrendSimpleServer.java

if %ERRORLEVEL% NEQ 0 (
    echo 编译失败！
    pause
    exit /b 1
)

echo 编译成功！

echo 启动服务器...
echo 访问地址: http://localhost:80
echo ========================================

java com.prevailingtrend.PrevailingTrendSimpleServer

pause