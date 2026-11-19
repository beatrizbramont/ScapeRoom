
// 📁 Pasta: frontend/src/components/hud/ProgressBar.jsx
import React from 'react';

function ProgressBar({ completed, total }) {
  const percentage = (completed / total) * 100;

  return (
    <div className="hud-progress">
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="progress-text">{completed}/{total}</span>
    </div>
  );
}

export default ProgressBar;

