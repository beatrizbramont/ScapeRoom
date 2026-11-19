
// 📁 Pasta: frontend/src/components/shared/PasswordInput.jsx
import React, { useState } from 'react';

function PasswordInput({ maxLength, placeholder, onSubmit, buttonText, numbersOnly, uppercase }) {
  const [value, setValue] = useState('');

  const handleChange = (e) => {
    let val = e.target.value;
    if (numbersOnly) val = val.replace(/\D/g, '');
    if (uppercase) val = val.toUpperCase();
    setValue(val);
  };

  const handleSubmit = () => {
    if (value.trim()) {
      onSubmit(value.trim());
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSubmit();
  };

  return (
    <div className="password-input-group">
      <input
        type="text"
        maxLength={maxLength}
        value={value}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        className="password-input"
        autoComplete="off"
      />
      <button onClick={handleSubmit} className="btn-solve">
        {buttonText || '🔓 Enviar'}
      </button>
    </div>
  );
}

export default PasswordInput;

