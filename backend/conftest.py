
"""
🧪 Fixtures compartilhadas por toda a suíte de testes
"""
import json
import pytest

from app import create_app


@pytest.fixture
def client():
    """Cliente de teste Flask, com a config de 'testing'"""
    app = create_app('testing')
    with app.test_client() as client:
        yield client


@pytest.fixture
def started_game(client):
    """Mesmo cliente, mas com uma partida já iniciada"""
    client.post('/api/game/start')
    return client


@pytest.fixture
def post_json(client):
    """Helper: POST com corpo JSON, devolve (response, data)"""
    def _post(url, payload=None):
        response = client.post(
            url,
            data=json.dumps(payload if payload is not None else {}),
            content_type='application/json'
        )
        return response, json.loads(response.data)
    return _post


@pytest.fixture
def get_json(client):
    """Helper: GET que já devolve o JSON decodificado"""
    def _get(url):
        return json.loads(client.get(url).data)
    return _get
