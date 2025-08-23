# 万得行业分类模块 Makefile

.PHONY: help install test lint format clean build run docker-build docker-run docker-stop setup-db monitor

# 默认目标
help:
	@echo "万得行业分类模块 - 可用命令:"
	@echo ""
	@echo "开发命令:"
	@echo "  install      - 安装依赖包"
	@echo "  test         - 运行测试"
	@echo "  lint         - 代码检查"
	@echo "  format       - 代码格式化"
	@echo "  clean        - 清理临时文件"
	@echo ""
	@echo "运行命令:"
	@echo "  run          - 启动API服务"
	@echo "  run-demo     - 运行演示程序"
	@echo "  setup-db     - 初始化数据库"
	@echo "  monitor      - 运行监控脚本"
	@echo ""
	@echo "Docker命令:"
	@echo "  docker-build - 构建Docker镜像"
	@echo "  docker-run   - 运行Docker容器"
	@echo "  docker-stop  - 停止Docker容器"
	@echo "  docker-compose-up   - 启动Docker Compose服务"
	@echo "  docker-compose-down - 停止Docker Compose服务"
	@echo ""
	@echo "部署命令:"
	@echo "  build        - 构建项目"
	@echo "  deploy       - 部署到生产环境"

# 安装依赖
install:
	@echo "安装Python依赖包..."
	pip install -r requirements.txt
	@echo "依赖安装完成"

# 运行测试
test:
	@echo "运行单元测试..."
	python -m pytest tests/ -v --cov=. --cov-report=html
	@echo "测试完成"

# 代码检查
lint:
	@echo "运行代码检查..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	@echo "代码检查完成"

# 代码格式化
format:
	@echo "格式化代码..."
	black . --line-length=127
	@echo "代码格式化完成"

# 清理临时文件
clean:
	@echo "清理临时文件..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	@echo "清理完成"

# 构建项目
build: clean
	@echo "构建项目..."
	python setup.py build
	@echo "构建完成"

# 启动API服务
run:
	@echo "启动API服务..."
	python api_server.py --service combined --port 5000

# 运行演示程序
run-demo:
	@echo "运行演示程序..."
	python run_demo.py

# 初始化数据库
setup-db:
	@echo "初始化数据库..."
	python scripts/setup_database.py --action all

# 运行监控脚本
monitor:
	@echo "运行监控脚本..."
	python scripts/monitor.py --check all

# 构建Docker镜像
docker-build:
	@echo "构建Docker镜像..."
	docker build -t industry-classification .
	@echo "Docker镜像构建完成"

# 运行Docker容器
docker-run:
	@echo "运行Docker容器..."
	docker run -d -p 5000:5000 --name industry-api industry-classification
	@echo "Docker容器启动完成"

# 停止Docker容器
docker-stop:
	@echo "停止Docker容器..."
	docker stop industry-api || true
	docker rm industry-api || true
	@echo "Docker容器已停止"

# 启动Docker Compose服务
docker-compose-up:
	@echo "启动Docker Compose服务..."
	docker-compose up -d
	@echo "Docker Compose服务启动完成"

# 停止Docker Compose服务
docker-compose-down:
	@echo "停止Docker Compose服务..."
	docker-compose down
	@echo "Docker Compose服务已停止"

# 查看Docker Compose日志
docker-compose-logs:
	@echo "查看Docker Compose日志..."
	docker-compose logs -f

# 部署到生产环境
deploy: clean test docker-build
	@echo "部署到生产环境..."
	docker-compose down
	docker-compose up -d
	@echo "部署完成"

# 开发环境设置
dev-setup: install setup-db
	@echo "开发环境设置完成"

# 生产环境设置
prod-setup: install setup-db docker-build
	@echo "生产环境设置完成"

# 完整测试
full-test: lint test
	@echo "完整测试完成"

# 代码质量检查
quality: format lint test
	@echo "代码质量检查完成"

# 备份数据库
backup:
	@echo "备份数据库..."
	mysqldump -u root -p prevailing_trend > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "数据库备份完成"

# 恢复数据库
restore:
	@echo "恢复数据库..."
	@read -p "请输入备份文件名: " backup_file; \
	mysql -u root -p prevailing_trend < $$backup_file
	@echo "数据库恢复完成"

# 查看服务状态
status:
	@echo "查看服务状态..."
	@echo "API服务状态:"
	@curl -s http://localhost:5000/health || echo "API服务未运行"
	@echo ""
	@echo "Docker容器状态:"
	@docker ps --filter "name=industry" || echo "无相关容器运行"

# 查看日志
logs:
	@echo "查看应用日志..."
	@tail -f logs/industry_classification_$(shell date +%Y%m%d).log

# 性能测试
benchmark:
	@echo "运行性能测试..."
	@ab -n 1000 -c 10 http://localhost:5000/health || echo "性能测试失败"

# 安全扫描
security-scan:
	@echo "运行安全扫描..."
	@bandit -r . || echo "安全扫描完成"

# 依赖检查
check-deps:
	@echo "检查依赖包..."
	@pip list --outdated || echo "依赖检查完成"

# 更新依赖
update-deps:
	@echo "更新依赖包..."
	@pip install --upgrade -r requirements.txt
	@echo "依赖更新完成"

# 创建发布版本
release:
	@echo "创建发布版本..."
	@read -p "请输入版本号: " version; \
	git tag -a v$$version -m "Release version $$version"; \
	git push origin v$$version
	@echo "发布版本创建完成"

# 帮助信息
.DEFAULT_GOAL := help 