
// 📁 Pasta: frontend/src/components/hud/GameHUD.jsx
import React from 'react';
import Timer from './Timer';
import ProgressBar from './ProgressBar';
import { PHASE_NAMES, PHASE_ICONS } from '../../utils/constants';
import '../../styles/GameHUD.css';

function GameHUD({ timeRemaining, currentPhase, completedPhases, hintsUsed }) {
  return (
    <div className="game-hud">
      <Timer timeRemaining={timeRemaining} />

      <div className="hud-phases">
        {[1, 2, 3, 4].map(phase => (
          <div
            key={phase}
            className={`hud-phase
              ${completedPhases.includes(phase) ? 'completed' : ''}
              ${currentPhase === phase ? 'active' : ''}
              ${phase > currentPhase ? 'locked' : ''}`}
            title={PHASE_NAMES[phase - 1]}
          >
            <span className="phase-num">{PHASE_ICONS[phase - 1]}</span>
            <span className="phase-label">{PHASE_NAMES[phase - 1]}</span>
          </div>
        ))}
      </div>

      <ProgressBar completed={completedPhases.length} total={4} />

      <div className="hud-hints">
        <span>💡 Dicas: {hintsUsed}</span>
      </div>
    </div>
  );
}

export default GameHUD;

