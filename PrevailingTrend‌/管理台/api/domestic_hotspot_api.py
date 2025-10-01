#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国内热点数据API接口
大势所趋风险框架管理台
"""

import json
import logging
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from services.domestic_hotspot_fetcher import DomesticHotspotFetcher

# 创建蓝图
domestic_hotspot_bp = Blueprint('domestic_hotspot', __name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建热点数据获取器实例
hotspot_fetcher = DomesticHotspotFetcher()

@domestic_hotspot_bp.route('/api/domestic-hotspot', methods=['GET'])
def get_domestic_hotspots():
    """
    获取国内热点数据
    
    查询参数:
    - limit: 返回数据条数限制 (默认: 50)
    - category: 分类筛选
    - sentiment: 情感筛选
    - source: 数据源筛选
    - start_date: 开始日期 (YYYY-MM-DD)
    - end_date: 结束日期 (YYYY-MM-DD)
    """
    try:
        # 获取查询参数
        limit = request.args.get('limit', 50, type=int)
        category = request.args.get('category')
        sentiment = request.args.get('sentiment')
        source = request.args.get('source')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 构建筛选条件
        filters = {}
        if category:
            filters['category'] = category
        if sentiment:
            filters['sentiment'] = sentiment
        if source:
            filters['source'] = source
        if start_date:
            filters['start_date'] = start_date
        if end_date:
            filters['end_date'] = end_date
        
        # 获取热点数据
        result = hotspot_fetcher.fetch_hotspots(limit=limit, filters=filters)
        
        if result['success']:
            logger.info(f"成功获取 {len(result['data'])} 条国内热点数据")
            return jsonify(result)
        else:
            logger.error(f"获取热点数据失败: {result.get('error', '未知错误')}")
            return jsonify({
                'success': False,
                'error': result.get('error', '获取数据失败'),
                'data': [],
                'statistics': {}
            }), 500
            
    except Exception as e:
        logger.error(f"API调用异常: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器内部错误: {str(e)}',
            'data': [],
            'statistics': {}
        }), 500

@domestic_hotspot_bp.route('/api/domestic-hotspot/statistics', methods=['GET'])
def get_hotspot_statistics():
    """
    获取热点数据统计信息
    """
    try:
        # 获取统计数据
        stats = hotspot_fetcher.get_statistics()
        
        if stats['success']:
            return jsonify(stats)
        else:
            return jsonify({
                'success': False,
                'error': stats.get('error', '获取统计数据失败'),
                'statistics': {}
            }), 500
            
    except Exception as e:
        logger.error(f"获取统计数据异常: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器内部错误: {str(e)}',
            'statistics': {}
        }), 500

@domestic_hotspot_bp.route('/api/domestic-hotspot/refresh', methods=['POST'])
def refresh_hotspot_data():
    """
    刷新热点数据
    """
    try:
        # 强制刷新数据
        result = hotspot_fetcher.refresh_data()
        
        if result['success']:
            logger.info("热点数据刷新成功")
            return jsonify({
                'success': True,
                'message': '数据刷新成功',
                'updated_count': result.get('updated_count', 0),
                'last_update': result.get('last_update')
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', '数据刷新失败')
            }), 500
            
    except Exception as e:
        logger.error(f"刷新数据异常: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器内部错误: {str(e)}'
        }), 500

@domestic_hotspot_bp.route('/api/domestic-hotspot/categories', methods=['GET'])
def get_hotspot_categories():
    """
    获取热点分类列表
    """
    try:
        categories = hotspot_fetcher.get_categories()
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        logger.error(f"获取分类列表异常: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器内部错误: {str(e)}',
            'categories': []
        }), 500

@domestic_hotspot_bp.route('/api/domestic-hotspot/sources', methods=['GET'])
def get_hotspot_sources():
    """
    获取数据源列表
    """
    try:
        sources = hotspot_fetcher.get_sources()
        return jsonify({
            'success': True,
            'sources': sources
        })
    except Exception as e:
        logger.error(f"获取数据源列表异常: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器内部错误: {str(e)}',
            'sources': []
        }), 500

@domestic_hotspot_bp.route('/api/domestic-hotspot/<hotspot_id>', methods=['GET'])
def get_hotspot_detail(hotspot_id):
    """
    获取单个热点详情
    """
    try:
        detail = hotspot_fetcher.get_hotspot_detail(hotspot_id)
        
        if detail:
            return jsonify({
                'success': True,
                'data': detail
            })
        else:
            return jsonify({
                'success': False,
                'error': '热点不存在'
            }), 404
            
    except Exception as e:
        logger.error(f"获取热点详情异常: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器内部错误: {str(e)}'
        }), 500

@domestic_hotspot_bp.route('/api/domestic-hotspot/export', methods=['GET'])
def export_hotspot_data():
    """
    导出热点数据
    """
    try:
        # 获取导出格式参数
        format_type = request.args.get('format', 'csv').lower()
        
        if format_type not in ['csv', 'json', 'excel']:
            return jsonify({
                'success': False,
                'error': '不支持的导出格式'
            }), 400
        
        # 获取筛选参数
        filters = {
            'category': request.args.get('category'),
            'sentiment': request.args.get('sentiment'),
            'source': request.args.get('source'),
            'start_date': request.args.get('start_date'),
            'end_date': request.args.get('end_date')
        }
        
        # 移除空值
        filters = {k: v for k, v in filters.items() if v}
        
        # 导出数据
        result = hotspot_fetcher.export_data(format_type, filters)
        
        if result['success']:
            return jsonify({
                'success': True,
                'download_url': result['download_url'],
                'filename': result['filename'],
                'file_size': result.get('file_size', 0)
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', '导出失败')
            }), 500
            
    except Exception as e:
        logger.error(f"导出数据异常: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器内部错误: {str(e)}'
        }), 500

# 错误处理
@domestic_hotspot_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': '接口不存在'
    }), 404

@domestic_hotspot_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': '服务器内部错误'
    }), 500