
"""
🛤️ Rotas da API — Escape Room de Natal
"""
from .game_routes import game_bp
from .puzzle_routes import puzzle_bp
from .health_routes import health_bp


def register_blueprints(app):
    """Registra todos os blueprints no app Flask"""
    app.register_blueprint(game_bp, url_prefix='/api/game')
    app.register_blueprint(puzzle_bp, url_prefix='/api/puzzle')
    app.register_blueprint(health_bp, url_prefix='/api')

