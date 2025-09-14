@echo off
echo ========================================
echo 万得行业分类动态股票数据服务器启动
echo ========================================

cd /d "%~dp0\.."

echo 检查编译文件...
if not exist "build\com\windindustry\api\DynamicStockApiServer.class" (
    echo 编译文件不存在，开始编译...
    call scripts\compile.bat
    if %ERRORLEVEL% NEQ 0 (
        echo 编译失败，无法启动服务器
        pause
        exit /b 1
    )
)

echo 启动动态股票数据服务器...
cd build
java -cp "." com.windindustry.api.DynamicStockApiServer

pause