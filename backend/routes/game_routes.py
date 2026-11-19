
"""
🎮 Rotas de controle da partida — Escape Room de Natal
"""
from flask import Blueprint, jsonify
from services.game_service import GameService
from services.timer_service import TimerService
from config.settings import GameConfig

game_bp = Blueprint('game', __name__)


@game_bp.route('/start', methods=['POST'])
def start_game():
    """
    POST /api/game/start
    Inicia (ou reinicia) uma partida.

    Response:
        - success: bool
        - message: str
        - time_remaining: int (segundos)
        - current_phase: int
        - total_phases: int
    """
    result = GameService.start_new_game()
    return jsonify(result), 200


@game_bp.route('/status', methods=['GET'])
def game_status():
    """
    GET /api/game/status
    Retorna o estado atual completo da partida.

    Response:
        - started, current_phase, completed_phases
        - time_remaining, time_formatted, time_status
        - hints_used, total_hints, found_objects
        - game_over, victory
    """
    return jsonify(GameService.get_status()), 200


@game_bp.route('/reset', methods=['POST'])
def reset_game():
    """
    POST /api/game/reset
    Limpa a sessão e volta ao estado inicial.

    Response:
        - success: bool
        - message: str
    """
    result = GameService.reset_game()
    return jsonify(result), 200


@game_bp.route('/info', methods=['GET'])
def game_info():
    """
    GET /api/game/info
    Retorna as regras do jogo (não depende de sessão).

    Response:
        - título, duração, penalidade e número de fases
    """
    return jsonify({
        'title': 'Escape Room de Natal 🎄',
        'subtitle': 'A Oficina do Papai Noel',
        'duration_seconds': GameConfig.GAME_DURATION,
        'duration_formatted': TimerService.format_time(GameConfig.GAME_DURATION),
        'total_phases': GameConfig.TOTAL_PHASES,
        'max_hints_per_phase': GameConfig.MAX_HINTS_PER_PHASE,
        'hint_penalty_seconds': GameConfig.HINT_PENALTY,
        'hint_penalty_text': TimerService.get_penalty_formatted()
    }), 200
