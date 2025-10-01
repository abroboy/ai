@echo off
chcp 65001 >nul
title 全球资金流向模块启动器

echo ====================================
echo 全球资金流向模块启动器
echo ====================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python环境
    echo 请先安装Python 3.7+
    pause
    exit /b 1
)

echo Python环境检查通过
echo.

echo 正在检查依赖包...
python -c "import flask, pandas" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install flask flask-cors pandas requests
    if errorlevel 1 (
        echo 依赖包安装失败
        pause
        exit /b 1
    )
)

echo 依赖包检查通过
echo.

echo 正在运行模块测试...
python test_global_capital_flow.py
echo.

echo 测试完成，按任意键启动API服务器...
pause >nul

echo 正在启动API服务器...
echo 服务地址: http://localhost:5001
echo 按 Ctrl+C 停止服务
echo.

python start_api_server.py

echo.
echo 服务已停止
pause