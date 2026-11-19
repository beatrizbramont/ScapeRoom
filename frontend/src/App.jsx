
// 📁 Pasta: frontend/src/App.jsx
import React from 'react';
import { useGameState } from './hooks/useGameState';
import StartScreen from './components/screens/StartScreen';
import VictoryScreen from './components/screens/VictoryScreen';
import GameOverScreen from './components/screens/GameOverScreen';
import GameHUD from './components/hud/GameHUD';
import FloatingMessage from './components/shared/FloatingMessage';
import Snowflakes from './components/shared/Snowflakes';
import Phase1StarMap from './components/phases/Phase1StarMap';
import Phase2Cipher from './components/phases/Phase2Cipher';
import Phase3Lights from './components/phases/Phase3Lights';
import Phase4Weight from './components/phases/Phase4Weight';
import { GAME_DURATION } from './utils/constants';

function App() {
  const {
    started, currentPhase, completedPhases,
    timeRemaining, totalHints, victory, gameOver,
    message, showMessage,
    startGame, solvePuzzle, clickObject, requestHint, resetGame
  } = useGameState();

  // ─── Telas especiais ───
  if (!started) {
    return <StartScreen onStart={startGame} />;
  }

  if (victory) {
    return (
      <VictoryScreen
        time={GAME_DURATION - timeRemaining}
        hints={totalHints}
        onRestart={resetGame}
      />
    );
  }

  if (gameOver) {
    return <GameOverScreen onRestart={resetGame} />;
  }

  // ─── Renderiza fase atual ───
  const renderPhase = () => {
    const props = { solvePuzzle, requestHint };
    switch (currentPhase) {
      case 1: return <Phase1StarMap {...props} clickObject={clickObject} />;
      case 2: return <Phase2Cipher {...props} />;
      case 3: return <Phase3Lights {...props} />;
      case 4: return <Phase4Weight {...props} />;
      default: return null;
    }
  };

  return (
    <div className="game-container">
      <Snowflakes count={30} />

      <GameHUD
        timeRemaining={timeRemaining}
        currentPhase={currentPhase}
        completedPhases={completedPhases}
        hintsUsed={totalHints}
      />

      <FloatingMessage message={message} visible={showMessage} />

      <div className="puzzle-area">
        {renderPhase()}
      </div>
    </div>
  );
}

export default App;

