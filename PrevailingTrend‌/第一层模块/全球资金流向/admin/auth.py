# -*- coding: utf-8 -*-
"""
管理台认证模块
"""

import os
import hashlib
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, session

class AdminAuth:
    """管理台认证类"""
    
    def __init__(self, secret_key=None):
        """初始化认证模块"""
        self.secret_key = secret_key or os.getenv('SECRET_KEY', 'your-secret-key-here')
        self.admin_users = {
            'admin': {
                'username': 'admin',
                'password_hash': self._hash_password('admin123'),
                'role': 'super_admin',
                'permissions': ['read', 'write', 'delete', 'admin']
            },
            'manager': {
                'username': 'manager',
                'password_hash': self._hash_password('manager123'),
                'role': 'manager',
                'permissions': ['read', 'write']
            },
            'viewer': {
                'username': 'viewer',
                'password_hash': self._hash_password('viewer123'),
                'role': 'viewer',
                'permissions': ['read']
            }
        }
    
    def _hash_password(self, password):
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, username, password):
        """验证密码"""
        if username in self.admin_users:
            user = self.admin_users[username]
            return user['password_hash'] == self._hash_password(password)
        return False
    
    def generate_token(self, username):
        """生成JWT令牌"""
        if username in self.admin_users:
            user = self.admin_users[username]
            payload = {
                'username': username,
                'role': user['role'],
                'permissions': user['permissions'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            return jwt.encode(payload, self.secret_key, algorithm='HS256')
        return None
    
    def verify_token(self, token):
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def require_auth(self, f):
        """认证装饰器"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'error': '未提供认证令牌'}), 401
            
            token = token.replace('Bearer ', '')
            payload = self.verify_token(token)
            if not payload:
                return jsonify({'error': '无效的认证令牌'}), 401
            
            request.user = payload
            return f(*args, **kwargs)
        return decorated_function
    
    def require_permission(self, permission):
        """权限装饰器"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not hasattr(request, 'user'):
                    return jsonify({'error': '未认证'}), 401
                
                if permission not in request.user.get('permissions', []):
                    return jsonify({'error': '权限不足'}), 403
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator

# 创建全局认证实例
admin_auth = AdminAuth() 