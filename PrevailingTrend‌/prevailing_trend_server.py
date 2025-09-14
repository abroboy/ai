#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
import webbrowser
import threading
import time

class PrevailingTrendHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            self.send_main_page()
        elif self.path.startswith('/layer'):
            self.send_layer_page()
        elif self.path.startswith('/api/'):
            self.send_api_response()
        else:
            self.send_404()
    
    def send_main_page(self):
        html_content = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>大势所趋风险框架 - PrevailingTrend Risk Framework</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
            <style>
                body {
                    font-family: 'Microsoft YaHei', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    margin: 0;
                    padding: 0;
                }
                .layout-container {
                    display: flex;
                    min-height: 100vh;
                }
                .main-content {
                    flex: 1;
                    background: rgba(255, 255, 255, 0.95);
                    margin: 20px 10px 20px 20px;
                    border-radius: 20px 0 0 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    backdrop-filter: blur(10px);
                    padding: 40px;
                    overflow-y: auto;
                }
                .sidebar {
                    width: 350px;
                    background: rgba(255, 255, 255, 0.98);
                    margin: 20px 20px 20px 10px;
                    border-radius: 0 20px 20px 0;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    backdrop-filter: blur(10px);
                    padding: 30px 25px;
                    overflow-y: auto;
                }
                .header-section {
                    text-align: center;
                    margin-bottom: 40px;
                }
                .header-title {
                    font-size: 2.5rem;
                    font-weight: 700;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }
                .layer-card {
                    background: white;
                    border-radius: 15px;
                    padding: 25px;
                    margin-bottom: 25px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                    border-left: 5px solid;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }
                .layer-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                }
                .layer-1 { border-left-color: #e74c3c; }
                .layer-2 { border-left-color: #f39c12; }
                .layer-3 { border-left-color: #f1c40f; }
                .layer-4 { border-left-color: #2ecc71; }
                .layer-5 { border-left-color: #3498db; }
                .layer-6 { border-left-color: #9b59b6; }
                .layer-title {
                    font-size: 1.2rem;
                    font-weight: 600;
                    margin-bottom: 15px;
                    display: flex;
                    align-items: center;
                }
                .layer-icon {
                    margin-right: 15px;
                    width: 35px;
                    height: 35px;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 1rem;
                }
                .module-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                    gap: 12px;
                    margin-top: 15px;
                }
                .module-btn {
                    padding: 12px;
                    border: 2px solid #e9ecef;
                    border-radius: 8px;
                    background: #f8f9fa;
                    text-decoration: none;
                    color: #495057;
                    font-weight: 500;
                    text-align: center;
                    transition: all 0.3s ease;
                    display: block;
                    cursor: pointer;
                    font-size: 0.9rem;
                }
                .module-btn:hover {
                    border-color: #007bff;
                    background: #007bff;
                    color: white;
                    text-decoration: none;
                    transform: scale(1.05);
                }
                .sidebar-header {
                    text-align: center;
                    margin-bottom: 30px;
                    padding-bottom: 20px;
                    border-bottom: 2px solid #e9ecef;
                }
                .sidebar-title {
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: #2c3e50;
                    margin-bottom: 8px;
                }
                .toc-section {
                    margin-bottom: 25px;
                }
                .toc-title {
                    font-size: 1.1rem;
                    font-weight: 600;
                    color: #495057;
                    margin-bottom: 15px;
                    padding-bottom: 8px;
                    border-bottom: 1px solid #dee2e6;
                }
                .toc-item {
                    display: block;
                    padding: 8px 15px;
                    color: #6c757d;
                    text-decoration: none;
                    border-radius: 6px;
                    transition: all 0.3s ease;
                    margin-bottom: 3px;
                    font-size: 0.9rem;
                }
                .toc-item:hover {
                    background: #f8f9fa;
                    color: #007bff;
                    text-decoration: none;
                    transform: translateX(5px);
                }
                .toc-item.active {
                    background: #007bff;
                    color: white;
                }
                .data-flow-section {
                    background: white;
                    border-radius: 15px;
                    padding: 25px;
                    margin-bottom: 25px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                }
                .flow-diagram {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 15px;
                }
                .flow-step {
                    flex: 1;
                    min-width: 120px;
                    text-align: center;
                    position: relative;
                }
                .flow-step::after {
                    content: '→';
                    position: absolute;
                    right: -12px;
                    top: 50%;
                    transform: translateY(-50%);
                    font-size: 20px;
                    color: #6c757d;
                }
                .flow-step:last-child::after {
                    display: none;
                }
                .flow-icon {
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 8px auto;
                    color: white;
                    font-size: 18px;
                    font-weight: 600;
                }
                .stats-section {
                    background: white;
                    border-radius: 15px;
                    padding: 25px;
                    margin-top: 25px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                }
                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 15px;
                }
                .stat-card {
                    text-align: center;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 8px;
                    border: 2px solid transparent;
                    transition: all 0.3s ease;
                }
                .stat-card:hover {
                    border-color: #007bff;
                    transform: translateY(-2px);
                }
                .stat-number {
                    font-size: 1.8rem;
                    font-weight: 700;
                    margin-bottom: 5px;
                }
                .stat-label {
                    font-size: 0.85rem;
                    color: #6c757d;
                }
                @media (max-width: 1200px) {
                    .layout-container {
                        flex-direction: column;
                    }
                    .sidebar {
                        width: 100%;
                        margin: 20px;
                        border-radius: 20px;
                        order: 2;
                    }
                    .main-content {
                        margin: 20px;
                        border-radius: 20px;
                        order: 1;
                    }
                }
        </head>
        <body>
            <div class="layout-container">
                <!-- 主要内容区域 -->
                <div class="main-content">
                    <div class="header-section">
                        <h1 class="header-title">
                            <i class="bi bi-graph-up-arrow"></i>
                            大势所趋风险框架
                        </h1>
                        <p class="text-muted">PrevailingTrend Risk Framework</p>
                        <p class="text-muted">基于AI的智能风险分析框架 - 六层模块协同工作</p>
                        <div class="alert alert-info">
                            <i class="bi bi-info-circle"></i>
                            统一端口80访问 | 完整六层架构 | 实时数据流向监控
                        </div>
                    </div>
                    
                    <!-- 数据流向图 -->
                    <div class="data-flow-section">
                        <h4 class="mb-4"><i class="bi bi-diagram-3"></i> 数据流向架构图</h4>
                        <div class="flow-diagram">
                            <div class="flow-step">
                                <div class="flow-icon bg-danger">L1</div>
                                <h6>数据采集</h6>
                                <small>基础数据源</small>
                            </div>
                            <div class="flow-step">
                                <div class="flow-icon bg-warning">L2</div>
                                <h6>AI加工</h6>
                                <small>智能处理</small>
                            </div>
                            <div class="flow-step">
                                <div class="flow-icon bg-info">L3</div>
                                <h6>深度挖掘</h6>
                                <small>多维分析</small>
                            </div>
                            <div class="flow-step">
                                <div class="flow-icon bg-success">L4</div>
                                <h6>评分算法</h6>
                                <small>智能评分</small>
                            </div>
                            <div class="flow-step">
                                <div class="flow-icon bg-primary">L5</div>
                                <h6>因子权重</h6>
                                <small>权重分析</small>
                            </div>
                            <div class="flow-step">
                                <div class="flow-icon bg-dark">L6</div>
                                <h6>曲线预测</h6>
                                <small>预测分析</small>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 第一层模块 -->
                    <div id="layer1" class="layer-card layer-1">
                        <div class="layer-title">
                            <div class="layer-icon bg-danger">
                                <i class="bi bi-database"></i>
                            </div>
                            第一层模块 - 基础数据采集
                        </div>
                        <p class="text-muted">信息数据有严格的时间限制，要二次确认数据是指定日期之前的数据</p>
                        <div class="module-grid">
                            <div class="module-btn" onclick="openModule('layer1', 'company-list')">公司名字列表</div>
                            <div class="module-btn" onclick="openModule('layer1', 'wind-industry')">万得行业分类</div>
                            <div class="module-btn" onclick="openModule('layer1', 'domestic-hotspot')">国内热点数据</div>
                            <div class="module-btn" onclick="openModule('layer1', 'international-hotspot')">国外热点数据</div>
                            <div class="module-btn" onclick="openModule('layer1', 'forum-hotspot')">雪球等论坛热点数据</div>
                            <div class="module-btn" onclick="openModule('layer1', 'tencent-index')">腾讯济安指数</div>
                            <div class="module-btn" onclick="openModule('layer1', 'global-capital-flow')">全球资金流向</div>
                            <div class="module-btn" onclick="openModule('layer1', 'internet-info')">其他互联网信息</div>
                        </div>
                    </div>
                    
                    <!-- 第二层模块 -->
                    <div id="layer2" class="layer-card layer-2">
                        <div class="layer-title">
                            <div class="layer-icon bg-warning">
                                <i class="bi bi-gear"></i>
                            </div>
                            第二层模块 - AI数据加工
                        </div>
                        <p class="text-muted">通过AI加工第一层数据，生成公司属性和热点分析</p>
                        <div class="module-grid">
                            <div class="module-btn" onclick="openModule('layer2', 'company-attributes')">公司属性表</div>
                            <div class="module-btn" onclick="openModule('layer2', 'hotspot-data')">热点数据表</div>
                        </div>
                    </div>
                    
                    <!-- 第三层模块 -->
                    <div id="layer3" class="layer-card layer-3">
                        <div class="layer-title">
                            <div class="layer-icon bg-info">
                                <i class="bi bi-search"></i>
                            </div>
                            第三层模块 - 深度数据挖掘
                        </div>
                        <p class="text-muted">依赖第二层筛选出来的行业和公司，继续按照目标去排查以下数据</p>
                        <div class="module-grid">
                            <div class="module-btn" onclick="openModule('layer3', 'tax-bank-report')">税银报告</div>
                            <div class="module-btn" onclick="openModule('layer3', 'financial-statements')">财务三表</div>
                            <div class="module-btn" onclick="openModule('layer3', 'enterprise-check')">企查查数据</div>
                            <div class="module-btn" onclick="openModule('layer3', 'forum-data')">雪球等论坛数据</div>
                        </div>
                    </div>
                    
                    <!-- 第四层模块 -->
                    <div id="layer4" class="layer-card layer-4">
                        <div class="layer-title">
                            <div class="layer-icon bg-success">
                                <i class="bi bi-calculator"></i>
                            </div>
                            第四层模块 - 智能评分算法
                        </div>
                        <p class="text-muted">依赖第三层的数据，通过AI找一个算法来计算</p>
                        <div class="module-grid">
                            <div class="module-btn" onclick="openModule('layer4', 'industry-score')">行业分值表</div>
                            <div class="module-btn" onclick="openModule('layer4', 'company-score')">公司分值表</div>
                            <div class="module-btn" onclick="openModule('layer4', 'industry-company-score')">行业+公司分值表</div>
                        </div>
                    </div>
                    
                    <!-- 第五层模块 -->
                    <div id="layer5" class="layer-card layer-5">
                        <div class="layer-title">
                            <div class="layer-icon bg-primary">
                                <i class="bi bi-sliders"></i>
                            </div>
                            第五层模块 - 因子权重分析
                        </div>
                        <p class="text-muted">通过因子权重，预测行业或公司业绩历史数据曲线，或二级市场曲线原始数据</p>
                        <div class="module-grid">
                            <div class="module-btn" onclick="openModule('layer5', 'factor-weights')">对象因子权重表</div>
                        </div>
                    </div>
                    
                    <!-- 第六层模块 -->
                    <div id="layer6" class="layer-card layer-6">
                        <div class="layer-title">
                            <div class="layer-icon bg-dark">
                                <i class="bi bi-graph-up"></i>
                            </div>
                            第六层模块 - 曲线预测分析
                        </div>
                        <p class="text-muted">类似chatBI的能力，把数据曲线化。能够通过调整因子权重输出对比的曲线</p>
                        <div class="module-grid">
                            <div class="module-btn" onclick="openModule('layer6', 'curve-prediction')">曲线预测分析</div>
                        </div>
                    </div>
                </div>
                
                <!-- 右侧导航目录 -->
                <div class="sidebar">
                    <div class="sidebar-header">
                        <h4 class="sidebar-title">
                            <i class="bi bi-list-ul"></i>
                            导航目录
                        </h4>
                        <p class="text-muted mb-0">快速访问各层模块</p>
                    </div>
                    
                    <!-- 第一层导航 -->
                    <div class="toc-section">
                        <div class="toc-title">
                            <i class="bi bi-database text-danger"></i>
                            第一层 - 数据采集
                        </div>
                        <a href="#layer1" class="toc-item" onclick="scrollToLayer('layer1')">公司名字列表</a>
                        <a href="#layer1" class="toc-item" onclick="scrollToLayer('layer1')">万得行业分类</a>
                        <a href="#layer1" class="toc-item" onclick="scrollToLayer('layer1')">国内热点数据</a>
                        <a href="#layer1" class="toc-item" onclick="scrollToLayer('layer1')">国外热点数据</a>
                        <a href="#layer1" class="toc-item" onclick="scrollToLayer('layer1')">雪球等论坛热点</a>
                        <a href="#layer1" class="toc-item" onclick="scrollToLayer('layer1')">腾讯济安指数</a>
                        <a href="#layer1" class="toc-item" onclick="scrollToLayer('layer1')">全球资金流向</a>
                        <a href="#layer1" class="toc-item" onclick="scrollToLayer('layer1')">其他互联网信息</a>
                    </div>
                    
                    <!-- 第二层导航 -->
                    <div class="toc-section">
                        <div class="toc-title">
                            <i class="bi bi-gear text-warning"></i>
                            第二层 - AI数据加工
                        </div>
                        <a href="#layer2" class="toc-item" onclick="scrollToLayer('layer2')">公司属性表</a>
                        <a href="#layer2" class="toc-item" onclick="scrollToLayer('layer2')">热点数据表</a>
                    </div>
                    
                    <!-- 第三层导航 -->
                    <div class="toc-section">
                        <div class="toc-title">
                            <i class="bi bi-search text-info"></i>
                            第三层 - 深度挖掘
                        </div>
                        <a href="#layer3" class="toc-item" onclick="scrollToLayer('layer3')">税银报告</a>
                        <a href="#layer3" class="toc-item" onclick="scrollToLayer('layer3')">财务三表</a>
                        <a href="#layer3" class="toc-item" onclick="scrollToLayer('layer3')">企查查数据</a>
                        <a href="#layer3" class="toc-item" onclick="scrollToLayer('layer3')">雪球等论坛数据</a>
                    </div>
                    
                    <!-- 第四层导航 -->
                    <div class="toc-section">
                        <div class="toc-title">
                            <i class="bi bi-calculator text-success"></i>
                            第四层 - 智能评分
                        </div>
                        <a href="#layer4" class="toc-item" onclick="scrollToLayer('layer4')">行业分值表</a>
                        <a href="#layer4" class="toc-item" onclick="scrollToLayer('layer4')">公司分值表</a>
                        <a href="#layer4" class="toc-item" onclick="scrollToLayer('layer4')">行业+公司分值表</a>
                    </div>
                    
                    <!-- 第五层导航 -->
                    <div class="toc-section">
                        <div class="toc-title">
                            <i class="bi bi-sliders text-primary"></i>
                            第五层 - 因子权重
                        </div>
                        <a href="#layer5" class="toc-item" onclick="scrollToLayer('layer5')">对象因子权重表</a>
                    </div>
                    
                    <!-- 第六层导航 -->
                    <div class="toc-section">
                        <div class="toc-title">
                            <i class="bi bi-graph-up text-dark"></i>
                            第六层 - 曲线预测
                        </div>
                        <a href="#layer6" class="toc-item" onclick="scrollToLayer('layer6')">曲线预测分析</a>
                    </div>
                    
                    <!-- 统计信息区域 -->
                    <div class="stats-section">
                        <h6 class="mb-3">
                            <i class="bi bi-bar-chart"></i>
                            系统统计
                        </h6>
                        <div class="stats-grid">
                            <div class="stat-card">
                                <div class="stat-number text-primary">6</div>
                                <div class="stat-label">层级模块</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number text-success">18</div>
                                <div class="stat-label">功能模块</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number text-info">80</div>
                                <div class="stat-label">统一端口</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number text-warning">AI</div>
                                <div class="stat-label">智能分析</div>
                            </div>
                        </div>
                        
                        <div class="mt-3 text-center">
                            <div class="text-muted small">
                                <i class="bi bi-shield-check"></i>
                                v1.0 | MySQL | AI分析
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                function openModule(layer, module) {
                    const url = '/' + layer + '/' + module;
                    window.open(url, '_blank');
                }
                
                function scrollToLayer(layerId) {
                    const element = document.querySelector('.layer-' + layerId.replace('layer', ''));
                    if (element) {
                        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        
                        // 高亮效果
                        element.style.transform = 'scale(1.02)';
                        element.style.boxShadow = '0 15px 30px rgba(0,0,0,0.2)';
                        
                        setTimeout(() => {
                            element.style.transform = '';
                            element.style.boxShadow = '';
                        }, 1000);
                    }
                }
                
                // 页面加载完成后的初始化
                document.addEventListener('DOMContentLoaded', function() {
                    console.log('大势所趋风险框架管理台已加载');
                    
                    // 监听滚动事件，更新导航状态
                    window.addEventListener('scroll', function() {
                        const layers = document.querySelectorAll('.layer-card');
                        const tocItems = document.querySelectorAll('.toc-item');
                        
                        layers.forEach((layer, index) => {
                            const rect = layer.getBoundingClientRect();
                            if (rect.top <= 100 && rect.bottom >= 100) {
                                // 移除所有活动状态
                                tocItems.forEach(item => item.classList.remove('active'));
                                
                                // 激活当前层的导航项
                                const layerClass = layer.className.match(/layer-(\d+)/);
                                if (layerClass) {
                                    const layerNum = layerClass[1];
                                    const currentSection = document.querySelectorAll(`.toc-section:nth-child(${parseInt(layerNum) + 1}) .toc-item`);
                                    currentSection.forEach(item => item.classList.add('active'));
                                }
                            }
                        });
                    });
                });
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def send_layer_page(self):
        path_parts = self.path.split('/')
        if len(path_parts) >= 3:
            layer = path_parts[1]
            module = path_parts[2] if len(path_parts) > 2 else ''
            
            html_content = f"""
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{layer} - {module}</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
            </head>
            <body>
                <div class="container mt-4">
                    <nav aria-label="breadcrumb">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item"><a href="/">首页</a></li>
                            <li class="breadcrumb-item"><a href="/{layer}/">{layer}</a></li>
                            <li class="breadcrumb-item active">{module}</li>
                        </ol>
                    </nav>
                    
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h3><i class="bi bi-gear"></i> {layer} - {module}</h3>
                        </div>
                        <div class="card-body">
                            <div class="alert alert-info">
                                <i class="bi bi-info-circle"></i>
                                此模块正在开发中，将提供完整的数据管理和分析功能。
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6">
                                    <h5>功能特性</h5>
                                    <ul class="list-group list-group-flush">
                                        <li class="list-group-item">数据采集和存储</li>
                                        <li class="list-group-item">AI智能分析</li>
                                        <li class="list-group-item">实时数据监控</li>
                                        <li class="list-group-item">可视化图表展示</li>
                                        <li class="list-group-item">数据导出功能</li>
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <h5>技术架构</h5>
                                    <ul class="list-group list-group-flush">
                                        <li class="list-group-item">MySQL数据库存储</li>
                                        <li class="list-group-item">REST API接口</li>
                                        <li class="list-group-item">Bootstrap响应式界面</li>
                                        <li class="list-group-item">实时数据更新</li>
                                        <li class="list-group-item">安全访问控制</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div class="mt-4">
                                <a href="/" class="btn btn-primary">
                                    <i class="bi bi-house"></i> 返回首页
                                </a>
                                <button class="btn btn-success" onclick="loadSampleData()">
                                    <i class="bi bi-database"></i> 加载示例数据
                                </button>
                                <button class="btn btn-info" onclick="refreshData()">
                                    <i class="bi bi-arrow-clockwise"></i> 刷新数据
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script>
                    function loadSampleData() {{
                        alert('示例数据加载功能即将推出');
                    }}
                    
                    function refreshData() {{
                        location.reload();
                    }}
                </script>
            </body>
            </html>
            """
        else:
            html_content = "<h1>层级页面</h1><p>无效的路径</p>"
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def send_api_response(self):
        # 模拟API响应
        response_data = {
            "status": "success",
            "message": "API正在开发中",
            "data": [],
            "timestamp": int(time.time())
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
    
    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html_content = """
        <html>
        <head><title>404 - 页面未找到</title></head>
        <body>
            <h1>404 - 页面未找到</h1>
            <p><a href="/">返回首页</a></p>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

def start_server():
    server_address = ('', 80)
    httpd = HTTPServer(server_address, PrevailingTrendHandler)
    print("========================================")
    print("大势所趋风险框架 - Python服务器启动中...")
    print("PrevailingTrend Risk Framework")
    print("统一端口：80")
    print("========================================")
    print("✅ 服务器启动成功！")
    print("访问地址: http://localhost:80")
    print("========================================")
    
    # 自动打开浏览器
    def open_browser():
        time.sleep(1)
        webbrowser.open('http://localhost:80')
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        httpd.server_close()

if __name__ == '__main__':
    start_server()