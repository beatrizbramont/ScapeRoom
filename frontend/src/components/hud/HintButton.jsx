
// 📁 Pasta: frontend/src/components/hud/HintButton.jsx
import React, { useState } from 'react';

function HintButton({ phase, onRequestHint }) {
  const [hint, setHint] = useState('');
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    const data = await onRequestHint(phase);
    if (data && data.hint) {
      setHint(data.hint);
    }
    setLoading(false);
  };

  return (
    <div className="hint-section">
      <button
        className="btn-hint"
        onClick={handleClick}
        disabled={loading}
      >
        {loading ? '⏳ Carregando...' : '💡 Pedir Dica (-2min)'}
      </button>
      {hint && (
        <div className="hint-box">
          <span className="hint-icon">💡</span>
          <span className="hint-text">{hint}</span>
        </div>
      )}
    </div>
  );
}

export default HintButton;

