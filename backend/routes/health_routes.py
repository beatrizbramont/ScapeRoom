
"""
🏥 Rota de saúde da API
"""
from flask import Blueprint, jsonify
import time

health_bp = Blueprint('health', __name__)

# Timestamp de quando o servidor iniciou
_start_time = time.time()


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    GET /api/health
    Verifica se o servidor está funcionando.
    
    Response:
        - status: str ("ok")
        - game: str
        - uptime: float (segundos desde o início)
        - version: str
    """
    uptime = round(time.time() - _start_time, 2)

    return jsonify({
        'status': 'ok',
        'game': 'Escape Room de Natal 🎄',
        'version': '1.0.0',
        'uptime_seconds': uptime,
        'endpoints': {
            'game': '/api/game/start | /status | /reset',
            'puzzles': '/api/puzzle/<phase>/info | /solve | /click | /hint',
            'health': '/api/health'
        }
    })

