
"""
🧪 Testes dos puzzles — validação, dicas e rotas
Rodar: cd backend && pytest tests/test_puzzles.py -v

As fixtures (client, started_game, post_json, get_json) vêm do conftest.py.
"""
import json
import pytest

from models.puzzle import PuzzlePhase, puzzle_manager
from models.game_state import GameState
from config.settings import GameConfig


class TestPuzzleManager:
    """Testes do carregamento dos puzzles"""

    def test_loads_all_four_phases(self):
        """Deve carregar as 4 fases do jogo"""
        assert sorted(puzzle_manager.get_all_phases()) == [1, 2, 3, 4]

    def test_every_phase_has_three_hints(self):
        """Cada fase deve ter 3 dicas"""
        for phase in range(1, GameConfig.TOTAL_PHASES + 1):
            puzzle = puzzle_manager.get_puzzle(phase)
            assert len(puzzle.hints) == GameConfig.MAX_HINTS_PER_PHASE

    def test_invalid_phase_returns_none(self):
        """Fase inexistente deve retornar None"""
        assert puzzle_manager.get_puzzle(99) is None

    def test_phase_enum_matches_names(self):
        """O enum de fases deve bater com os puzzles carregados"""
        assert PuzzlePhase.STAR_MAP.value == 1
        assert PuzzlePhase.CIPHER.value == 2
        assert PuzzlePhase.LIGHTS.value == 3
        assert PuzzlePhase.WEIGHT.value == 4


class TestPhase1StarMap:
    """Fase 1 — Mapa Estelar (senha 1225)"""

    def test_correct_password(self):
        puzzle = puzzle_manager.get_puzzle(1)
        assert puzzle.validate_answer('1225') is True

    def test_ignores_surrounding_spaces(self):
        puzzle = puzzle_manager.get_puzzle(1)
        assert puzzle.validate_answer('  1225  ') is True

    def test_accepts_number_instead_of_string(self):
        """O frontend pode mandar o número sem aspas"""
        puzzle = puzzle_manager.get_puzzle(1)
        assert puzzle.validate_answer(1225) is True

    def test_wrong_password(self):
        puzzle = puzzle_manager.get_puzzle(1)
        assert puzzle.validate_answer('1224') is False


class TestPhase2Cipher:
    """Fase 2 — Lista Criptografada (Cifra de César, UHQD → RENA)"""

    def test_correct_answer_is_case_insensitive(self):
        puzzle = puzzle_manager.get_puzzle(2)
        assert puzzle.validate_answer('RENA') is True
        assert puzzle.validate_answer('rena') is True

    def test_encrypted_message_decodes_to_answer(self):
        """Aplicar o deslocamento reverso na mensagem deve dar a resposta"""
        puzzle = puzzle_manager.get_puzzle(2)
        encrypted = puzzle.extra['encrypted']
        shift = puzzle.extra['cipher_shift']

        decoded = ''.join(
            chr((ord(letra) - ord('A') - shift) % 26 + ord('A'))
            for letra in encrypted
        )
        assert decoded == puzzle.answer

    def test_wrong_answer(self):
        puzzle = puzzle_manager.get_puzzle(2)
        assert puzzle.validate_answer('TRENO') is False


class TestPhase3Lights:
    """Fase 3 — Sequência de Luzes (gerada por partida)"""

    def _state_com_sequencia(self, sequencia):
        state = GameState()
        state.light_sequence = sequencia
        return state

    def test_matching_sequence(self):
        puzzle = puzzle_manager.get_puzzle(3)
        state = self._state_com_sequencia(
            ['vermelho', 'verde', 'azul', 'amarelo', 'verde']
        )
        assert puzzle.validate_answer(list(state.light_sequence), state) is True

    def test_wrong_order_fails(self):
        puzzle = puzzle_manager.get_puzzle(3)
        state = self._state_com_sequencia(
            ['vermelho', 'verde', 'azul', 'amarelo', 'verde']
        )
        invertida = list(reversed(state.light_sequence))
        assert puzzle.validate_answer(invertida, state) is False

    def test_requires_a_list(self):
        puzzle = puzzle_manager.get_puzzle(3)
        state = self._state_com_sequencia(['vermelho'])
        assert puzzle.validate_answer('vermelho', state) is False

    def test_requires_game_state(self):
        puzzle = puzzle_manager.get_puzzle(3)
        assert puzzle.validate_answer(['vermelho'], None) is False

    def test_empty_sequence_never_matches(self):
        """Partida não iniciada: [] == [] não pode valer vitória"""
        puzzle = puzzle_manager.get_puzzle(3)
        state = self._state_com_sequencia([])
        assert puzzle.validate_answer([], state) is False


class TestPhase4Weight:
    """Fase 4 — Peso do Trenó (100 kg exatos)"""

    def test_exact_weight(self):
        puzzle = puzzle_manager.get_puzzle(4)
        assert puzzle.validate_answer([25.0, 35.0, 40.0]) is True

    def test_other_valid_combination(self):
        puzzle = puzzle_manager.get_puzzle(4)
        assert puzzle.validate_answer([40.0, 30.0, 20.0, 10.0]) is True

    def test_order_does_not_matter(self):
        puzzle = puzzle_manager.get_puzzle(4)
        assert puzzle.validate_answer([40.0, 25.0, 35.0]) is True

    def test_wrong_total(self):
        puzzle = puzzle_manager.get_puzzle(4)
        assert puzzle.validate_answer([5.0, 10.0]) is False

    def test_non_numeric_values(self):
        puzzle = puzzle_manager.get_puzzle(4)
        assert puzzle.validate_answer(['pesado', 'leve']) is False

    def test_empty_list(self):
        puzzle = puzzle_manager.get_puzzle(4)
        assert puzzle.validate_answer([]) is False

    def test_rejects_weight_not_on_the_scale(self):
        """Não existe um saco de 100 kg na oficina"""
        puzzle = puzzle_manager.get_puzzle(4)
        assert puzzle.validate_answer([100.0]) is False

    def test_rejects_repeated_sack(self):
        """Cada saco só existe uma vez — 20+40+40 não vale"""
        puzzle = puzzle_manager.get_puzzle(4)
        assert puzzle.validate_answer([20.0, 40.0, 40.0]) is False

    def test_every_available_weight_is_usable(self):
        """Todos os pesos do JSON devem ser aceitos individualmente"""
        puzzle = puzzle_manager.get_puzzle(4)
        for peso in puzzle.extra['available_weights']:
            assert peso in GameConfig.AVAILABLE_WEIGHTS


class TestPublicInfo:
    """A resposta nunca pode vazar para o jogador"""

    @pytest.mark.parametrize('phase', [1, 2, 3])
    def test_answer_is_never_exposed(self, phase):
        puzzle = puzzle_manager.get_puzzle(phase)
        info = puzzle.get_public_info()

        assert 'answer' not in info
        assert str(puzzle.answer) not in json.dumps(info, ensure_ascii=False)

    def test_hints_are_not_exposed_upfront(self):
        """O /info informa quantas dicas existem, mas não o texto delas"""
        puzzle = puzzle_manager.get_puzzle(1)
        info = puzzle.get_public_info()

        assert info['total_hints'] == 3
        assert 'hints' not in info

    def test_get_hint_out_of_range(self):
        puzzle = puzzle_manager.get_puzzle(1)
        assert puzzle.get_hint(0) is not None
        assert puzzle.get_hint(99) is None
        assert puzzle.get_hint(-1) is None


class TestPuzzleRoutes:
    """Testes das rotas /api/puzzle/..."""

    def test_info_returns_public_data(self, get_json, started_game):
        data = get_json('/api/puzzle/1/info')

        assert data['name'] == 'Mapa Estelar'
        assert data['locked'] is False
        assert data['completed'] is False

    def test_info_marks_future_phase_as_locked(self, get_json, started_game):
        data = get_json('/api/puzzle/4/info')
        assert data['locked'] is True

    def test_info_locked_before_start(self, get_json):
        """Sem partida, até a Fase 1 aparece trancada"""
        data = get_json('/api/puzzle/1/info')

        assert data['started'] is False
        assert data['locked'] is True

    def test_invalid_phase_returns_400(self, client):
        response = client.get('/api/puzzle/9/info')
        assert response.status_code == 400
        assert 'error' in json.loads(response.data)

    def test_click_decoy_object(self, get_json, post_json, started_game):
        """Objeto que não é pista não deve entrar em found_objects"""
        _, data = post_json('/api/puzzle/1/click', {'object': 'estrela'})
        assert data['success'] is False

        info = get_json('/api/puzzle/1/info')
        assert 'estrela' not in info['found_objects']

    def test_click_same_object_twice(self, post_json, started_game):
        _, first = post_json('/api/puzzle/1/click', {'object': 'relogio'})
        _, second = post_json('/api/puzzle/1/click', {'object': 'relogio'})

        assert first['success'] is True
        assert second['success'] is False
        assert 'já encontrou' in second['message']

    def test_click_all_clues_sets_all_found(self, post_json, started_game):
        for obj in ['relogio', 'carta', 'cookie']:
            _, data = post_json('/api/puzzle/1/click', {'object': obj})
        assert data['all_found'] is True

    def test_click_without_body_returns_400(self, started_game):
        response = started_game.post('/api/puzzle/1/click')
        assert response.status_code == 400

    def test_click_only_works_on_phase_1(self, post_json, started_game):
        response, data = post_json('/api/puzzle/2/click', {'object': 'relogio'})
        assert response.status_code == 400
        assert 'error' in data

    def test_solve_without_answer_returns_400(self, post_json, started_game):
        response, data = post_json('/api/puzzle/1/solve', {})
        assert response.status_code == 400
        assert 'error' in data

    def test_solve_rejects_fake_weight_over_http(self, post_json, started_game):
        """O bypass [100.0] precisa ser barrado na rota também"""
        post_json('/api/puzzle/1/solve', {'answer': '1225'})
        post_json('/api/puzzle/2/solve', {'answer': 'RENA'})

        _, data = post_json('/api/puzzle/4/solve', {'answer': [100.0]})
        assert 'error' in data or data['success'] is False


class TestHints:
    """Testes do sistema de dicas e suas penalidades"""

    def test_first_hint_costs_time(self, get_json, started_game):
        antes = get_json('/api/game/status')['time_remaining']

        data = json.loads(started_game.post('/api/puzzle/1/hint').data)

        assert data['hint_number'] == 1
        assert data['penalty'] == GameConfig.HINT_PENALTY
        assert data['exhausted'] is False

        depois = get_json('/api/game/status')['time_remaining']
        assert antes - depois >= GameConfig.HINT_PENALTY

    def test_hints_are_sequential(self, started_game):
        numeros = []
        for _ in range(GameConfig.MAX_HINTS_PER_PHASE):
            data = json.loads(started_game.post('/api/puzzle/1/hint').data)
            numeros.append(data['hint_number'])

        assert numeros == [1, 2, 3]

    def test_hints_run_out(self, started_game):
        for _ in range(GameConfig.MAX_HINTS_PER_PHASE):
            started_game.post('/api/puzzle/1/hint')

        data = json.loads(started_game.post('/api/puzzle/1/hint').data)
        assert data['exhausted'] is True
        assert data['penalty'] == 0

    def test_hint_for_locked_phase(self, started_game):
        response = started_game.post('/api/puzzle/3/hint')
        assert response.status_code == 400
        assert 'trancada' in json.loads(response.data)['error']

    def test_hints_summary(self, get_json, started_game):
        started_game.post('/api/puzzle/1/hint')
        data = get_json('/api/puzzle/1/hints')

        assert data['hints_used'] == 1
        assert data['hints_available'] == 2
        assert data['total_penalty'] == GameConfig.HINT_PENALTY

    def test_hints_are_counted_per_phase(self, post_json, started_game):
        """Esgotar as dicas da Fase 1 não afeta a Fase 2"""
        for _ in range(GameConfig.MAX_HINTS_PER_PHASE):
            started_game.post('/api/puzzle/1/hint')

        post_json('/api/puzzle/1/solve', {'answer': '1225'})

        data = json.loads(started_game.post('/api/puzzle/2/hint').data)
        assert data['hint_number'] == 1
        assert data['exhausted'] is False
