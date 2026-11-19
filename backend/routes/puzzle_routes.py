
"""
🧩 Rotas dos puzzles — Escape Room de Natal
"""
from flask import Blueprint, jsonify, request
from services.game_service import GameService
from services.hint_service import HintService
from config.settings import GameConfig

puzzle_bp = Blueprint('puzzle', __name__)


def _validate_phase(phase):
    """Garante que a fase existe (1 a 4). Retorna mensagem de erro ou None."""
    if phase < 1 or phase > GameConfig.TOTAL_PHASES:
        return f'Fase inválida! Escolha entre 1 e {GameConfig.TOTAL_PHASES}.'
    return None


@puzzle_bp.route('/<int:phase>/info', methods=['GET'])
def puzzle_info(phase):
    """
    GET /api/puzzle/<phase>/info
    Retorna os dados públicos do puzzle (nunca a resposta!).

    Response:
        - phase, name, total_hints, locked, completed
        - campos específicos da fase (objects, encrypted_message,
          sequence, available_weights...)
    """
    error = _validate_phase(phase)
    if error:
        return jsonify({'error': error}), 400

    info = GameService.get_puzzle_info(phase)
    if info is None:
        return jsonify({'error': 'Puzzle não encontrado'}), 404

    return jsonify(info), 200


@puzzle_bp.route('/<int:phase>/click', methods=['POST'])
def click_object(phase):
    """
    POST /api/puzzle/<phase>/click
    Fase 1: registra o clique do jogador em um objeto da oficina.

    Body:
        - object: str (ex: "relogio")

    Response:
        - success: bool
        - message: str
        - found_objects: list
        - all_found: bool
    """
    error = _validate_phase(phase)
    if error:
        return jsonify({'error': error}), 400

    if phase != 1:
        return jsonify({'error': 'Apenas a Fase 1 aceita cliques em objetos'}), 400

    data = request.get_json(silent=True) or {}
    object_name = data.get('object')

    if not object_name:
        return jsonify({'error': 'Informe o objeto clicado'}), 400

    result, status = GameService.click_object(str(object_name))
    return jsonify(result), status


@puzzle_bp.route('/<int:phase>/solve', methods=['POST'])
def solve_puzzle(phase):
    """
    POST /api/puzzle/<phase>/solve
    Valida a resposta do jogador para a fase atual.

    Body:
        - answer: str | list
          Fase 1: "1225" | Fase 2: "RENA"
          Fase 3: ["vermelho", ...] | Fase 4: [25.0, 35.0, 40.0]

    Response:
        - success: bool
        - message: str
        - next_phase: int (quando avança)
        - victory: bool, time_elapsed, hints_used (ao vencer)
    """
    error = _validate_phase(phase)
    if error:
        return jsonify({'error': error}), 400

    data = request.get_json(silent=True) or {}

    if 'answer' not in data:
        return jsonify({'error': 'Informe uma resposta'}), 400

    result, status = GameService.solve_puzzle(phase, data['answer'])
    return jsonify(result), status


@puzzle_bp.route('/<int:phase>/hint', methods=['POST'])
def request_hint(phase):
    """
    POST /api/puzzle/<phase>/hint
    Pede a próxima dica da fase — cobra penalidade de tempo.

    Response:
        - hint: str
        - penalty: int (segundos), penalty_text: str
        - time_remaining: int
        - hint_number: int, total_available: int, exhausted: bool
    """
    error = _validate_phase(phase)
    if error:
        return jsonify({'error': error}), 400

    result, status = HintService.request_hint(phase)
    return jsonify(result), status


@puzzle_bp.route('/<int:phase>/hints', methods=['GET'])
def hints_summary(phase):
    """
    GET /api/puzzle/<phase>/hints
    Resumo de dicas usadas/disponíveis na fase (não cobra penalidade).

    Response:
        - phase, hints_used, hints_available, total_hints
        - penalty_per_hint, total_penalty
    """
    error = _validate_phase(phase)
    if error:
        return jsonify({'error': error}), 400

    summary = HintService.get_hints_summary(phase)
    if summary is None:
        return jsonify({'error': 'Puzzle não encontrado'}), 404

    return jsonify(summary), 200
