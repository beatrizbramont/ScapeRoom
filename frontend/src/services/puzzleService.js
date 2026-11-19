
// 📁 Pasta: frontend/src/services/puzzleService.js
// Endpoints dos puzzles: info, solve, click, hint

import { apiGet, apiPost } from './api';

const puzzleService = {
  /**
   * GET /api/puzzle/:phase/info — Info pública do puzzle
   */
  getInfo: (phase) => apiGet(`/puzzle/${phase}/info`),

  /**
   * POST /api/puzzle/:phase/solve — Envia resposta
   */
  solve: (phase, answer) => apiPost(`/puzzle/${phase}/solve`, { answer }),

  /**
   * POST /api/puzzle/1/click — Clica em objeto (Fase 1)
   */
  clickObject: (objectName) => apiPost('/puzzle/1/click', { object: objectName }),

  /**
   * POST /api/puzzle/:phase/hint — Pede dica
   */
  requestHint: (phase) => apiPost(`/puzzle/${phase}/hint`)
};

export default puzzleService;

