
"""
💡 HintService — Sistema de dicas com penalidade
"""
from models.puzzle import puzzle_manager
from services.game_service import GameService
from config.settings import GameConfig


class HintService:
    """
    Serviço que gerencia o sistema de dicas do jogo.
    Cada dica usada aplica uma penalidade de tempo.
    """

    @classmethod
    def request_hint(cls, phase):
        """
        Processa um pedido de dica.
        
        Args:
            phase: Número da fase (1-4)
            
        Returns:
            dict com a dica, penalidade e tempo restante
        """
        state = GameService.get_state()
        puzzle = puzzle_manager.get_puzzle(phase)

        if not puzzle:
            return {'error': 'Fase inválida'}, 400

        # Mesmo porteiro usado para cliques e respostas
        blocked = GameService.ensure_active(state)
        if blocked:
            return blocked

        # Verifica se a fase está disponível
        if phase > state.current_phase:
            return {'error': 'Esta fase ainda está trancada!'}, 400

        # Tenta usar uma dica
        hint_index = state.use_hint(phase)

        if hint_index is None:
            return {
                'hint': '⚠️ Você já usou todas as dicas desta fase!',
                'penalty': 0,
                'time_remaining': state.get_remaining_time(),
                'hint_number': GameConfig.MAX_HINTS_PER_PHASE,
                'total_available': len(puzzle.hints),
                'exhausted': True
            }, 200

        # Busca a dica
        hint_text = puzzle.get_hint(hint_index)
        GameService.save_state(state)

        remaining = state.get_remaining_time()

        # Verifica se tempo acabou após a penalidade
        if remaining <= 0:
            state.game_over = True
            GameService.save_state(state)

        return {
            'hint': f'💡 {hint_text}',
            'penalty': GameConfig.HINT_PENALTY,
            'penalty_text': f'-{GameConfig.HINT_PENALTY // 60} min',
            'time_remaining': remaining,
            'hint_number': hint_index + 1,
            'total_available': len(puzzle.hints),
            'exhausted': False
        }, 200

    @classmethod
    def get_hints_summary(cls, phase):
        """
        Retorna resumo de dicas usadas em uma fase.
        
        Returns:
            dict com informações sobre uso de dicas
        """
        state = GameService.get_state()
        puzzle = puzzle_manager.get_puzzle(phase)

        if not puzzle:
            return None

        phase_key = str(phase)
        used = state.hints_used.get(phase_key, 0)
        total = len(puzzle.hints)

        return {
            'phase': phase,
            'hints_used': used,
            'hints_available': total - used,
            'total_hints': total,
            'penalty_per_hint': GameConfig.HINT_PENALTY,
            'total_penalty': used * GameConfig.HINT_PENALTY
        }

