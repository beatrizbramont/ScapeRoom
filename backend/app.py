
"""
🎄 ═══════════════════════════════════════════
   ESCAPE ROOM DE NATAL — Servidor Flask
   ═══════════════════════════════════════════

   Ponto de entrada principal da aplicação.
   Usa Blueprints para organizar as rotas.

   Como rodar:
     cd backend
     pip install -r requirements.txt
     python app.py
"""
import os
import sys

# Adiciona o diretório backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# No Windows o console usa cp1252 e quebraria os prints com emoji
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from flask import Flask, jsonify
from flask_cors import CORS
from config.settings import get_config
from routes import register_blueprints


def register_error_handlers(app):
    """A API responde JSON em qualquer situação — inclusive nos erros."""

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Requisição inválida', 'detail': error.description}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Rota não encontrada 🎅',
            'hint': 'Consulte /api/health para a lista de endpoints'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Método não permitido nesta rota'}), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Pane na oficina do Papai Noel ❄️'}), 500


def create_app(config_name=None):
    """
    Factory function para criar a aplicação Flask.

    Args:
        config_name: Nome do ambiente ('development', 'testing', 'production').
                     Se omitido, usa a variável FLASK_ENV.

    Returns:
        Instância configurada do Flask
    """
    app = Flask(__name__)

    # Carrega configurações
    config = get_config(config_name)
    app.config.from_object(config)

    # Habilita CORS para o React frontend
    CORS(app, supports_credentials=True, origins=[
        'http://localhost:5173',   # Vite dev server
        'http://localhost:3000',   # React dev server alternativo
        'http://127.0.0.1:5173',
        'http://127.0.0.1:3000',
    ])

    # Registra todos os blueprints (rotas) e os tratadores de erro
    register_blueprints(app)
    register_error_handlers(app)

    # Log de inicialização (silencioso durante os testes)
    if not app.config.get('TESTING'):
        port = os.getenv('PORT', 5000)
        print("=" * 50)
        print("🎄 ESCAPE ROOM DE NATAL — Servidor Flask")
        print("=" * 50)
        print(f"🌍 Ambiente: {config.__name__}")
        print(f"🔗 API: http://localhost:{port}")
        print(f"❤️  Health: http://localhost:{port}/api/health")
        print("=" * 50)

    return app


# ─── Ponto de entrada ───
if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=port
    )
