@echo off
echo ========================================
echo 腾讯济安指数模块编译脚本
echo ========================================

cd /d "%~dp0\.."

echo 清理之前的编译文件...
if exist "build" rmdir /s /q build
mkdir build

echo 编译Java文件...
javac -encoding UTF-8 -d build -cp "." java\com\tencentindex\api\TencentIndexApiServer.java java\com\tencentindex\service\TencentIndexDataService.java

if %ERRORLEVEL% EQU 0 (
    echo ✅ 编译成功！
    echo 编译文件位置: build\
    echo ========================================
) else (
    echo ❌ 编译失败！
    echo 请检查Java文件是否有语法错误
    echo ========================================
    pause
    exit /b 1
)

echo 复制资源文件...
if exist "resources" xcopy /s /y resources build\resources\

echo ✅ 项目构建完成！
echo 可以使用 scripts\run.bat 启动服务器
echo ========================================
pause