# 本地开发环境启动脚本
# 版本: 1.0
# 用途: 启动大势所趋风险框架管理台

# 1. 设置环境变量
$env:NODE_ENV = "development"

# 2. 安装依赖
Write-Host "正在安装开发依赖..."
npm install

# 3. 启动开发服务器
Write-Host "正在启动开发服务器..."
npm run dev

Write-Host "启动完成! 访问地址: http://localhost:3000"