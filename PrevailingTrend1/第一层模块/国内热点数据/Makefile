# 国内热点数据模块 Makefile

.PHONY: help install test run clean logs

# 默认目标
help:
	@echo "国内热点数据模块管理命令:"
	@echo "  install    - 安装依赖包"
	@echo "  test       - 运行测试"
	@echo "  run        - 启动服务"
	@echo "  run-web    - 仅启动Web服务"
	@echo "  clean      - 清理临时文件"
	@echo "  logs       - 查看日志"
	@echo "  db-test    - 运行数据库测试"

# 安装依赖
install:
	@echo "安装依赖包..."
	pip install -r requirements.txt

# 运行测试
test:
	@echo "运行模块测试..."
	python test_module.py

# 运行数据库测试
db-test:
	@echo "运行数据库测试..."
	python hotspot_test.py

# 启动完整服务
run:
	@echo "启动完整服务..."
	python start.py

# 仅启动Web服务
run-web:
	@echo "启动Web服务..."
	python app.py

# 清理临时文件
clean:
	@echo "清理临时文件..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete

# 查看日志
logs:
	@echo "查看最新日志..."
	tail -f logs/hotspot.log

# 创建日志目录
setup:
	@echo "创建必要目录..."
	mkdir -p logs
	mkdir -p static/js
	@echo "复制环境变量文件..."
	cp env.example .env
	@echo "设置完成，请编辑 .env 文件配置数据库连接"

# 数据库初始化
init-db:
	@echo "初始化数据库..."
	python -c "from utils.database import db_manager; db_manager.create_tables()"

# 开发模式
dev:
	@echo "启动开发模式..."
	export FLASK_ENV=development
	python app.py 