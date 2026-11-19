
"""
🎮 GameState — Gerencia o estado completo de uma sessão de jogo
"""
import time
import random
from config.settings import GameConfig


class GameState:
    """
    Representa o estado atual de uma partida do Escape Room.
    Armazenado na sessão Flask do jogador.
    """

    def __init__(self):
        self.started = False
        self.start_time = None
        self.current_phase = 1
        self.completed_phases = []
        self.hints_used = {str(i): 0 for i in range(1, GameConfig.TOTAL_PHASES + 1)}
        self.total_hints = 0
        self.found_objects = []
        self.light_sequence = []
        self.game_over = False
        self.victory = False

    def start(self):
        """Inicia uma nova partida"""
        self.started = True
        self.start_time = time.time()
        self.current_phase = 1
        self.completed_phases = []
        self.hints_used = {str(i): 0 for i in range(1, GameConfig.TOTAL_PHASES + 1)}
        self.total_hints = 0
        self.found_objects = []
        self.game_over = False
        self.victory = False

        # Gera sequência aleatória de luzes para Fase 3
        self.light_sequence = [
            random.choice(GameConfig.AVAILABLE_COLORS)
            for _ in range(GameConfig.LIGHT_SEQUENCE_LENGTH)
        ]

    def get_remaining_time(self):
        """Calcula tempo restante considerando penalidades"""
        if not self.started or not self.start_time:
            return GameConfig.GAME_DURATION

        elapsed = time.time() - self.start_time
        penalty = self.total_hints * GameConfig.HINT_PENALTY
        remaining = GameConfig.GAME_DURATION - elapsed - penalty
        return max(0, round(remaining))

    def is_time_up(self):
        """Verifica se o tempo acabou"""
        return self.get_remaining_time() <= 0

    def advance_phase(self):
        """Avança para a próxima fase"""
        self.completed_phases.append(self.current_phase)
        if self.current_phase < GameConfig.TOTAL_PHASES:
            self.current_phase += 1
            return False  # Não é vitória ainda
        else:
            self.victory = True
            self.game_over = True
            return True  # Vitória!

    def add_found_object(self, obj_name):
        """Registra objeto encontrado na Fase 1"""
        if obj_name not in self.found_objects:
            self.found_objects.append(obj_name)
            return True
        return False

    def use_hint(self, phase):
        """Registra uso de dica e aplica penalidade"""
        phase_key = str(phase)
        current_hints = self.hints_used.get(phase_key, 0)

        if current_hints >= GameConfig.MAX_HINTS_PER_PHASE:
            return None  # Sem dicas disponíveis

        self.hints_used[phase_key] = current_hints + 1
        self.total_hints += 1
        return current_hints  # Retorna o índice da dica usada

    def get_elapsed_time(self):
        """Retorna tempo decorrido"""
        remaining = self.get_remaining_time()
        return GameConfig.GAME_DURATION - remaining

    def to_dict(self):
        """Serializa o estado para a sessão"""
        return {
            'started': self.started,
            'start_time': self.start_time,
            'current_phase': self.current_phase,
            'completed_phases': self.completed_phases,
            'hints_used': self.hints_used,
            'total_hints': self.total_hints,
            'found_objects': self.found_objects,
            'light_sequence': self.light_sequence,
            'game_over': self.game_over,
            'victory': self.victory
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstrói o estado a partir da sessão"""
        state = cls()
        if data:
            state.started = data.get('started', False)
            state.start_time = data.get('start_time')
            state.current_phase = data.get('current_phase', 1)
            state.completed_phases = data.get('completed_phases', [])
            state.hints_used = data.get('hints_used', {str(i): 0 for i in range(1, 5)})
            state.total_hints = data.get('total_hints', 0)
            state.found_objects = data.get('found_objects', [])
            state.light_sequence = data.get('light_sequence', [])
            state.game_over = data.get('game_over', False)
            state.victory = data.get('victory', False)
        return state

