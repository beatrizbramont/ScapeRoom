
// 📁 Pasta: frontend/src/components/shared/HintBox.jsx
import React from 'react';

function HintBox({ hint, hintNumber, totalHints }) {
  if (!hint) return null;

  return (
    <div className="hint-box">
      <div className="hint-header">
        <span className="hint-icon">💡</span>
        {hintNumber && totalHints && (
          <span className="hint-count">Dica {hintNumber}/{totalHints}</span>
        )}
      </div>
      <p className="hint-text">{hint}</p>
    </div>
  );
}

export default HintBox;

