
// 📁 Pasta: frontend/src/components/phases/Phase2Cipher.jsx
import React, { useState } from 'react';
import PasswordInput from '../shared/PasswordInput';
import HintButton from '../hud/HintButton';
import { caesarDecrypt, getAlphabet, getShiftedAlphabet } from '../../utils/cipherUtils';
import { CHRISTMAS_SYMBOLS } from '../../utils/constants';
import '../../styles/Phase2.css';

function Phase2Cipher({ solvePuzzle, requestHint }) {
  const [decoderShift, setDecoderShift] = useState(0);

  const encryptedMessage = 'UHQD';
  const alphabet = getAlphabet();
  const shiftedAlphabet = getShiftedAlphabet(decoderShift);
  const decodedPreview = caesarDecrypt(encryptedMessage, decoderShift);

  const handleSolve = async (answer) => {
    await solvePuzzle(2, answer);
  };

  return (
    <div className="phase-container phase-2">
      <div className="phase-header">
        <h2>📜 Fase 2 — Lista Criptografada</h2>
        <p>Os duendes escreveram uma mensagem secreta! Decifre o código para avançar.</p>
      </div>

      {/* Mensagem criptografada */}
      <div className="cipher-display">
        <div className="scroll-paper">
          <h3>📋 Mensagem dos Duendes:</h3>
          <div className="encrypted-text">
            {encryptedMessage.split('').map((char, i) => (
              <span key={i} className="cipher-letter">
                <span className="symbol">{CHRISTMAS_SYMBOLS[char] || char}</span>
                <span className="letter">{char}</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Roda decodificadora */}
      <div className="decoder-section">
        <h3>🔄 Roda Decodificadora</h3>
        <p>Ajuste o deslocamento da Cifra de César:</p>

        <div className="decoder-wheel">
          <button className="btn-shift" onClick={() => setDecoderShift(s => (s - 1 + 26) % 26)}>◀</button>
          <span className="shift-display">Deslocamento: {decoderShift}</span>
          <button className="btn-shift" onClick={() => setDecoderShift(s => (s + 1) % 26)}>▶</button>
        </div>

        <div className="decode-preview">
          <span className="label">Resultado:</span>
          <span className="decoded-text">{decodedPreview}</span>
        </div>

        {/* Tabela de referência */}
        <div className="cipher-table">
          <div className="cipher-row original">
            {alphabet.split('').map(l => (
              <span key={l} className="cipher-cell">{l}</span>
            ))}
          </div>
          <div className="cipher-row shifted">
            {shiftedAlphabet.map((l, i) => (
              <span key={i} className="cipher-cell">{l}</span>
            ))}
          </div>
        </div>
      </div>

      {/* Resposta */}
      <div className="password-section">
        <p>🔓 Qual é a palavra secreta?</p>
        <PasswordInput
          maxLength={10}
          placeholder="Digite a palavra..."
          onSubmit={handleSolve}
          buttonText="📜 Decifrar"
          uppercase
        />
      </div>

      <HintButton phase={2} onRequestHint={requestHint} />
    </div>
  );
}

export default Phase2Cipher;

