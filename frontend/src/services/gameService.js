
// 📁 Pasta: frontend/src/services/gameService.js
// Endpoints do jogo: start, status, reset

import { apiGet, apiPost } from './api';

const gameService = {
  /**
   * POST /api/game/start — Inicia nova partida
   */
  startGame: () => apiPost('/game/start'),

  /**
   * GET /api/game/status — Retorna estado do jogo
   */
  getStatus: () => apiGet('/game/status'),

  /**
   * POST /api/game/reset — Reinicia o jogo
   */
  resetGame: () => apiPost('/game/reset')
};

export default gameService;

