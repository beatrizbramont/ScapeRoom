
// 📁 Pasta: frontend/src/components/phases/Phase4Weight.jsx
import React, { useState } from 'react';
import HintButton from '../hud/HintButton';
import { PHASE4_WEIGHTS, SLEIGH_TARGET } from '../../utils/constants';
import '../../styles/Phase4.css';

function Phase4Weight({ solvePuzzle, requestHint }) {
  const [selectedWeights, setSelectedWeights] = useState([]);

  const currentWeight = selectedWeights.reduce((sum, w) => sum + w, 0);
  const difference = SLEIGH_TARGET - currentWeight;

  const toggleWeight = (kg) => {
    setSelectedWeights(prev =>
      prev.includes(kg) ? prev.filter(w => w !== kg) : [...prev, kg]
    );
  };

  const getBalanceAngle = () => {
    if (currentWeight === SLEIGH_TARGET) return 0;
    if (currentWeight < SLEIGH_TARGET) return -15;
    return 15;
  };

  const handleSolve = async () => {
    await solvePuzzle(4, selectedWeights);
  };

  return (
    <div className="phase-container phase-4">
      <div className="phase-header">
        <h2>⚖️ Fase 4 — Peso do Trenó</h2>
        <p>
          Equilibre os presentes na balança! O trenó precisa de exatamente
          <strong> {SLEIGH_TARGET} kg</strong> para decolar.
        </p>
      </div>

      {/* Balança visual */}
      <div className="scale-container">
        <div className="scale-beam" style={{ transform: `rotate(${getBalanceAngle()}deg)` }}>
          <div className="scale-left">
            <div className="scale-plate">
              {selectedWeights.map((kg, i) => {
                const w = PHASE4_WEIGHTS.find(a => a.kg === kg);
                return <span key={i} className="weight-on-scale">{w?.emoji}</span>;
              })}
            </div>
            <span className="scale-value">{currentWeight} kg</span>
          </div>
          <div className="scale-pivot">⚖️</div>
          <div className="scale-right">
            <div className="scale-plate">
              <span className="target-weight">🎯</span>
            </div>
            <span className="scale-value">{SLEIGH_TARGET} kg</span>
          </div>
        </div>
      </div>

      {/* Indicador de peso */}
      <div className={`weight-indicator ${currentWeight === SLEIGH_TARGET ? 'balanced' : ''}`}>
        <span className="current">Peso atual: <strong>{currentWeight} kg</strong></span>
        <span className="separator">|</span>
        <span className="target">Alvo: <strong>{SLEIGH_TARGET} kg</strong></span>
        <span className="separator">|</span>
        <span className={`diff ${difference === 0 ? 'zero' : difference > 0 ? 'under' : 'over'}`}>
          {difference === 0
            ? '✅ Equilibrado!'
            : difference > 0
              ? `Faltam ${difference} kg`
              : `Excesso de ${Math.abs(difference)} kg`}
        </span>
      </div>

      {/* Grid de pesos */}
      <div className="weights-grid">
        <h3>🎁 Sacos de Presentes Disponíveis:</h3>
        <div className="weights-list">
          {PHASE4_WEIGHTS.map(w => (
            <button
              key={w.kg}
              className={`weight-item ${selectedWeights.includes(w.kg) ? 'selected' : ''}`}
              onClick={() => toggleWeight(w.kg)}
            >
              <span className="weight-emoji">{w.emoji}</span>
              <span className="weight-label">{w.label}</span>
              <span className="weight-kg">{w.kg} kg</span>
            </button>
          ))}
        </div>
      </div>

      {/* Ações */}
      <div className="weight-actions">
        <button className="btn-solve" onClick={handleSolve}>🛷 Carregar Trenó</button>
        <button className="btn-reset-seq" onClick={() => setSelectedWeights([])}>🔄 Esvaziar</button>
      </div>

      <HintButton phase={4} onRequestHint={requestHint} />
    </div>
  );
}

export default Phase4Weight;

