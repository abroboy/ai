@echo off
echo ========================================
echo 趋势科技数据 - 多端口服务启动脚本
echo TrendTech Data Analytics Multi-Port Services
echo ========================================
echo.
echo 正在启动所有数据监控服务...
echo.

:: 设置颜色代码
setlocal enabledelayedexpansion

echo 📊 服务端口分配:
echo    端口 5001 - 万得行业分类智能数据平台
echo    端口 5002 - 全球资金流向监控平台  
echo    端口 5003 - 国内热点数据监控平台
echo    端口 5004 - 国外热点数据监控平台
echo    端口 5005 - 腾讯济安指数监控平台
echo    端口 5006 - 论坛热点数据监控平台
echo.

echo 🚀 开始启动各模块服务...
echo.

:: 检查并启动万得行业分类模块 (端口 5001)
echo [1/6] 启动万得行业分类智能数据平台 (端口 5001)...
cd /d "%~dp0万得行业分类"
if exist "scripts\run.bat" (
    start "万得行业分类-5001" cmd /k "scripts\run.bat"
    echo    ✅ 万得行业分类服务启动中...
) else (
    echo    ❌ 未找到万得行业分类启动脚本
)
cd /d "%~dp0"

:: 等待2秒
timeout /t 2 /nobreak >nul

:: 检查并启动全球资金流向模块 (端口 5002)
echo [2/6] 启动全球资金流向监控平台 (端口 5002)...
cd /d "%~dp0全球资金流向"
if exist "scripts\run.bat" (
    start "全球资金流向-5002" cmd /k "scripts\run.bat"
    echo    ✅ 全球资金流向服务启动中...
) else (
    echo    ❌ 未找到全球资金流向启动脚本
)
cd /d "%~dp0"

:: 等待2秒
timeout /t 2 /nobreak >nul

:: 检查并启动国内热点数据模块 (端口 5003)
echo [3/6] 启动国内热点数据监控平台 (端口 5003)...
cd /d "%~dp0国内热点数据"
if exist "scripts\run.bat" (
    start "国内热点数据-5003" cmd /k "scripts\run.bat"
    echo    ✅ 国内热点数据服务启动中...
) else (
    echo    ❌ 未找到国内热点数据启动脚本
)
cd /d "%~dp0"

:: 等待2秒
timeout /t 2 /nobreak >nul

:: 检查并启动国外热点数据模块 (端口 5004)
echo [4/6] 启动国外热点数据监控平台 (端口 5004)...
cd /d "%~dp0国外热点数据"
if exist "scripts\run.bat" (
    start "国外热点数据-5004" cmd /k "scripts\run.bat"
    echo    ✅ 国外热点数据服务启动中...
) else (
    echo    ❌ 未找到国外热点数据启动脚本
)
cd /d "%~dp0"

:: 等待2秒
timeout /t 2 /nobreak >nul

:: 检查并启动腾讯济安指数模块 (端口 5005)
echo [5/6] 启动腾讯济安指数监控平台 (端口 5005)...
cd /d "%~dp0腾讯济安指数"
if exist "scripts\run.bat" (
    start "腾讯济安指数-5005" cmd /k "scripts\run.bat"
    echo    ✅ 腾讯济安指数服务启动中...
) else (
    echo    ❌ 未找到腾讯济安指数启动脚本
)
cd /d "%~dp0"

:: 等待2秒
timeout /t 2 /nobreak >nul

:: 检查并启动论坛热点数据模块 (端口 5006)
echo [6/6] 启动论坛热点数据监控平台 (端口 5006)...
cd /d "%~dp0雪球等论坛热点数据"
if exist "scripts\run.bat" (
    start "论坛热点数据-5006" cmd /k "scripts\run.bat"
    echo    ✅ 论坛热点数据服务启动中...
) else (
    echo    ❌ 未找到论坛热点数据启动脚本
)
cd /d "%~dp0"

echo.
echo ========================================
echo 🎉 所有服务启动完成！
echo ========================================
echo.
echo 📱 访问地址列表:
echo    万得行业分类智能数据平台: http://localhost:5001
echo    全球资金流向监控平台:     http://localhost:5002  
echo    国内热点数据监控平台:     http://localhost:5003
echo    国外热点数据监控平台:     http://localhost:5004
echo    腾讯济安指数监控平台:     http://localhost:5005
echo    论坛热点数据监控平台:     http://localhost:5006
echo.
echo 💡 提示:
echo    - 各服务需要1-2分钟完全启动
echo    - 如需停止服务，请关闭对应的命令行窗口
echo    - 所有服务支持实时数据刷新和API接口
echo.
echo ========================================
echo © 2025 趋势科技数据 (TrendTech Data Analytics)
echo 专业的多端口金融数据监控解决方案
echo ========================================

pause