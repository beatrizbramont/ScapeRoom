
"""
🎮 GameService — Lógica central do jogo
"""
from flask import session
from models.game_state import GameState
from models.puzzle import puzzle_manager
from services.timer_service import TimerService
from config.settings import GameConfig


class GameService:
    """
    Serviço principal que orquestra toda a lógica do jogo.
    """

    @staticmethod
    def get_state():
        """Recupera ou cria o estado do jogo na sessão"""
        game_data = session.get('game')
        if game_data:
            return GameState.from_dict(game_data)
        return GameState()

    @staticmethod
    def save_state(state):
        """Salva o estado do jogo na sessão"""
        session['game'] = state.to_dict()
        session.modified = True

    @classmethod
    def ensure_active(cls, state):
        """
        Porteiro de toda ação que mexe na partida.

        Returns:
            None se o jogo está rolando, ou (dict de erro, status) se não está.
        """
        if not state.started:
            return {
                'error': 'Nenhuma partida em andamento. Comece em /api/game/start! 🎅',
                'started': False
            }, 400

        if state.victory:
            return {
                'error': 'Você já salvou o Natal! Reinicie para jogar de novo. 🎄',
                'victory': True,
                'game_over': True
            }, 400

        if state.is_time_up() or state.game_over:
            if not state.game_over:
                state.game_over = True
                cls.save_state(state)
            return {'error': 'Tempo esgotado! ⏰', 'game_over': True}, 400

        return None

    @classmethod
    def start_new_game(cls):
        """Inicia uma nova partida"""
        state = GameState()
        state.start()
        cls.save_state(state)

        return {
            'success': True,
            'message': 'Bem-vindo à Oficina do Papai Noel! 🎅',
            'time_remaining': GameConfig.GAME_DURATION,
            'current_phase': 1,
            'total_phases': GameConfig.TOTAL_PHASES
        }

    @classmethod
    def get_status(cls):
        """Retorna o status atual completo do jogo"""
        state = cls.get_state()
        remaining = state.get_remaining_time()

        # Verifica se o tempo acabou
        if remaining <= 0 and state.started and not state.victory:
            state.game_over = True
            cls.save_state(state)

        return {
            'started': state.started,
            'current_phase': state.current_phase,
            'completed_phases': state.completed_phases,
            'total_phases': GameConfig.TOTAL_PHASES,
            'progress': round(
                len(state.completed_phases) / GameConfig.TOTAL_PHASES * 100
            ),
            'time_remaining': remaining,
            'time_formatted': TimerService.format_time(remaining),
            'time_status': TimerService.get_time_status(remaining),
            'hints_used': state.hints_used,
            'total_hints': state.total_hints,
            'found_objects': state.found_objects,
            'game_over': state.game_over,
            'victory': state.victory
        }

    @classmethod
    def get_puzzle_info(cls, phase):
        """Retorna informações públicas de um puzzle"""
        puzzle = puzzle_manager.get_puzzle(phase)
        if not puzzle:
            return None

        state = cls.get_state()
        info = puzzle.get_public_info(state)
        info['started'] = state.started
        info['locked'] = not state.started or phase > state.current_phase
        info['completed'] = phase in state.completed_phases

        return info

    @classmethod
    def click_object(cls, object_name):
        """Fase 1: Processa clique em um objeto"""
        state = cls.get_state()

        blocked = cls.ensure_active(state)
        if blocked:
            return blocked

        if state.current_phase != 1:
            return {'error': 'Fase não disponível'}, 400

        puzzle = puzzle_manager.get_puzzle(1)
        required = puzzle.extra.get('required_objects', [])
        obj = object_name.lower()

        # Verifica se é um objeto válido e necessário
        if obj in required and obj not in state.found_objects:
            state.add_found_object(obj)
            cls.save_state(state)

            all_found = len(state.found_objects) == len(required)
            return {
                'success': True,
                'message': f'Objeto encontrado: {obj}! 🔍',
                'found_objects': state.found_objects,
                'all_found': all_found
            }, 200

        elif obj in state.found_objects:
            return {
                'success': False,
                'message': 'Você já encontrou este objeto!'
            }, 200
        else:
            return {
                'success': False,
                'message': 'Este objeto não é uma pista...'
            }, 200

    @classmethod
    def solve_puzzle(cls, phase, answer):
        """Valida a resposta de qualquer fase"""
        state = cls.get_state()

        blocked = cls.ensure_active(state)
        if blocked:
            return blocked

        if phase != state.current_phase:
            return {'error': 'Complete as fases anteriores primeiro!'}, 400

        puzzle = puzzle_manager.get_puzzle(phase)
        if not puzzle:
            return {'error': 'Fase inválida'}, 400

        # Valida a resposta
        correct = puzzle.validate_answer(answer, state)

        if correct:
            is_victory = state.advance_phase()
            cls.save_state(state)

            if is_victory:
                elapsed = state.get_elapsed_time()
                return {
                    'success': True,
                    'message': '🎄 PARABÉNS! Você salvou o Natal! 🎅✨',
                    'victory': True,
                    'time_elapsed': round(elapsed),
                    'hints_used': state.total_hints
                }, 200
            else:
                return {
                    'success': True,
                    'message': f'🎉 Fase {phase} completa! Avançando para a Fase {phase + 1}...',
                    'next_phase': phase + 1,
                    'victory': False
                }, 200
        else:
            return {
                'success': False,
                'message': '❌ Resposta incorreta! Tente novamente...'
            }, 200

    @classmethod
    def reset_game(cls):
        """Reinicia completamente o jogo"""
        session.pop('game', None)
        return {'success': True, 'message': 'Jogo reiniciado!'}

