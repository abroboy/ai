"""
最简单的Flask测试应用
"""

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return "国内热点数据管理台 - 测试页面"

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': '服务运行正常'
    })

@app.route('/api/test')
def test():
    return jsonify({
        'success': True,
        'data': {
            'message': '测试成功',
            'count': 100
        }
    })

if __name__ == '__main__':
    print("启动测试Flask应用...")
    print("访问地址: http://localhost:5003")
    print("健康检查: http://localhost:5003/api/health")
    print("测试接口: http://localhost:5003/api/test")
    
    app.run(host='0.0.0.0', port=5003, debug=True) 