
// 📁 Pasta: frontend/src/hooks/useGameState.js
// Hook que conecta o Context com os Services

import { useCallback, useEffect } from 'react';
import { useGame, ACTIONS } from '../context/GameContext';
import gameService from '../services/gameService';
import puzzleService from '../services/puzzleService';

export function useGameState() {
  const { state, dispatch, displayMessage } = useGame();

  // ─── Iniciar jogo ───
  const startGame = useCallback(async () => {
    try {
      const data = await gameService.startGame();
      if (data.success) {
        dispatch({ type: ACTIONS.START_GAME, payload: { timeRemaining: data.time_remaining } });
        displayMessage(data.message);
      }
      return data;
    } catch (err) {
      console.error('Erro ao iniciar:', err);
    }
  }, [dispatch, displayMessage]);

  // ─── Buscar status ───
  const fetchStatus = useCallback(async () => {
    try {
      const data = await gameService.getStatus();
      dispatch({
        type: ACTIONS.UPDATE_STATUS,
        payload: {
          timeRemaining: data.time_remaining,
          currentPhase: data.current_phase,
          completedPhases: data.completed_phases,
          totalHints: data.total_hints,
          foundObjects: data.found_objects,
          gameOver: data.game_over,
          victory: data.victory
        }
      });
      if (data.game_over && !data.victory) {
        dispatch({ type: ACTIONS.SET_GAME_OVER });
      }
      return data;
    } catch (err) {
      console.error('Erro ao buscar status:', err);
    }
  }, [dispatch]);

  // ─── Resolver puzzle ───
  const solvePuzzle = useCallback(async (phase, answer) => {
    try {
      const data = await puzzleService.solve(phase, answer);
      displayMessage(data.message);
      if (data.success) {
        if (data.victory) {
          dispatch({ type: ACTIONS.SET_VICTORY });
        } else if (data.next_phase) {
          dispatch({ type: ACTIONS.ADVANCE_PHASE, payload: data.next_phase });
        }
      }
      return data;
    } catch (err) {
      console.error('Erro ao resolver:', err);
      return { success: false };
    }
  }, [dispatch, displayMessage]);

  // ─── Clicar objeto (Fase 1) ───
  const clickObject = useCallback(async (objectName) => {
    try {
      const data = await puzzleService.clickObject(objectName);
      displayMessage(data.message);
      if (data.success) {
        dispatch({ type: ACTIONS.ADD_FOUND_OBJECT, payload: objectName });
      }
      return data;
    } catch (err) {
      console.error('Erro ao clicar:', err);
      return { success: false };
    }
  }, [dispatch, displayMessage]);

  // ─── Pedir dica ───
  const requestHint = useCallback(async (phase) => {
    try {
      const data = await puzzleService.requestHint(phase);
      if (data.time_remaining !== undefined) {
        dispatch({ type: ACTIONS.USE_HINT, payload: { timeRemaining: data.time_remaining } });
      }
      return data;
    } catch (err) {
      console.error('Erro ao pedir dica:', err);
      return null;
    }
  }, [dispatch]);

  // ─── Resetar ───
  const resetGame = useCallback(async () => {
    try {
      await gameService.resetGame();
      dispatch({ type: ACTIONS.RESET_GAME });
    } catch (err) {
      console.error('Erro ao resetar:', err);
    }
  }, [dispatch]);

  // ─── Polling de status a cada 1s ───
  useEffect(() => {
    if (state.started && !state.victory && !state.gameOver) {
      const interval = setInterval(fetchStatus, 1000);
      return () => clearInterval(interval);
    }
  }, [state.started, state.victory, state.gameOver, fetchStatus]);

  return {
    ...state,
    startGame,
    fetchStatus,
    solvePuzzle,
    clickObject,
    requestHint,
    resetGame
  };
}

export default useGameState;

