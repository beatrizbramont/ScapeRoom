
"""
🎄 Configurações globais do Escape Room de Natal
"""
import os
from dotenv import load_dotenv

# Carrega o .env do diretório backend/, não importa de onde o processo foi iniciado
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_BACKEND_DIR, '.env'))


class Config:
    """Configurações base do Flask"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'papai-noel-secreto-2026')

    # O estado da partida viaja num cookie de sessão assinado
    SESSION_PERMANENT = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'   # frontend e API dividem o host (localhost)
    SESSION_COOKIE_SECURE = False     # o ambiente de dev roda em http


class GameConfig:
    """Configurações específicas do jogo"""
    GAME_DURATION = int(os.getenv('GAME_DURATION', 1800))       # 30 min em segundos
    HINT_PENALTY = int(os.getenv('HINT_PENALTY', 120))          # 2 min por dica
    TOTAL_PHASES = 4
    MAX_HINTS_PER_PHASE = 3
    LIGHT_SEQUENCE_LENGTH = 5
    SLEIGH_TARGET_WEIGHT = 100.0

    # Cores disponíveis para Fase 3
    AVAILABLE_COLORS = ['vermelho', 'verde', 'azul', 'amarelo']

    # Pesos disponíveis para Fase 4
    AVAILABLE_WEIGHTS = [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


# Mapa de ambientes
config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}


def get_config(config_name=None):
    """
    Retorna a configuração do ambiente.

    Args:
        config_name: ambiente explícito ('development', 'testing', 'production').
                     Se omitido, cai no FLASK_ENV.
    """
    env = config_name or os.getenv('FLASK_ENV', 'development')
    return config_map.get(env, DevelopmentConfig)
