#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
曲线预测可视化模块
提供预测结果的可视化功能
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker
import os
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('curve_visualization')

class CurveVisualizer:
    """曲线预测可视化类"""
    
    def __init__(self, theme='default', figsize=(12, 8), dpi=100):
        """
        初始化曲线预测可视化
        
        参数:
            theme: 可视化主题
            figsize: 图形大小
            dpi: 图形分辨率
        """
        self.theme = theme
        self.figsize = figsize
        self.dpi = dpi
        
        # 设置绘图风格
        if theme == 'dark':
            plt.style.use('dark_background')
            self.colors = {
                'actual': '#1f77b4',
                'predicted': '#ff7f0e',
                'upper_bound': '#2ca02c',
                'lower_bound': '#d62728',
                'grid': '#555555'
            }
        else:
            plt.style.use('seaborn-whitegrid')
            self.colors = {
                'actual': '#1f77b4',
                'predicted': '#ff7f0e',
                'upper_bound': '#2ca02c',
                'lower_bound': '#d62728',
                'grid': '#cccccc'
            }
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    def plot_prediction(self, actual_data, predicted_data, confidence_intervals=None, title=None, xlabel=None, ylabel=None, save_path=None):
        """
        绘制预测曲线
        
        参数:
            actual_data: 实际数据
            predicted_data: 预测数据
            confidence_intervals: 置信区间，格式为(lower_bound, upper_bound)
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            save_path: 保存路径
            
        返回:
            matplotlib图形对象
        """
        try:
            # 创建图形
            fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
            
            # 绘制实际数据
            ax.plot(actual_data.index, actual_data, label='实际值', color=self.colors['actual'], linewidth=2)
            
            # 绘制预测数据
            ax.plot(predicted_data.index, predicted_data, label='预测值', color=self.colors['predicted'], linewidth=2, linestyle='--')
            
            # 绘制置信区间
            if confidence_intervals is not None:
                lower_bound, upper_bound = confidence_intervals
                ax.fill_between(
                    predicted_data.index,
                    lower_bound,
                    upper_bound,
                    color=self.colors['predicted'],
                    alpha=0.2,
                    label='95%置信区间'
                )
            
            # 设置图表标题和标签
            ax.set_title(title or '时间序列预测', fontsize=16)
            ax.set_xlabel(xlabel or '日期', fontsize=12)
            ax.set_ylabel(ylabel or '值', fontsize=12)
            
            # 设置日期格式
            date_format = DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_formatter(date_format)
            fig.autofmt_xdate()  # 自动格式化x轴日期标签
            
            # 添加图例
            ax.legend(loc='best', fontsize=12)
            
            # 添加网格线
            ax.grid(True, linestyle='--', alpha=0.7, color=self.colors['grid'])
            
            # 保存图形
            if save_path:
                plt.savefig(save_path, bbox_inches='tight')
                logger.info(f"图形已保存到 {save_path}")
            
            return fig, ax
        
        except Exception as e:
            logger.error(f"绘制预测曲线失败: {e}")
            raise
    
    def plot_comparison(self, models_predictions, actual_data, title=None, xlabel=None, ylabel=None, save_path=None):
        """
        绘制多模型预测比较
        
        参数:
            models_predictions: 字典，键为模型名称，值为预测结果
            actual_data: 实际数据
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            save_path: 保存路径
            
        返回:
            matplotlib图形对象
        """
        try:
            # 创建图形
            fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
            
            # 绘制实际数据
            ax.plot(actual_data.index, actual_data, label='实际值', color=self.colors['actual'], linewidth=2)
            
            # 绘制各模型预测结果
            colors = plt.cm.tab10.colors
            for i, (model_name, predictions) in enumerate(models_predictions.items()):
                ax.plot(
                    predictions.index,
                    predictions,
                    label=f'{model_name}预测值',
                    color=colors[i % len(colors)],
                    linewidth=1.5,
                    linestyle='--'
                )
            
            # 设置图表标题和标签
            ax.set_title(title or '多模型预测比较', fontsize=16)
            ax.set_xlabel(xlabel or '日期', fontsize=12)
            ax.set_ylabel(ylabel or '值', fontsize=12)
            
            # 设置日期格式
            date_format = DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_formatter(date_format)
            fig.autofmt_xdate()  # 自动格式化x轴日期标签
            
            # 添加图例
            ax.legend(loc='best', fontsize=12)
            
            # 添加网格线
            ax.grid(True, linestyle='--', alpha=0.7, color=self.colors['grid'])
            
            # 保存图形
            if save_path:
                plt.savefig(save_path, bbox_inches='tight')
                logger.info(f"图形已保存到 {save_path}")
            
            return fig, ax
        
        except Exception as e:
            logger.error(f"绘制多模型预测比较失败: {e}")
            raise
    
    def plot_error_analysis(self, actual_data, predicted_data, title=None, save_path=None):
        """
        绘制误差分析图
        
        参数:
            actual_data: 实际数据
            predicted_data: 预测数据
            title: 图表标题
            save_path: 保存路径
            
        返回:
            matplotlib图形对象
        """
        try:
            # 计算误差
            error = actual_data - predicted_data
            
            # 创建图形
            fig, axes = plt.subplots(2, 2, figsize=self.figsize, dpi=self.dpi)
            
            # 绘制误差时间序列
            axes[0, 0].plot(error.index, error, color='red')
            axes[0, 0].set_title('误差时间序列', fontsize=14)
            axes[0, 0].set_xlabel('日期', fontsize=12)
            axes[0, 0].set_ylabel('误差', fontsize=12)
            axes[0, 0].grid(True, linestyle='--', alpha=0.7, color=self.colors['grid'])
            
            # 设置日期格式
            date_format = DateFormatter('%Y-%m-%d')
            axes[0, 0].xaxis.set_major_formatter(date_format)
            fig.autofmt_xdate()  # 自动格式化x轴日期标签
            
            # 绘制误差直方图
            axes[0, 1].hist(error, bins=20, color='blue', alpha=0.7)
            axes[0, 1].set_title('误差分布', fontsize=14)
            axes[0, 1].set_xlabel('误差', fontsize=12)
            axes[0, 1].set_ylabel('频率', fontsize=12)
            axes[0, 1].grid(True, linestyle='--', alpha=0.7, color=self.colors['grid'])
            
            # 绘制QQ图
            from scipy import stats
            stats.probplot(error, dist="norm", plot=axes[1, 0])
            axes[1, 0].set_title('QQ图', fontsize=14)
            axes[1, 0].grid(True, linestyle='--', alpha=0.7, color=self.colors['grid'])
            
            # 绘制实际值与预测值散点图
            axes[1, 1].scatter(actual_data, predicted_data, alpha=0.5)
            axes[1, 1].plot([actual_data.min(), actual_data.max()], [actual_data.min(), actual_data.max()], 'r--')
            axes[1, 1].set_title('实际值 vs 预测值', fontsize=14)
            axes[1, 1].set_xlabel('实际值', fontsize=12)
            axes[1, 1].set_ylabel('预测值', fontsize=12)
            axes[1, 1].grid(True, linestyle='--', alpha=0.7, color=self.colors['grid'])
            
            # 调整布局
            plt.tight_layout()
            
            # 设置总标题
            if title:
                fig.suptitle(title, fontsize=16, y=1.05)
            
            # 保存图形
            if save_path:
                plt.savefig(save_path, bbox_inches='tight')
                logger.info(f"图形已保存到 {save_path}")
            
            return fig, axes
        
        except Exception as e:
            logger.error(f"绘制误差分析图失败: {e}")
            raise
    
    def plot_feature_importance(self, feature_names, importances, title=None, save_path=None):
        """
        绘制特征重要性图
        
        参数:
            feature_names: 特征名称列表
            importances: 特征重要性列表
            title: 图表标题
            save_path: 保存路径
            
        返回:
            matplotlib图形对象
        """
        try:
            # 创建DataFrame
            feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            })
            
            # 按重要性排序
            feature_importance = feature_importance.sort_values('importance', ascending=False)
            
            # 创建图形
            fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
            
            # 绘制条形图
            sns.barplot(x='importance', y='feature', data=feature_importance, ax=ax)
            
            # 设置图表标题和标签
            ax.set_title(title or '特征重要性', fontsize=16)
            ax.set_xlabel('重要性', fontsize=12)
            ax.set_ylabel('特征', fontsize=12)
            
            # 添加网格线
            ax.grid(True, linestyle='--', alpha=0.7, color=self.colors['grid'])
            
            # 保存图形
            if save_path:
                plt.savefig(save_path, bbox_inches='tight')
                logger.info(f"图形已保存到 {save_path}")
            
            return fig, ax
        
        except Exception as e:
            logger.error(f"绘制特征重要性图失败: {e}")
            raise