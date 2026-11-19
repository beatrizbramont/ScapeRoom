
"""
🧩 Puzzle — Definição e validação dos enigmas do jogo
"""
import json
import os
from enum import Enum

from config.settings import GameConfig


class PuzzlePhase(Enum):
    """Enumeração das fases do jogo"""
    STAR_MAP = 1
    CIPHER = 2
    LIGHTS = 3
    WEIGHT = 4


class Puzzle:
    """
    Representa um puzzle individual com dados, validação e dicas.
    """

    def __init__(self, phase, name, answer, hints, **kwargs):
        self.phase = phase
        self.name = name
        self.answer = answer
        self.hints = hints
        self.extra = kwargs  # Dados extras específicos de cada fase

    def validate_answer(self, player_answer, game_state=None):
        """
        Valida a resposta do jogador.
        Retorna True se correto, False se incorreto.
        """
        if self.phase == PuzzlePhase.STAR_MAP.value:
            return str(player_answer).strip() == str(self.answer)

        elif self.phase == PuzzlePhase.CIPHER.value:
            return str(player_answer).strip().upper() == str(self.answer).upper()

        elif self.phase == PuzzlePhase.LIGHTS.value:
            if not isinstance(player_answer, list) or not game_state:
                return False
            # Sem partida iniciada não há sequência — uma lista vazia não é acerto
            if not game_state.light_sequence:
                return False
            return player_answer == game_state.light_sequence

        elif self.phase == PuzzlePhase.WEIGHT.value:
            return self._validate_weights(player_answer)

        return False

    def _validate_weights(self, player_answer):
        """
        Fase 4: os sacos escolhidos precisam existir na balança,
        não podem repetir e a soma tem que bater com o peso alvo.
        """
        if not isinstance(player_answer, list) or not player_answer:
            return False

        try:
            chosen = [float(w) for w in player_answer]
        except (ValueError, TypeError):
            return False

        # Cada saco está uma única vez na oficina
        if len(set(chosen)) != len(chosen):
            return False

        available = self.extra.get('available_weights', [])
        if available and any(w not in available for w in chosen):
            return False

        return abs(sum(chosen) - float(self.answer)) < 0.01

    def get_hint(self, hint_index):
        """Retorna a dica pelo índice"""
        if 0 <= hint_index < len(self.hints):
            return self.hints[hint_index]
        return None

    def get_public_info(self, game_state=None):
        """Retorna informações públicas do puzzle (sem a resposta!)"""
        info = {
            'phase': self.phase,
            'name': self.name,
            'total_hints': len(self.hints)
        }

        if self.phase == PuzzlePhase.STAR_MAP.value:
            info['objects'] = self.extra.get('objects', [])
            info['required_objects'] = self.extra.get('required_objects', [])
            info['required_count'] = len(self.extra.get('required_objects', []))
            if game_state:
                info['found_objects'] = game_state.found_objects

        elif self.phase == PuzzlePhase.CIPHER.value:
            info['encrypted_message'] = self.extra.get('encrypted', '')
            info['cipher_shift'] = self.extra.get('cipher_shift', 3)

        elif self.phase == PuzzlePhase.LIGHTS.value:
            info['colors'] = self.extra.get('colors', [])
            info['sequence_length'] = self.extra.get('sequence_length', 5)
            if game_state:
                info['sequence'] = game_state.light_sequence

        elif self.phase == PuzzlePhase.WEIGHT.value:
            info['available_weights'] = self.extra.get('available_weights', [])
            info['target_weight'] = self.answer

        return info

    def __repr__(self):
        return f"<Puzzle phase={self.phase} name='{self.name}'>"


class PuzzleManager:
    """
    Gerencia o carregamento e acesso aos puzzles do jogo.
    """

    def __init__(self):
        self.puzzles = {}
        self._load_puzzles()

    def _load_puzzles(self):
        """Carrega puzzles do arquivo JSON"""
        data_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'data', 'puzzles.json'
        )

        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            loaded = {}
            for puzzle_data in data.get('puzzles', []):
                phase = puzzle_data['phase']
                loaded[phase] = Puzzle(
                    phase=phase,
                    name=puzzle_data['name'],
                    answer=puzzle_data['answer'],
                    hints=puzzle_data['hints'],
                    **puzzle_data.get('extra', {})
                )

            # Só aceita o JSON se ele trouxer todas as fases do jogo
            if len(loaded) != GameConfig.TOTAL_PHASES:
                raise ValueError(
                    f'puzzles.json tem {len(loaded)} fases, esperado {GameConfig.TOTAL_PHASES}'
                )

            self.puzzles = loaded

        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, ValueError) as erro:
            # Fallback: o jogo continua de pé com os puzzles embutidos
            print(f'⚠️  Não foi possível ler data/puzzles.json ({erro}). Usando puzzles padrão.')
            self._load_default_puzzles()

    def _load_default_puzzles(self):
        """Puzzles padrão caso o JSON não esteja disponível"""
        self.puzzles = {
            1: Puzzle(
                phase=1, name="Mapa Estelar", answer="1225",
                hints=[
                    "Procure objetos que o Papai Noel usa na noite de Natal...",
                    "O relógio marca uma hora especial — meia-noite!",
                    "Junte os números: relógio(12), carta(2), cookie(5) → 1225"
                ],
                objects=["relogio", "carta", "cookie", "estrela", "meia", "presente"],
                required_objects=["relogio", "carta", "cookie"]
            ),
            2: Puzzle(
                phase=2, name="Lista Criptografada", answer="RENA",
                hints=[
                    "É uma Cifra de César... cada letra foi deslocada.",
                    "O deslocamento é de 3 posições para frente.",
                    "R-E-N-A: o animal que puxa o trenó!"
                ],
                encrypted="UHQD", cipher_shift=3
            ),
            3: Puzzle(
                phase=3, name="Sequência de Luzes", answer=None,
                hints=[
                    "Preste atenção na ordem das cores que acendem!",
                    "São 5 cores na sequência. Tente memorizar as 3 primeiras.",
                    "Respire fundo e observe novamente — você consegue!"
                ],
                colors=["vermelho", "verde", "azul", "amarelo"],
                sequence_length=5
            ),
            4: Puzzle(
                phase=4, name="Peso do Trenó", answer=100.0,
                hints=[
                    "O peso alvo do trenó é 100 kg exatos.",
                    "Tente combinar: 25 + 35 + 40 = 100!",
                    "Qualquer combinação que some 100 kg funciona!"
                ],
                available_weights=[5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]
            )
        }

    def get_puzzle(self, phase):
        """Retorna puzzle por fase"""
        return self.puzzles.get(phase)

    def get_all_phases(self):
        """Retorna lista de todas as fases"""
        return list(self.puzzles.keys())


# Instância global do gerenciador de puzzles
puzzle_manager = PuzzleManager()

