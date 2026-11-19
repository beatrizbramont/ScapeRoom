
"""
⏰ TimerService — Gerenciamento do cronômetro do jogo
"""
import time
from config.settings import GameConfig


class TimerService:
    """
    Serviço responsável por todos os cálculos de tempo do jogo.
    """

    @staticmethod
    def calculate_remaining(start_time, total_hints):
        """
        Calcula o tempo restante considerando penalidades.
        
        Args:
            start_time: Timestamp Unix do início da partida
            total_hints: Número total de dicas usadas
            
        Returns:
            Tempo restante em segundos (mínimo 0)
        """
        if not start_time:
            return GameConfig.GAME_DURATION

        elapsed = time.time() - start_time
        penalty = total_hints * GameConfig.HINT_PENALTY
        remaining = GameConfig.GAME_DURATION - elapsed - penalty
        return max(0, round(remaining))

    @staticmethod
    def calculate_elapsed(start_time, total_hints):
        """
        Calcula o tempo decorrido (usado na tela de vitória).
        
        Returns:
            Tempo gasto em segundos
        """
        remaining = TimerService.calculate_remaining(start_time, total_hints)
        return GameConfig.GAME_DURATION - remaining

    @staticmethod
    def is_time_up(start_time, total_hints):
        """
        Verifica se o tempo esgotou.
        
        Returns:
            True se acabou, False se ainda há tempo
        """
        return TimerService.calculate_remaining(start_time, total_hints) <= 0

    @staticmethod
    def format_time(seconds):
        """
        Formata segundos em string MM:SS.
        
        Args:
            seconds: Tempo em segundos
            
        Returns:
            String formatada (ex: "29:58")
        """
        seconds = max(0, int(seconds))
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    @staticmethod
    def get_penalty_amount():
        """Retorna o valor da penalidade em segundos"""
        return GameConfig.HINT_PENALTY

    @staticmethod
    def get_penalty_formatted():
        """Retorna a penalidade formatada como texto"""
        penalty = GameConfig.HINT_PENALTY
        minutes = penalty // 60
        return f"{minutes} minuto{'s' if minutes != 1 else ''}"

    @staticmethod
    def get_time_status(remaining):
        """
        Retorna o status do tempo para feedback visual.
        
        Returns:
            'critical' | 'warning' | 'normal'
        """
        if remaining <= 120:    # 2 minutos
            return 'critical'
        elif remaining <= 300:  # 5 minutos
            return 'warning'
        return 'normal'

