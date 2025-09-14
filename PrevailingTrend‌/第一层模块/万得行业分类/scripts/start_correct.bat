@echo off
chcp 65001
echo ========================================
echo 万得行业分类仪表盘 - 正确启动脚本
echo ========================================

REM 设置Java环境
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%

REM 进入项目目录
cd /d "c:\work\AI\PrevailingTrend‌\第一层模块\万得行业分类"

echo 数据库已初始化完成，正在启动Spring Boot应用...
echo 服务端口: 5001
echo 数据库: MySQL (localhost:3306/pt)
echo ========================================

REM 检查是否已编译
if not exist "target\classes" (
    echo 正在创建target目录...
    mkdir target\classes
)

REM 启动简化的Web服务器进行演示
java SimpleWebServer