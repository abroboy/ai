# 大势所趋风险框架 (PrevailingTrend Risk Framework)

## 项目概述
这是一个基于AI的智能风险分析框架，通过多个独立模块协同工作，实现自动化的风险识别、评估和预测。

## 设计原则
1. 每个模块都是独立的程序模块，生成独立的数据
2. 通过AI默认识别内容数据
3. 每个模块生成数据字段和值，由AI自动识别生成和建议
4. 通过AI推荐生成因子的计算函数和算法
5. 分配比例由AI计算和推荐
6. 每个模块一个目录，目录层级结构和设计一致
7. 使用java脚本编写代码和执行
8. 每个模块内包含自己的AI代码、程序、数据脚本
9. 数据库采用MySQL

## 技术栈
- **后端**: java 3.9+
- **数据库**: MySQL 8.0
- **AI框架**: OpenAI GPT, 本地AI模型
- **数据处理**: Pandas, NumPy
- **可视化**: Matplotlib, Plotly
- **Web框架**: Flask/FastAPI

给我一个清晰的目录结构 和 命名。 希望每个目录都能够独立运行，有自己的设计文档markdown格式。能够独立依赖外部数据源，AI引擎，输出目标数据。

所以我先要目录

## 快速开始
1. 安装依赖: `pip install -r requirements.txt`
2. 配置数据库: 修改 `config/database.py`
3. 运行主程序: `java main.py`

## 数据库配置
- Host: localhost:3306
- Username: root
- Password: rr1234RR 


AI的配置：
{  
    "title": "deepseek-v3",  
    "provider": "openai",  
    "model": "deepseek-v3",  
    "apiKey": "sk-JpmFeCKlMewNL1th8joM9Q",  
    "apiBase": "http://172.21.3.106:80"  
}