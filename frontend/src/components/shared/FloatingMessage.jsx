
// 📁 Pasta: frontend/src/components/shared/FloatingMessage.jsx
import React from 'react';

function FloatingMessage({ message, visible }) {
  if (!visible || !message) return null;

  return (
    <div className="floating-message">
      <p>{message}</p>
    </div>
  );
}

export default FloatingMessage;

