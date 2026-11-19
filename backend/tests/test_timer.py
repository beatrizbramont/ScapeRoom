
"""
🧪 Testes do cronômetro e das penalidades de tempo
Rodar: cd backend && pytest tests/test_timer.py -v
"""
import pytest
import time

from services.timer_service import TimerService
from models.game_state import GameState
from config.settings import GameConfig


class TestCalculateRemaining:
    """Cálculo do tempo restante"""

    def test_without_start_time_returns_full_duration(self):
        """Antes de começar, o tempo cheio está disponível"""
        assert TimerService.calculate_remaining(None, 0) == GameConfig.GAME_DURATION

    def test_just_started(self):
        """Logo após o início, resta praticamente a duração inteira"""
        restante = TimerService.calculate_remaining(time.time(), 0)
        assert GameConfig.GAME_DURATION - 2 <= restante <= GameConfig.GAME_DURATION

    def test_discounts_elapsed_time(self):
        """Deve descontar o tempo já decorrido"""
        começou_há_60s = time.time() - 60
        restante = TimerService.calculate_remaining(começou_há_60s, 0)

        assert restante == pytest.approx(GameConfig.GAME_DURATION - 60, abs=2)

    def test_discounts_hint_penalty(self):
        """Cada dica custa HINT_PENALTY segundos"""
        agora = time.time()
        sem_dica = TimerService.calculate_remaining(agora, 0)
        com_duas = TimerService.calculate_remaining(agora, 2)

        assert sem_dica - com_duas == pytest.approx(2 * GameConfig.HINT_PENALTY, abs=2)

    def test_never_goes_negative(self):
        """O tempo restante nunca fica negativo"""
        começou_há_muito = time.time() - (GameConfig.GAME_DURATION * 2)
        assert TimerService.calculate_remaining(começou_há_muito, 0) == 0

    def test_penalty_alone_can_end_the_game(self):
        """Dicas demais zeram o cronômetro sozinhas"""
        dicas = (GameConfig.GAME_DURATION // GameConfig.HINT_PENALTY) + 1
        assert TimerService.calculate_remaining(time.time(), dicas) == 0


class TestCalculateElapsed:
    """Cálculo do tempo gasto (tela de vitória)"""

    def test_elapsed_starts_at_zero(self):
        gasto = TimerService.calculate_elapsed(time.time(), 0)
        assert gasto == pytest.approx(0, abs=2)

    def test_elapsed_includes_penalty(self):
        """O tempo gasto soma o decorrido com as penalidades"""
        gasto = TimerService.calculate_elapsed(time.time() - 60, 1)
        esperado = 60 + GameConfig.HINT_PENALTY
        assert gasto == pytest.approx(esperado, abs=2)

    def test_elapsed_plus_remaining_is_duration(self):
        começou = time.time() - 120
        restante = TimerService.calculate_remaining(começou, 1)
        gasto = TimerService.calculate_elapsed(começou, 1)

        assert restante + gasto == GameConfig.GAME_DURATION


class TestIsTimeUp:
    """Verificação de fim de tempo"""

    def test_not_up_when_game_just_started(self):
        assert TimerService.is_time_up(time.time(), 0) is False

    def test_up_when_duration_passed(self):
        assert TimerService.is_time_up(time.time() - GameConfig.GAME_DURATION, 0) is True

    def test_not_up_before_start(self):
        assert TimerService.is_time_up(None, 0) is False


class TestFormatTime:
    """Formatação MM:SS"""

    @pytest.mark.parametrize('segundos,esperado', [
        (0, '00:00'),
        (5, '00:05'),
        (59, '00:59'),
        (60, '01:00'),
        (598, '09:58'),
        (1800, '30:00'),
    ])
    def test_formats_correctly(self, segundos, esperado):
        assert TimerService.format_time(segundos) == esperado

    def test_negative_becomes_zero(self):
        assert TimerService.format_time(-30) == '00:00'

    def test_accepts_float(self):
        assert TimerService.format_time(90.9) == '01:30'


class TestTimeStatus:
    """Status visual do cronômetro (verde / amarelo / vermelho)"""

    @pytest.mark.parametrize('restante,esperado', [
        (1800, 'normal'),
        (301, 'normal'),
        (300, 'warning'),
        (121, 'warning'),
        (120, 'critical'),
        (0, 'critical'),
    ])
    def test_thresholds(self, restante, esperado):
        assert TimerService.get_time_status(restante) == esperado


class TestPenaltyHelpers:
    """Informações da penalidade exibidas no HUD"""

    def test_penalty_amount(self):
        assert TimerService.get_penalty_amount() == GameConfig.HINT_PENALTY

    def test_penalty_formatted(self):
        """Com HINT_PENALTY=120 o texto deve ser '2 minutos'"""
        texto = TimerService.get_penalty_formatted()
        assert texto == f"{GameConfig.HINT_PENALTY // 60} minutos"

    def test_penalty_singular(self, monkeypatch):
        """Um minuto de penalidade deve usar o singular"""
        monkeypatch.setattr(GameConfig, 'HINT_PENALTY', 60)
        assert TimerService.get_penalty_formatted() == '1 minuto'


class TestGameStateTimer:
    """O GameState deve usar as mesmas regras de tempo"""

    def test_full_time_before_start(self):
        state = GameState()
        assert state.get_remaining_time() == GameConfig.GAME_DURATION
        assert state.is_time_up() is False

    def test_matches_timer_service(self):
        """GameState e TimerService devem concordar no tempo restante"""
        state = GameState()
        state.start()
        state.total_hints = 2

        esperado = TimerService.calculate_remaining(state.start_time, state.total_hints)
        assert state.get_remaining_time() == pytest.approx(esperado, abs=2)

    def test_hint_reduces_remaining_time(self):
        state = GameState()
        state.start()

        antes = state.get_remaining_time()
        state.use_hint(1)
        depois = state.get_remaining_time()

        assert antes - depois == pytest.approx(GameConfig.HINT_PENALTY, abs=2)

    def test_hints_are_capped_per_phase(self):
        """Depois de MAX_HINTS_PER_PHASE a fase não cobra mais penalidade"""
        state = GameState()
        state.start()

        for _ in range(GameConfig.MAX_HINTS_PER_PHASE):
            assert state.use_hint(1) is not None

        assert state.use_hint(1) is None
        assert state.total_hints == GameConfig.MAX_HINTS_PER_PHASE

    def test_time_up_after_duration(self):
        state = GameState()
        state.start()
        state.start_time = time.time() - GameConfig.GAME_DURATION

        assert state.get_remaining_time() == 0
        assert state.is_time_up() is True

    def test_elapsed_time_after_start(self):
        state = GameState()
        state.start()
        state.start_time = time.time() - 300

        assert state.get_elapsed_time() == pytest.approx(300, abs=2)

    def test_timer_survives_session_roundtrip(self):
        """O estado serializado para a sessão deve preservar o cronômetro"""
        state = GameState()
        state.start()
        state.total_hints = 1

        restaurado = GameState.from_dict(state.to_dict())

        assert restaurado.start_time == state.start_time
        assert restaurado.get_remaining_time() == pytest.approx(
            state.get_remaining_time(), abs=2
        )
