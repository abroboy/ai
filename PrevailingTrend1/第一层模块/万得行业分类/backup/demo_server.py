"""
万得行业分类模块演示服务器
"""

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    """首页"""
    return jsonify({
        "message": "万得行业分类模块API服务",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/industries')
def get_industries():
    """获取行业列表"""
    industries = [
        {
            "industry_code": "801010",
            "industry_name": "农林牧渔",
            "industry_level": 1,
            "status": "active"
        },
        {
            "industry_code": "801020", 
            "industry_name": "采掘",
            "industry_level": 1,
            "status": "active"
        },
        {
            "industry_code": "801030",
            "industry_name": "化工",
            "industry_level": 1,
            "status": "active"
        }
    ]
    
    return jsonify({
        "success": True,
        "data": industries,
        "count": len(industries)
    })

@app.route('/api/stocks/<industry_code>')
def get_stocks_by_industry(industry_code):
    """根据行业代码获取股票列表"""
    stocks = [
        {
            "stock_code": "000001",
            "stock_name": "平安银行",
            "industry_code": industry_code,
            "industry_name": "农林牧渔",
            "confidence": 0.95
        },
        {
            "stock_code": "000002",
            "stock_name": "万科A",
            "industry_code": industry_code,
            "industry_name": "农林牧渔", 
            "confidence": 0.92
        }
    ]
    
    return jsonify({
        "success": True,
        "data": stocks,
        "count": len(stocks)
    })

if __name__ == '__main__':
    print("启动万得行业分类模块演示服务器...")
    print("访问地址: http://localhost:5000")
    print("API文档:")
    print("  GET / - 首页")
    print("  GET /health - 健康检查")
    print("  GET /api/industries - 获取行业列表")
    print("  GET /api/stocks/<industry_code> - 获取行业股票")
    print("按 Ctrl+C 停止服务")
    
    app.run(host='0.0.0.0', port=5000, debug=True) 