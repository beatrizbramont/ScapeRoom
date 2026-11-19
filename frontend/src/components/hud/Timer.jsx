
// 📁 Pasta: frontend/src/components/hud/Timer.jsx
import React from 'react';
import { useTimer } from '../../hooks/useTimer';

function Timer({ timeRemaining }) {
  const { formatted, isLowTime, status } = useTimer(timeRemaining);

  return (
    <div className={`hud-timer ${isLowTime ? 'low-time' : ''} timer-${status}`}>
      <span className="timer-icon">⏰</span>
      <span className="timer-text">{formatted}</span>
    </div>
  );
}

export default Timer;

