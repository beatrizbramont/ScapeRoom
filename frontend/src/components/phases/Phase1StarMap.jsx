
// 📁 Pasta: frontend/src/components/phases/Phase1StarMap.jsx
import React, { useState } from 'react';
import PasswordInput from '../shared/PasswordInput';
import HintButton from '../hud/HintButton';
import { PHASE1_OBJECTS } from '../../utils/constants';
import '../../styles/Phase1.css';

function Phase1StarMap({ solvePuzzle, requestHint, clickObject }) {
  const [foundObjects, setFoundObjects] = useState([]);
  const [allFound, setAllFound] = useState(false);

  const handleClick = async (obj) => {
    const result = await clickObject(obj.id);
    if (result && result.success) {
      setFoundObjects(prev => [...prev, obj.id]);
      if (result.all_found) setAllFound(true);
    }
  };

  const handleSolve = async (password) => {
    await solvePuzzle(1, password);
  };

  return (
    <div className="phase-container phase-1">
      <div className="phase-header">
        <h2>⭐ Fase 1 — Mapa Estelar</h2>
        <p>Explore a oficina e encontre os 3 objetos escondidos que revelam a senha!</p>
      </div>

      {/* Cenário interativo */}
      <div className="star-map-scene">
        <div className="workshop-room">
          {PHASE1_OBJECTS.map(obj => (
            <div
              key={obj.id}
              className={`clickable-object ${foundObjects.includes(obj.id) ? 'found' : ''}`}
              onClick={() => handleClick(obj)}
            >
              <span className="object-emoji">{obj.emoji}</span>
              <span className="object-name">{obj.name}</span>
              {foundObjects.includes(obj.id) && <span className="check">✅</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Contador */}
      <div className="found-counter">
        🔍 Objetos encontrados: {foundObjects.length}/3
        {foundObjects.map(id => {
          const obj = PHASE1_OBJECTS.find(o => o.id === id);
          return <span key={id} className="found-badge">{obj?.emoji}</span>;
        })}
      </div>

      {/* Campo de senha */}
      {allFound && (
        <div className="password-section animate-in">
          <p>🔓 Agora junte as pistas! Qual é a senha de 4 dígitos?</p>
          <PasswordInput
            maxLength={4}
            placeholder="_ _ _ _"
            onSubmit={handleSolve}
            buttonText="🔓 Enviar Senha"
            numbersOnly
          />
        </div>
      )}

      <HintButton phase={1} onRequestHint={requestHint} />
    </div>
  );
}

export default Phase1StarMap;

