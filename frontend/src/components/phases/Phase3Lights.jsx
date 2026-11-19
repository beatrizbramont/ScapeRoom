
// 📁 Pasta: frontend/src/components/phases/Phase3Lights.jsx
import React, { useState, useEffect } from 'react';
import HintButton from '../hud/HintButton';
import { LIGHT_COLORS } from '../../utils/constants';
import puzzleService from '../../services/puzzleService';
import '../../styles/Phase3.css';

function Phase3Lights({ solvePuzzle, requestHint }) {
  const [sequence, setSequence] = useState([]);
  const [playerSequence, setPlayerSequence] = useState([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeColor, setActiveColor] = useState(null);
  const [sequenceLoaded, setSequenceLoaded] = useState(false);

  // Busca sequência do backend
  useEffect(() => {
    const fetchSequence = async () => {
      try {
        const data = await puzzleService.getInfo(3);
        if (data && data.sequence) {
          setSequence(data.sequence);
          setSequenceLoaded(true);
        }
      } catch (err) {
        console.error('Erro ao buscar sequência:', err);
      }
    };
    fetchSequence();
  }, []);

  // Reproduz sequência de luzes
  const playSequence = async () => {
    setIsPlaying(true);
    setPlayerSequence([]);

    for (let i = 0; i < sequence.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 600));
      setActiveColor(sequence[i]);
      await new Promise(resolve => setTimeout(resolve, 500));
      setActiveColor(null);
    }

    await new Promise(resolve => setTimeout(resolve, 300));
    setIsPlaying(false);
  };

  // Clique na cor
  const handleColorClick = (colorId) => {
    if (isPlaying) return;
    setActiveColor(colorId);
    setTimeout(() => setActiveColor(null), 200);
    setPlayerSequence(prev => [...prev, colorId]);
  };

  const handleSolve = async () => {
    await solvePuzzle(3, playerSequence);
  };

  return (
    <div className="phase-container phase-3">
      <div className="phase-header">
        <h2>💡 Fase 3 — Sequência de Luzes</h2>
        <p>Memorize a sequência do pisca-pisca e repita na ordem certa!</p>
      </div>

      {/* Luzes do Genius */}
      <div className="lights-board">
        {LIGHT_COLORS.map(c => (
          <button
            key={c.id}
            className={`light-button ${activeColor === c.id ? 'active' : ''}`}
            style={{ '--light-color': c.hex, '--light-glow': c.glow }}
            onClick={() => handleColorClick(c.id)}
            disabled={isPlaying}
          >
            {c.name}
          </button>
        ))}
      </div>

      {/* Controles */}
      <div className="lights-controls">
        <button
          className="btn-play"
          onClick={playSequence}
          disabled={isPlaying || !sequenceLoaded}
        >
          {isPlaying ? '🎵 Reproduzindo...' : '▶️ Ver Sequência'}
        </button>
      </div>

      {/* Sequência do jogador */}
      <div className="player-sequence">
        <h3>Sua sequência ({playerSequence.length}/{sequence.length}):</h3>
        <div className="sequence-display">
          {playerSequence.map((colorId, i) => {
            const color = LIGHT_COLORS.find(c => c.id === colorId);
            return (
              <span
                key={i}
                className="sequence-dot"
                style={{ backgroundColor: color?.hex }}
                title={color?.name}
              />
            );
          })}
          {[...Array(Math.max(0, sequence.length - playerSequence.length))].map((_, i) => (
            <span key={`empty-${i}`} className="sequence-dot empty" />
          ))}
        </div>
      </div>

      {/* Botões de ação */}
      <div className="lights-actions">
        <button
          className="btn-solve"
          onClick={handleSolve}
          disabled={playerSequence.length !== sequence.length}
        >
          ✨ Verificar Sequência
        </button>
        <button className="btn-reset-seq" onClick={() => setPlayerSequence([])}>
          🔄 Limpar
        </button>
      </div>

      <HintButton phase={3} onRequestHint={requestHint} />
    </div>
  );
}

export default Phase3Lights;

