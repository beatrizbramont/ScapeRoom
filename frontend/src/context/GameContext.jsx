
// 📁 Pasta: frontend/src/context/GameContext.jsx
import React, { createContext, useContext, useReducer, useCallback } from 'react';

const GameContext = createContext(null);

// ─── Estado Inicial ───
const initialState = {
  started: false,
  currentPhase: 1,
  completedPhases: [],
  timeRemaining: 1800,
  hintsUsed: {},
  totalHints: 0,
  foundObjects: [],
  gameOver: false,
  victory: false,
  message: '',
  showMessage: false,
  loading: false
};

// ─── Ações ───
const ACTIONS = {
  START_GAME: 'START_GAME',
  UPDATE_STATUS: 'UPDATE_STATUS',
  ADVANCE_PHASE: 'ADVANCE_PHASE',
  COMPLETE_PHASE: 'COMPLETE_PHASE',
  ADD_FOUND_OBJECT: 'ADD_FOUND_OBJECT',
  SET_ALL_FOUND: 'SET_ALL_FOUND',
  USE_HINT: 'USE_HINT',
  SET_VICTORY: 'SET_VICTORY',
  SET_GAME_OVER: 'SET_GAME_OVER',
  SHOW_MESSAGE: 'SHOW_MESSAGE',
  HIDE_MESSAGE: 'HIDE_MESSAGE',
  SET_LOADING: 'SET_LOADING',
  RESET_GAME: 'RESET_GAME',
  SET_TIME: 'SET_TIME'
};

// ─── Reducer ───
function gameReducer(state, action) {
  switch (action.type) {
    case ACTIONS.START_GAME:
      return {
        ...initialState,
        started: true,
        timeRemaining: action.payload?.timeRemaining || 1800
      };

    case ACTIONS.UPDATE_STATUS:
      return {
        ...state,
        ...action.payload
      };

    case ACTIONS.ADVANCE_PHASE:
      return {
        ...state,
        currentPhase: action.payload,
        completedPhases: [...state.completedPhases, state.currentPhase]
      };

    case ACTIONS.COMPLETE_PHASE:
      return {
        ...state,
        completedPhases: [...new Set([...state.completedPhases, action.payload])]
      };

    case ACTIONS.ADD_FOUND_OBJECT:
      return {
        ...state,
        foundObjects: [...state.foundObjects, action.payload]
      };

    case ACTIONS.USE_HINT:
      return {
        ...state,
        totalHints: state.totalHints + 1,
        timeRemaining: action.payload?.timeRemaining ?? state.timeRemaining
      };

    case ACTIONS.SET_VICTORY:
      return {
        ...state,
        victory: true,
        gameOver: true
      };

    case ACTIONS.SET_GAME_OVER:
      return {
        ...state,
        gameOver: true
      };

    case ACTIONS.SHOW_MESSAGE:
      return {
        ...state,
        message: action.payload,
        showMessage: true
      };

    case ACTIONS.HIDE_MESSAGE:
      return {
        ...state,
        showMessage: false
      };

    case ACTIONS.SET_LOADING:
      return {
        ...state,
        loading: action.payload
      };

    case ACTIONS.SET_TIME:
      return {
        ...state,
        timeRemaining: action.payload
      };

    case ACTIONS.RESET_GAME:
      return { ...initialState };

    default:
      return state;
  }
}

// ─── Provider ───
export function GameProvider({ children }) {
  const [state, dispatch] = useReducer(gameReducer, initialState);

  const displayMessage = useCallback((msg) => {
    dispatch({ type: ACTIONS.SHOW_MESSAGE, payload: msg });
    setTimeout(() => dispatch({ type: ACTIONS.HIDE_MESSAGE }), 3000);
  }, []);

  return (
    <GameContext.Provider value={{ state, dispatch, ACTIONS, displayMessage }}>
      {children}
    </GameContext.Provider>
  );
}

// ─── Hook de acesso ───
export function useGame() {
  const context = useContext(GameContext);
  if (!context) {
    throw new Error('useGame deve ser usado dentro de <GameProvider>');
  }
  return context;
}

export { ACTIONS };
export default GameContext;

