@echo off
chcp 65001
echo ========================================
echo 大势所趋风险框架 - 管理台启动中...
echo ========================================

REM 设置Java环境
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%

REM 进入项目目录
cd /d "%~dp0"

echo 正在启动管理台...
echo 服务端口: 8090
echo 访问地址: http://localhost:8090/管理台/
echo ========================================

REM 自动打开浏览器
start http://localhost:8090/管理台/

REM 使用Python启动HTTP服务器
python -m http.server 8090

pause
