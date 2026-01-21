"""
健康检查路由
"""
from flask import Blueprint, jsonify
import time

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'service': 'pcb-impedance-calculator-backend'
    }), 200

@health_bp.route('/api/health', methods=['GET'])
def api_health_check():
    """API健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'service': 'pcb-impedance-calculator-api'
    }), 200