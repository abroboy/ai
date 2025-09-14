# 全球资金流向系统 - 新架构说明

## 架构变更

系统已重构为两个独立的模块：

### 1. 数据收集服务 (Data Collector Service)
- **文件**: `data_collector_service.py`
- **端口**: 5004
- **功能**: 
  - 数据拉取和入库
  - 数据分析处理
  - 数据库管理
  - 定时任务调度

### 2. 数据展示服务 (Display Service)
- **文件**: `display_service.py`
- **端口**: 5003
- **功能**:
  - 数据可视化展示
  - Web界面服务
  - API接口提供
  - 无密码管理

## 主要改进

### ✅ 已完成的改进
1. **去掉密码管理**: 展示服务不再需要登录验证
2. **模块分离**: 数据收集和展示完全独立
3. **服务解耦**: 两个服务可以独立启动和停止
4. **端口分离**: 不同服务使用不同端口

### 🔧 服务管理
- **统一启动**: 使用 `start_services.py` 管理两个服务
- **独立启动**: 可以单独启动任一服务
- **状态监控**: 每个服务都有独立的健康检查

## 启动方式

### 方式1: 使用服务管理器
```bash
java start_services.py
```

### 方式2: 独立启动
```bash
# 启动数据收集服务
java data_collector_service.py

# 启动数据展示服务
java display_service.py
```

## API接口

### 数据收集服务 (端口5004)
- `GET /api/status` - 服务状态
- `POST /api/start_collection` - 启动数据收集
- `POST /api/stop_collection` - 停止数据收集
- `POST /api/collect_once` - 执行一次收集
- `GET /api/database_info` - 数据库信息
- `GET /api/health` - 健康检查

### 数据展示服务 (端口5003)
- `GET /` - 首页
- `GET /dashboard` - 仪表盘
- `GET /api/dashboard_data` - 仪表盘数据
- `GET /api/flow_analysis` - 资金流向分析
- `GET /api/system_status` - 系统状态
- `GET /api/health` - 健康检查

## 访问地址

### 数据展示服务
- **首页**: http://localhost:5003/
- **仪表盘**: http://localhost:5003/dashboard

### 数据收集服务
- **API状态**: http://localhost:5004/api/status
- **健康检查**: http://localhost:5004/api/health

## 优势

1. **高可用性**: 一个服务故障不影响另一个
2. **可扩展性**: 可以独立扩展任一服务
3. **维护性**: 代码结构更清晰，便于维护
4. **安全性**: 展示服务无敏感操作，更安全
5. **灵活性**: 可以根据需要启动不同服务

## 注意事项

1. 数据收集服务需要数据库连接
2. 两个服务可以独立运行，也可以协同工作
3. 展示服务目前使用模拟数据，实际使用时需要连接数据库
4. 建议先启动数据收集服务，再启动展示服务 