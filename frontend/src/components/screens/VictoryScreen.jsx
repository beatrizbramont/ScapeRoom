
// 📁 Pasta: frontend/src/components/screens/VictoryScreen.jsx
import React from 'react';
import Snowflakes from '../shared/Snowflakes';
import { formatTime } from '../../utils/formatTime';
import '../../styles/VictoryScreen.css';

function VictoryScreen({ time, hints, onRestart }) {
  const getStars = () => {
    if (hints === 0 && time < 900) return 3;
    if (hints <= 2 && time < 1500) return 2;
    return 1;
  };

  const stars = getStars();
  const timeStr = formatTime(time);

  return (
    <div className="victory-screen">
      <Snowflakes count={30} />

      <div className="victory-content">
        <h1>🎄 NATAL SALVO! 🎄</h1>
        <div className="victory-santa">🎅</div>
        <p className="victory-message">
          Parabéns! Você destrancou a oficina e o Papai Noel conseguiu
          entregar todos os presentes a tempo!
        </p>

        <div className="stars-display">
          {[1, 2, 3].map(i => (
            <span key={i} className={`star ${i <= stars ? 'earned' : 'empty'}`}>
              {i <= stars ? '⭐' : '☆'}
            </span>
          ))}
        </div>

        <div className="victory-stats">
          <div className="stat">
            <span className="stat-label">⏱️ Tempo</span>
            <span className="stat-value">{timeStr}</span>
          </div>
          <div className="stat">
            <span className="stat-label">💡 Dicas</span>
            <span className="stat-value">{hints}</span>
          </div>
          <div className="stat">
            <span className="stat-label">⭐ Estrelas</span>
            <span className="stat-value">{stars}/3</span>
          </div>
        </div>

        <button className="start-button" onClick={onRestart}>
          🔄 Jogar Novamente
        </button>
      </div>
    </div>
  );
}

export default VictoryScreen;

