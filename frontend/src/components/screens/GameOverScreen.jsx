
// 📁 Pasta: frontend/src/components/screens/GameOverScreen.jsx
import React from 'react';
import '../../styles/GameOverScreen.css';

function GameOverScreen({ onRestart }) {
  return (
    <div className="gameover-screen">
      <div className="gameover-content">
        <h1>⏰ TEMPO ESGOTADO!</h1>
        <div className="gameover-emoji">😢</div>
        <p>
          A tempestade de neve venceu desta vez... As crianças não
          receberão seus presentes!
        </p>
        <p className="gameover-tip">
          💡 Tente usar menos dicas e ser mais rápida nos enigmas!
        </p>
        <button className="start-button" onClick={onRestart}>
          🔄 Tentar Novamente
        </button>
      </div>
    </div>
  );
}

export default GameOverScreen;

