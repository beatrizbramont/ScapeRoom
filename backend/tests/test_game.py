
"""
🧪 Testes do fluxo principal do jogo
Rodar: cd backend && pytest tests/ -v

As fixtures (client, started_game, post_json, get_json) vêm do conftest.py.
"""
import json

from config.settings import GameConfig


class TestGameStart:
    """Testes de início do jogo"""

    def test_start_game_success(self, client):
        """Deve iniciar o jogo com sucesso"""
        response = client.post('/api/game/start')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['success'] is True
        assert data['time_remaining'] == 1800
        assert data['current_phase'] == 1
        assert data['total_phases'] == 4

    def test_start_game_resets_previous(self, started_game):
        """Deve resetar o jogo anterior ao iniciar novo"""
        response = started_game.post('/api/game/start')
        data = json.loads(response.data)

        assert data['success'] is True
        assert data['current_phase'] == 1

    def test_start_generates_light_sequence(self, get_json, started_game):
        """Deve gerar a sequência de luzes da Fase 3 logo no início"""
        data = get_json('/api/puzzle/3/info')

        assert len(data['sequence']) == GameConfig.LIGHT_SEQUENCE_LENGTH
        assert all(cor in data['colors'] for cor in data['sequence'])

    def test_restart_clears_progress(self, get_json, post_json, started_game):
        """Recomeçar deve apagar o progresso anterior"""
        post_json('/api/puzzle/1/solve', {'answer': '1225'})
        started_game.post('/api/game/start')

        status = get_json('/api/game/status')
        assert status['current_phase'] == 1
        assert status['completed_phases'] == []
        assert status['found_objects'] == []
        assert status['total_hints'] == 0


class TestGameStatus:
    """Testes do status do jogo"""

    def test_status_before_start(self, client):
        """Deve retornar estado inicial antes de começar"""
        response = client.get('/api/game/status')
        data = json.loads(response.data)

        assert data['started'] is False
        assert data['current_phase'] == 1
        assert data['completed_phases'] == []

    def test_status_after_start(self, started_game):
        """Deve retornar estado ativo após início"""
        response = started_game.get('/api/game/status')
        data = json.loads(response.data)

        assert data['started'] is True
        assert data['time_remaining'] > 0
        assert data['game_over'] is False

    def test_status_time_decreases(self, started_game):
        """Tempo deve estar diminuindo"""
        import time

        response1 = started_game.get('/api/game/status')
        data1 = json.loads(response1.data)

        time.sleep(1)

        response2 = started_game.get('/api/game/status')
        data2 = json.loads(response2.data)

        assert data2['time_remaining'] <= data1['time_remaining']

    def test_status_has_hud_fields(self, get_json, started_game):
        """Status deve trazer os campos prontos para o HUD"""
        data = get_json('/api/game/status')

        assert ':' in data['time_formatted']
        assert data['time_status'] in ('normal', 'warning', 'critical')
        assert data['progress'] == 0
        assert data['total_phases'] == GameConfig.TOTAL_PHASES


class TestGameReset:
    """Testes de reset do jogo"""

    def test_reset_game(self, started_game):
        """Deve resetar o jogo"""
        response = started_game.post('/api/game/reset')
        data = json.loads(response.data)

        assert data['success'] is True

        # Verifica que voltou ao estado inicial
        status = started_game.get('/api/game/status')
        status_data = json.loads(status.data)
        assert status_data['started'] is False

    def test_cannot_play_after_reset(self, post_json, started_game):
        """Depois do reset não dá para continuar de onde parou"""
        started_game.post('/api/game/reset')

        response, data = post_json('/api/puzzle/1/solve', {'answer': '1225'})
        assert response.status_code == 400
        assert data['started'] is False


class TestGameInfo:
    """Regras do jogo expostas para a tela inicial"""

    def test_info_does_not_need_a_session(self, get_json):
        data = get_json('/api/game/info')

        assert data['total_phases'] == GameConfig.TOTAL_PHASES
        assert data['duration_seconds'] == GameConfig.GAME_DURATION
        assert data['duration_formatted'] == '30:00'
        assert data['hint_penalty_seconds'] == GameConfig.HINT_PENALTY


class TestRequiresStartedGame:
    """Nada pode acontecer antes de a partida começar"""

    def test_cannot_solve_before_start(self, post_json):
        response, data = post_json('/api/puzzle/1/solve', {'answer': '1225'})

        assert response.status_code == 400
        assert data['started'] is False

    def test_cannot_click_before_start(self, post_json):
        response, data = post_json('/api/puzzle/1/click', {'object': 'relogio'})

        assert response.status_code == 400
        assert data['started'] is False

    def test_cannot_use_hint_before_start(self, client):
        response = client.post('/api/puzzle/1/hint')

        assert response.status_code == 400
        assert json.loads(response.data)['started'] is False

    def test_empty_light_sequence_is_not_a_win(self, post_json):
        """Sem partida a sequência está vazia — [] não pode ser aceito"""
        response, data = post_json('/api/puzzle/3/solve', {'answer': []})

        assert response.status_code == 400
        assert data['started'] is False


class TestGameFlow:
    """Testes do fluxo completo do jogo"""

    def test_cannot_skip_phases(self, started_game):
        """Não deve permitir pular fases"""
        response = started_game.post(
            '/api/puzzle/3/solve',
            data=json.dumps({'answer': ['vermelho']}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert 'error' in data

    def test_phase1_click_and_solve(self, started_game):
        """Deve completar a Fase 1 corretamente"""
        # Clica nos 3 objetos corretos
        for obj in ['relogio', 'carta', 'cookie']:
            response = started_game.post(
                '/api/puzzle/1/click',
                data=json.dumps({'object': obj}),
                content_type='application/json'
            )
            data = json.loads(response.data)
            assert data['success'] is True

        # Resolve com a senha correta
        response = started_game.post(
            '/api/puzzle/1/solve',
            data=json.dumps({'answer': '1225'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['next_phase'] == 2

    def test_full_playthrough_victory(self, get_json, post_json, started_game):
        """Deve vencer o jogo ao resolver as 4 fases em sequência"""
        # Fase 1 — Mapa Estelar
        _, data = post_json('/api/puzzle/1/solve', {'answer': '1225'})
        assert data['next_phase'] == 2

        # Fase 2 — Lista Criptografada (Cifra de César)
        _, data = post_json('/api/puzzle/2/solve', {'answer': 'RENA'})
        assert data['next_phase'] == 3

        # Fase 3 — Sequência de Luzes (lida do próprio estado da partida)
        sequencia = get_json('/api/puzzle/3/info')['sequence']
        _, data = post_json('/api/puzzle/3/solve', {'answer': sequencia})
        assert data['next_phase'] == 4

        # Fase 4 — Peso do Trenó (25 + 35 + 40 = 100 kg)
        _, data = post_json('/api/puzzle/4/solve', {'answer': [25.0, 35.0, 40.0]})
        assert data['success'] is True
        assert data['victory'] is True
        assert data['hints_used'] == 0

        # Estado final deve refletir a vitória
        status = get_json('/api/game/status')
        assert status['victory'] is True
        assert status['game_over'] is True
        assert status['completed_phases'] == [1, 2, 3, 4]
        assert status['progress'] == 100

    def test_wrong_answer_keeps_phase(self, get_json, post_json, started_game):
        """Resposta errada não deve avançar de fase"""
        _, data = post_json('/api/puzzle/1/solve', {'answer': '0000'})
        assert data['success'] is False

        status = get_json('/api/game/status')
        assert status['current_phase'] == 1
        assert status['completed_phases'] == []


class TestAfterVictory:
    """Partida encerrada não aceita mais jogadas"""

    def _vencer(self, get_json, post_json):
        post_json('/api/puzzle/1/solve', {'answer': '1225'})
        post_json('/api/puzzle/2/solve', {'answer': 'RENA'})
        sequencia = get_json('/api/puzzle/3/info')['sequence']
        post_json('/api/puzzle/3/solve', {'answer': sequencia})
        post_json('/api/puzzle/4/solve', {'answer': [25.0, 35.0, 40.0]})

    def test_solving_again_reports_victory_not_timeout(
        self, get_json, post_json, started_game
    ):
        """O erro precisa dizer que já venceu — e não 'tempo esgotado'"""
        self._vencer(get_json, post_json)

        response, data = post_json('/api/puzzle/4/solve', {'answer': [25.0, 35.0, 40.0]})

        assert response.status_code == 400
        assert data['victory'] is True
        assert 'Tempo esgotado' not in data['error']

    def test_hint_after_victory_is_blocked(self, get_json, post_json, started_game):
        self._vencer(get_json, post_json)

        response = started_game.post('/api/puzzle/1/hint')
        assert response.status_code == 400
        assert json.loads(response.data)['victory'] is True


class TestErrorResponses:
    """A API nunca deve devolver HTML"""

    def test_unknown_route_returns_json(self, client):
        response = client.get('/api/rota/que/nao/existe')

        assert response.status_code == 404
        assert response.is_json
        assert 'error' in json.loads(response.data)

    def test_wrong_method_returns_json(self, client):
        response = client.get('/api/game/start')   # start é POST

        assert response.status_code == 405
        assert response.is_json

    def test_malformed_json_body(self, client):
        """Corpo inválido não pode derrubar o servidor"""
        response = client.post(
            '/api/puzzle/1/solve',
            data='{isso nao e json',
            content_type='application/json'
        )

        assert response.status_code == 400
        assert response.is_json
