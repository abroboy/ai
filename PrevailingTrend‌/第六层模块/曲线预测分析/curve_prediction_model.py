#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
曲线预测分析模型
提供多种预测模型实现，包括ARIMA、LSTM、Prophet等
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import logging
import joblib
import os
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('curve_prediction_model')

class ARIMAModel:
    """ARIMA模型实现"""
    
    def __init__(self, order=(5, 1, 0), seasonal_order=None):
        """
        初始化ARIMA模型
        
        参数:
            order: ARIMA模型阶数 (p, d, q)
            seasonal_order: 季节性ARIMA模型阶数 (P, D, Q, s)
        """
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None
        self.is_seasonal = seasonal_order is not None
    
    def fit(self, data):
        """
        训练模型
        
        参数:
            data: 时间序列数据
            
        返回:
            训练好的模型
        """
        try:
            if self.is_seasonal:
                # 使用SARIMAX模型
                self.model = SARIMAX(
                    data,
                    order=self.order,
                    seasonal_order=self.seasonal_order,
                    enforce_stationarity=False,
                    enforce_invertibility=False
                )
            else:
                # 使用ARIMA模型
                self.model = ARIMA(data, order=self.order)
            
            # 训练模型
            self.result = self.model.fit()
            logger.info("ARIMA模型训练完成")
            
            return self.result
        
        except Exception as e:
            logger.error(f"ARIMA模型训练失败: {e}")
            raise
    
    def predict(self, steps=30, return_conf_int=True, alpha=0.05):
        """
        预测未来值
        
        参数:
            steps: 预测步数
            return_conf_int: 是否返回置信区间
            alpha: 置信区间的显著性水平
            
        返回:
            预测结果，如果return_conf_int为True，则返回(预测值, 置信区间)
        """
        if self.result is None:
            raise ValueError("模型尚未训练")
        
        try:
            # 预测未来值
            if return_conf_int:
                forecast = self.result.get_forecast(steps=steps)
                mean_forecast = forecast.predicted_mean
                conf_int = forecast.conf_int(alpha=alpha)
                
                return mean_forecast, conf_int
            else:
                forecast = self.result.get_forecast(steps=steps)
                mean_forecast = forecast.predicted_mean
                
                return mean_forecast
        
        except Exception as e:
            logger.error(f"ARIMA预测失败: {e}")
            raise
    
    def save(self, path):
        """
        保存模型
        
        参数:
            path: 模型保存路径
        """
        if self.result is None:
            raise ValueError("模型尚未训练")
        
        try:
            # 保存模型
            self.result.save(path)
            
            # 保存模型参数
            params = {
                'order': self.order,
                'seasonal_order': self.seasonal_order,
                'is_seasonal': self.is_seasonal
            }
            
            joblib.dump(params, f"{path}_params.pkl")
            logger.info(f"ARIMA模型已保存到 {path}")
        
        except Exception as e:
            logger.error(f"保存ARIMA模型失败: {e}")
            raise
    
    @classmethod
    def load(cls, path):
        """
        加载模型
        
        参数:
            path: 模型加载路径
            
        返回:
            加载的模型
        """
        try:
            # 加载模型参数
            params = joblib.load(f"{path}_params.pkl")
            
            # 创建模型实例
            model = cls(
                order=params['order'],
                seasonal_order=params['seasonal_order']
            )
            
            # 加载模型
            if params['is_seasonal']:
                model.model = SARIMAX(
                    endog=[0],  # 临时数据，将被替换
                    order=params['order'],
                    seasonal_order=params['seasonal_order'],
                    enforce_stationarity=False,
                    enforce_invertibility=False
                )
            else:
                model.model = ARIMA(
                    endog=[0],  # 临时数据，将被替换
                    order=params['order']
                )
            
            model.result = model.model.load(path)
            logger.info(f"ARIMA模型已从 {path} 加载")
            
            return model
        
        except Exception as e:
            logger.error(f"加载ARIMA模型失败: {e}")
            raise


class LSTMModel:
    """LSTM模型实现"""
    
    def __init__(self, seq_length=60, units=50, dropout=0.2, epochs=100, batch_size=32):
        """
        初始化LSTM模型
        
        参数:
            seq_length: 序列长度
            units: LSTM单元数
            dropout: Dropout比例
            epochs: 训练轮数
            batch_size: 批次大小
        """
        self.seq_length = seq_length
        self.units = units
        self.dropout = dropout
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
    
    def _create_sequences(self, data):
        """
        创建序列数据
        
        参数:
            data: 时间序列数据
            
        返回:
            X序列和y标签
        """
        X, y = [], []
        for i in range(len(data) - self.seq_length):
            X.append(data[i:i + self.seq_length])
            y.append(data[i + self.seq_length])
        
        return np.array(X), np.array(y)
    
    def fit(self, data):
        """
        训练模型
        
        参数:
            data: 时间序列数据
            
        返回:
            训练历史
        """
        try:
            # 标准化数据
            data_scaled = self.scaler.fit_transform(data.values.reshape(-1, 1)).flatten()
            
            # 创建序列数据
            X, y = self._create_sequences(data_scaled)
            X = X.reshape(X.shape[0], X.shape[1], 1)
            
            # 创建模型
            self.model = Sequential()
            self.model.add(LSTM(units=self.units, return_sequences=True, input_shape=(self.seq_length, 1)))
            self.model.add(Dropout(self.dropout))
            self.model.add(LSTM(units=self.units))
            self.model.add(Dropout(self.dropout))
            self.model.add(Dense(1))
            
            # 编译模型
            self.model.compile(optimizer='adam', loss='mean_squared_error')
            
            # 训练模型
            history = self.model.fit(
                X, y,
                epochs=self.epochs,
                batch_size=self.batch_size,
                verbose=1
            )
            
            logger.info("LSTM模型训练完成")
            return history
        
        except Exception as e:
            logger.error(f"LSTM模型训练失败: {e}")
            raise
    
    def predict(self, data, steps=30):
        """
        预测未来值
        
        参数:
            data: 时间序列数据
            steps: 预测步数
            
        返回:
            预测结果
        """
        if self.model is None:
            raise ValueError("模型尚未训练")
        
        try:
            # 标准化数据
            data_scaled = self.scaler.transform(data.values.reshape(-1, 1)).flatten()
            
            # 预测未来值
            predictions = []
            current_batch = data_scaled[-self.seq_length:].reshape(1, self.seq_length, 1)
            
            for i in range(steps):
                # 预测下一个值
                current_pred = self.model.predict(current_batch)[0][0]
                predictions.append(current_pred)
                
                # 更新当前批次
                current_batch = np.append(current_batch[:, 1:, :], [[current_pred]], axis=1)
            
            # 反标准化
            predictions = np.array(predictions).reshape(-1, 1)
            predictions = self.scaler.inverse_transform(predictions).flatten()
            
            # 创建日期索引
            last_date = data.index[-1]
            date_range = pd.date_range(start=last_date + timedelta(days=1), periods=steps)
            
            # 创建预测结果DataFrame
            predictions_df = pd.Series(predictions, index=date_range)
            
            return predictions_df
        
        except Exception as e:
            logger.error(f"LSTM预测失败: {e}")
            raise
    
    def save(self, path):
        """
        保存模型
        
        参数:
            path: 模型保存路径
        """
        if self.model is None:
            raise ValueError("模型尚未训练")
        
        try:
            # 保存模型
            self.model.save(f"{path}.h5")
            
            # 保存scaler
            joblib.dump(self.scaler, f"{path}_scaler.pkl")
            
            # 保存模型参数
            params = {
                'seq_length': self.seq_length,
                'units': self.units,
                'dropout': self.dropout,
                'epochs': self.epochs,
                'batch_size': self.batch_size
            }
            
            joblib.dump(params, f"{path}_params.pkl")
            logger.info(f"LSTM模型已保存到 {path}")
        
        except Exception as e:
            logger.error(f"保存LSTM模型失败: {e}")
            raise
    
    @classmethod
    def load(cls, path):
        """
        加载模型
        
        参数:
            path: 模型加载路径
            
        返回:
            加载的模型
        """
        try:
            # 加载模型参数
            params = joblib.load(f"{path}_params.pkl")
            
            # 创建模型实例
            model = cls(
                seq_length=params['seq_length'],
                units=params['units'],
                dropout=params['dropout'],
                epochs=params['epochs'],
                batch_size=params['batch_size']
            )
            
            # 加载模型
            model.model = tf.keras.models.load_model(f"{path}.h5")
            
            # 加载scaler
            model.scaler = joblib.load(f"{path}_scaler.pkl")
            
            logger.info(f"LSTM模型已从 {path} 加载")
            
            return model
        
        except Exception as e:
            logger.error(f"加载LSTM模型失败: {e}")
            raise


class EnsembleModel:
    """集成模型实现"""
    
    def __init__(self, models=None, weights=None):
        """
        初始化集成模型
        
        参数:
            models: 模型列表
            weights: 模型权重列表
        """
        self.models = models or []
        self.weights = weights or []
        
        # 如果提供了模型但没有提供权重，则使用均匀权重
        if self.models and not self.weights:
            self.weights = [1.0 / len(self.models)] * len(self.models)
    
    def add_model(self, model, weight=None):
        """
        添加模型
        
        参数:
            model: 模型
            weight: 模型权重
        """
        self.models.append(model)
        
        if weight is None:
            # 重新计算均匀权重
            self.weights = [1.0 / len(self.models)] * len(self.models)
        else:
            # 添加新权重并归一化
            self.weights.append(weight)
            total_weight = sum(self.weights)
            self.weights = [w / total_weight for w in self.weights]
    
    def fit(self, data):
        """
        训练所有模型
        
        参数:
            data: 时间序列数据
            
        返回:
            训练结果列表
        """
        results = []
        
        for i, model in enumerate(self.models):
            try:
                logger.info(f"训练模型 {i+1}/{len(self.models)}")
                result = model.fit(data)
                results.append(result)
            except Exception as e:
                logger.error(f"模型 {i+1} 训练失败: {e}")
                results.append(None)
        
        return results
    
    def predict(self, data=None, steps=30):
        """
        预测未来值
        
        参数:
            data: 时间序列数据（对于某些模型可能需要）
            steps: 预测步数
            
        返回:
            加权平均预测结果
        """
        if not self.models:
            raise ValueError("没有可用的模型")
        
        predictions = []
        valid_weights = []
        
        for i, (model, weight) in enumerate(zip(self.models, self.weights)):
            try:
                logger.info(f"使用模型 {i+1}/{len(self.models)} 进行预测")
                
                if isinstance(model, LSTMModel):
                    # LSTM模型需要数据
                    if data is None:
                        logger.warning(f"模型 {i+1} 需要数据进行预测，但未提供数据")
                        continue
                    
                    pred = model.predict(data, steps=steps)
                else:
                    # 其他模型直接预测
                    pred = model.predict(steps=steps)
                    
                    # 如果返回的是元组（预测值和置信区间），只取预测值
                    if isinstance(pred, tuple):
                        pred = pred[0]
                
                predictions.append(pred)
                valid_weights.append(weight)
            
            except Exception as e:
                logger.error(f"模型 {i+1} 预测失败: {e}")
        
        if not predictions:
            raise ValueError("所有模型预测均失败")
        
        # 归一化有效权重
        total_weight = sum(valid_weights)
        valid_weights = [w / total_weight for w in valid_weights]
        
        # 计算加权平均预测结果
        weighted_predictions = None
        
        for pred, weight in zip(predictions, valid_weights):
            if weighted_predictions is None:
                weighted_predictions = pred * weight
            else:
                # 确保索引一致
                weighted_predictions = weighted_predictions.add(pred * weight, fill_value=0)
        
        return weighted_predictions
    
    def save(self, path):
        """
        保存所有模型
        
        参数:
            path: 模型保存目录
        """
        if not os.path.exists(path):
            os.makedirs(path)
        
        # 保存模型权重
        joblib.dump(self.weights, os.path.join(path, "ensemble_weights.pkl"))
        
        # 保存每个模型
        for i, model in enumerate(self.models):
            model_path = os.path.join(path, f"model_{i}")
            
            try:
                if isinstance(model, ARIMAModel):
                    model.save(model_path)
                elif isinstance(model, LSTMModel):
                    model.save(model_path)
                else:
                    joblib.dump(model, f"{model_path}.pkl")
            
            except Exception as e:
                logger.error(f"保存模型 {i+1} 失败: {e}")
        
        # 保存模型类型信息
        model_types = [type(model).__name__ for model in self.models]
        joblib.dump(model_types, os.path.join(path, "model_types.pkl"))
        
        logger.info(f"集成模型已保存到 {path}")
    
    @classmethod
    def load(cls, path):
        """
        加载集成模型
        
        参数:
            path: 模型加载目录
            
        返回:
            加载的集成模型
        """
        try:
            # 加载模型权重
            weights = joblib.load(os.path.join(path, "ensemble_weights.pkl"))
            
            # 加载模型类型信息
            model_types = joblib.load(os.path.join(path, "model_types.pkl"))
            
            # 创建集成模型实例
            ensemble = cls(weights=weights)
            
            # 加载每个模型
            for i, model_type in enumerate(model_types):
                model_path = os.path.join(path, f"model_{i}")
                
                try:
                    if model_type == "ARIMAModel":
                        model = ARIMAModel.load(model_path)
                    elif model_type == "LSTMModel":
                        model = LSTMModel.load(model_path)
                    else:
                        model = joblib.load(f"{model_path}.pkl")
                    
                    ensemble.models.append(model)
                
                except Exception as e:
                    logger.error(f"加载模型 {i+1} 失败: {e}")
            
            logger.info(f"集成模型已从 {path} 加载")
            
            return ensemble
        
        except Exception as e:
            logger.error(f"加载集成模型失败: {e}")
            raise


def evaluate_model(model, test_data, train_data=None):
    """
    评估模型性能
    
    参数:
        model: 预测模型
        test_data: 测试数据
        train_data: 训练数据（对于某些模型可能需要）
        
    返回:
        评估指标字典
    """
    try:
        # 获取预测结果
        if isinstance(model, LSTMModel) and train_data is not None:
            predictions = model.predict(train_data, steps=len(test_data))
        else:
            predictions = model.predict(steps=len(test_data))
            
            # 如果返回的是元组（预测值和置信区间），只取预测值
            if isinstance(predictions, tuple):
                predictions = predictions[0]
        
        # 计算评估指标
        mse = mean_squared_error(test_data, predictions)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(test_data, predictions)
        
        # 计算MAPE（平均绝对百分比误差）
        mape = np.mean(np.abs((test_data - predictions) / test_data)) * 100
        
        # 计算R²
        r2 = r2_score(test_data, predictions)
        
        return {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'mape': mape,
            'r2': r2,
            'predictions': predictions
        }
    
    except Exception as e:
        logger.error(f"评估模型失败: {e}")
        raise