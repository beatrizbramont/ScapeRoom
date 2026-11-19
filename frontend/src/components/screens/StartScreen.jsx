
// 📁 Pasta: frontend/src/components/screens/StartScreen.jsx
import React from 'react';
import Snowflakes from '../shared/Snowflakes';
import { PHASE_NAMES, PHASE_ICONS } from '../../utils/constants';
import '../../styles/StartScreen.css';

function StartScreen({ onStart }) {
  return (
    <div className="start-screen">
      <Snowflakes count={20} />

      <div className="start-content">
        <div className="title-ornament">🎄</div>
        <h1 className="game-title">🎅 Escape Room de Natal</h1>
        <div className="subtitle">A Oficina do Papai Noel</div>

        <div className="story-box">
          <p>⚠️ <strong>ALERTA DE EMERGÊNCIA!</strong> ⚠️</p>
          <p>
            Uma terrível tempestade de neve trancou a oficina do Papai Noel
            faltando apenas <strong>30 minutos</strong> para a entrega dos presentes!
          </p>
          <p>
            Você precisa resolver 4 enigmas para encontrar as senhas e
            destrancar a porta do trenó. O Natal está em suas mãos! 🎁
          </p>
        </div>

        <div className="phases-preview">
          {PHASE_NAMES.map((name, i) => (
            <div key={i} className="phase-card">
              <span className="phase-icon">{PHASE_ICONS[i]}</span>
              <span>{name}</span>
            </div>
          ))}
        </div>

        <button className="start-button" onClick={onStart}>
          🔓 Iniciar Resgate
        </button>

        <p className="start-tip">💡 Cada dica usada custa 2 minutos do seu tempo!</p>
      </div>
    </div>
  );
}

export default StartScreen;

