#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
曲线预测数据处理模块
提供数据预处理、特征工程等功能
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import tempfile
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('curve_data_processor')

class DataProcessor:
    """数据处理类"""
    
    def __init__(self):
        """初始化数据处理器"""
        self.scaler = MinMaxScaler(feature_range=(0, 1))
    
    def parse_input_data(self, data, date_column='date', value_column='value'):
        """
        解析输入数据
        
        参数:
            data: 输入数据，可以是JSON数组或CSV字符串
            date_column: 日期列名
            value_column: 值列名
            
        返回:
            解析后的DataFrame
        """
        try:
            # 将数据转换为DataFrame
            if isinstance(data, list):
                # JSON数组
                df = pd.DataFrame(data)
            elif isinstance(data, str):
                # CSV字符串
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                    f.write(data)
                    temp_file = f.name
                
                df = pd.read_csv(temp_file)
                os.unlink(temp_file)
            else:
                raise ValueError('不支持的数据格式')
            
            # 确保日期列存在
            if date_column not in df.columns:
                raise ValueError(f'日期列 {date_column} 不存在')
            
            # 确保值列存在
            if value_column not in df.columns:
                raise ValueError(f'值列 {value_column} 不存在')
            
            # 将日期列转换为日期类型
            df[date_column] = pd.to_datetime(df[date_column])
            
            # 设置日期列为索引
            df = df.set_index(date_column)
            
            return df
        
        except Exception as e:
            logger.error(f"解析输入数据失败: {e}")
            raise
    
    def preprocess_data(self, data, fill_method='ffill', outlier_threshold=3):
        """
        预处理数据
        
        参数:
            data: 输入数据，可以是Series或DataFrame
            fill_method: 填充缺失值的方法，可选值为'ffill', 'bfill', 'interpolate'
            outlier_threshold: 异常值检测的阈值，单位为标准差
            
        返回:
            预处理后的数据
        """
        try:
            # 复制数据
            processed_data = data.copy()
            
            # 处理缺失值
            if fill_method == 'ffill':
                processed_data = processed_data.fillna(method='ffill')
            elif fill_method == 'bfill':
                processed_data = processed_data.fillna(method='bfill')
            elif fill_method == 'interpolate':
                processed_data = processed_data.interpolate()
            
            # 处理异常值
            if outlier_threshold > 0:
                # 计算均值和标准差
                mean = processed_data.mean()
                std = processed_data.std()
                
                # 检测异常值
                lower_bound = mean - outlier_threshold * std
                upper_bound = mean + outlier_threshold * std
                
                # 替换异常值为边界值
                processed_data = processed_data.clip(lower=lower_bound, upper=upper_bound)
            
            return processed_data
        
        except Exception as e:
            logger.error(f"预处理数据失败: {e}")
            raise
    
    def normalize_data(self, data):
        """
        标准化数据
        
        参数:
            data: 输入数据，可以是Series或DataFrame
            
        返回:
            标准化后的数据
        """
        try:
            # 复制数据
            normalized_data = data.copy()
            
            # 标准化数据
            if isinstance(normalized_data, pd.Series):
                normalized_values = self.scaler.fit_transform(normalized_data.values.reshape(-1, 1)).flatten()
                normalized_data = pd.Series(normalized_values, index=normalized_data.index)
            else:
                normalized_values = self.scaler.fit_transform(normalized_data)
                normalized_data = pd.DataFrame(normalized_values, index=normalized_data.index, columns=normalized_data.columns)
            
            return normalized_data
        
        except Exception as e:
            logger.error(f"标准化数据失败: {e}")
            raise
    
    def inverse_normalize(self, data):
        """
        反标准化数据
        
        参数:
            data: 输入数据，可以是Series或DataFrame
            
        返回:
            反标准化后的数据
        """
        try:
            # 复制数据
            inverse_data = data.copy()
            
            # 反标准化数据
            if isinstance(inverse_data, pd.Series):
                inverse_values = self.scaler.inverse_transform(inverse_data.values.reshape(-1, 1)).flatten()
                inverse_data = pd.Series(inverse_values, index=inverse_data.index)
            else:
                inverse_values = self.scaler.inverse_transform(inverse_data)
                inverse_data = pd.DataFrame(inverse_values, index=inverse_data.index, columns=inverse_data.columns)
            
            return inverse_data
        
        except Exception as e:
            logger.error(f"反标准化数据失败: {e}")
            raise
    
    def create_features(self, data):
        """
        创建特征
        
        参数:
            data: 输入数据，可以是Series或DataFrame
            
        返回:
            特征DataFrame
        """
        try:
            # 复制数据
            df = data.copy()
            
            if isinstance(df, pd.Series):
                df = df.to_frame(name='value')
            
            # 提取日期特征
            df['year'] = df.index.year
            df['month'] = df.index.month
            df['day'] = df.index.day
            df['dayofweek'] = df.index.dayofweek
            df['quarter'] = df.index.quarter
            df['is_month_start'] = df.index.is_month_start.astype(int)
            df['is_month_end'] = df.index.is_month_end.astype(int)
            df['is_quarter_start'] = df.index.is_quarter_start.astype(int)
            df['is_quarter_end'] = df.index.is_quarter_end.astype(int)
            df['is_year_start'] = df.index.is_year_start.astype(int)
            df['is_year_end'] = df.index.is_year_end.astype(int)
            
            # 创建滞后特征
            for lag in range(1, 8):
                df[f'lag_{lag}'] = df['value'].shift(lag)
            
            # 创建滚动统计特征
            for window in [7, 14, 30]:
                df[f'rolling_mean_{window}'] = df['value'].rolling(window=window).mean()
                df[f'rolling_std_{window}'] = df['value'].rolling(window=window).std()
                df[f'rolling_min_{window}'] = df['value'].rolling(window=window).min()
                df[f'rolling_max_{window}'] = df['value'].rolling(window=window).max()
            
            # 创建差分特征
            df['diff_1'] = df['value'].diff()
            df['diff_7'] = df['value'].diff(7)
            
            # 删除缺失值
            df = df.dropna()
            
            return df
        
        except Exception as e:
            logger.error(f"创建特征失败: {e}")
            raise
    
    def split_data(self, data, test_size=0.2):
        """
        划分训练集和测试集
        
        参数:
            data: 输入数据，可以是Series或DataFrame
            test_size: 测试集比例
            
        返回:
            (训练集, 测试集)
        """
        try:
            # 计算划分点
            split_idx = int(len(data) * (1 - test_size))
            
            # 划分数据
            train_data = data.iloc[:split_idx]
            test_data = data.iloc[split_idx:]
            
            return train_data, test_data
        
        except Exception as e:
            logger.error(f"划分数据失败: {e}")
            raise
    
    def check_stationarity(self, data):
        """
        检查时间序列的平稳性
        
        参数:
            data: 输入数据，可以是Series
            
        返回:
            (是否平稳, ADF检验结果)
        """
        try:
            # 执行ADF检验
            result = adfuller(data.dropna())
            
            # 解析结果
            adf_stat = result[0]
            p_value = result[1]
            critical_values = result[4]
            
            # 判断是否平稳
            is_stationary = p_value < 0.05
            
            # 返回结果
            return is_stationary, {
                'adf_stat': adf_stat,
                'p_value': p_value,
                'critical_values': critical_values,
                'is_stationary': is_stationary
            }
        
        except Exception as e:
            logger.error(f"检查平稳性失败: {e}")
            raise
    
    def make_stationary(self, data, method='diff'):
        """
        将时间序列转换为平稳序列
        
        参数:
            data: 输入数据，可以是Series
            method: 转换方法，可选值为'diff', 'log', 'sqrt'
            
        返回:
            平稳序列
        """
        try:
            # 复制数据
            stationary_data = data.copy()
            
            # 转换数据
            if method == 'diff':
                stationary_data = stationary_data.diff().dropna()
            elif method == 'log':
                stationary_data = np.log(stationary_data)
            elif method == 'sqrt':
                stationary_data = np.sqrt(stationary_data)
            
            return stationary_data
        
        except Exception as e:
            logger.error(f"转换为平稳序列失败: {e}")
            raise
    
    def decompose_time_series(self, data, period=None):
        """
        分解时间序列
        
        参数:
            data: 输入数据，可以是Series
            period: 周期，如果为None则自动检测
            
        返回:
            分解结果
        """
        try:
            # 如果未指定周期，则自动检测
            if period is None:
                # 计算自相关函数
                acf_values = acf(data.dropna(), nlags=len(data) // 2)
                
                # 查找第一个峰值
                for i in range(1, len(acf_values)):
                    if acf_values[i] > acf_values[i-1] and acf_values[i] > acf_values[i+1]:
                        period = i
                        break
                
                # 如果未找到峰值，则使用默认周期
                if period is None:
                    period = 7  # 默认为周周期
            
            # 分解时间序列
            result = seasonal_decompose(data, period=period)
            
            return result
        
        except Exception as e:
            logger.error(f"分解时间序列失败: {e}")
            raise