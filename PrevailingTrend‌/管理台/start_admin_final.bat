@echo off
echo 启动大势所趋风险框架管理台...
echo.

echo 启动增强版国内热点数据API服务器...
start "国内热点数据API" cmd /k "cd /d \"%~dp0..\第一层模块\国内热点数据\" && java -cp java com.domestichotspot.api.DomesticHotspotApiServer"

echo 等待API服务器启动...
timeout /t 3 /nobreak >nul

echo 启动管理台HTTP服务器...
start "管理台服务器" cmd /k "cd /d \"%~dp0\" && python -m http.server 8090"

echo 等待管理台服务器启动...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo 大势所趋风险框架管理台启动完成！
echo ========================================
echo.
echo 访问地址：
echo   增强版管理台: http://localhost:8090/index_final.html
echo   测试页面: http://localhost:8090/test_enhanced_hotspot.html
echo   原始管理台: http://localhost:8090/index.html
echo.
echo 增强版国内热点数据API: /api/domestic-hotspot (同端口)
echo.
echo 按任意键打开浏览器...
pause >nul

start http://localhost:8090/index_final.html

echo.
echo 管理台已启动，按任意键退出...
pause >nul
