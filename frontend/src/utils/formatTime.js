
// 📁 Pasta: frontend/src/utils/formatTime.js

/**
 * Formata segundos em MM:SS
 * @param {number} seconds — tempo em segundos
 * @returns {string} — ex: "29:58"
 */
export function formatTime(seconds) {
  const total = Math.max(0, Math.floor(seconds));
  const min = Math.floor(total / 60);
  const sec = total % 60;
  return `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
}

/**
 * Formata segundos em texto legível
 * @param {number} seconds
 * @returns {string} — ex: "5 minutos e 30 segundos"
 */
export function formatTimeText(seconds) {
  const total = Math.max(0, Math.floor(seconds));
  const min = Math.floor(total / 60);
  const sec = total % 60;

  if (min === 0) return `${sec} segundo${sec !== 1 ? 's' : ''}`;
  if (sec === 0) return `${min} minuto${min !== 1 ? 's' : ''}`;
  return `${min} minuto${min !== 1 ? 's' : ''} e ${sec} segundo${sec !== 1 ? 's' : ''}`;
}

export default formatTime;

