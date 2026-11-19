
// 📁 Pasta: frontend/src/utils/cipherUtils.js

const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

/**
 * Cifra de César — codifica
 * @param {string} text — texto original
 * @param {number} shift — deslocamento
 * @returns {string} — texto cifrado
 */
export function caesarEncrypt(text, shift) {
  return text
    .toUpperCase()
    .split('')
    .map(char => {
      const idx = ALPHABET.indexOf(char);
      if (idx === -1) return char;
      return ALPHABET[(idx + shift) % 26];
    })
    .join('');
}

/**
 * Cifra de César — decodifica
 * @param {string} text — texto cifrado
 * @param {number} shift — deslocamento usado na cifragem
 * @returns {string} — texto original
 */
export function caesarDecrypt(text, shift) {
  return text
    .toUpperCase()
    .split('')
    .map(char => {
      const idx = ALPHABET.indexOf(char);
      if (idx === -1) return char;
      return ALPHABET[(idx - shift + 26) % 26];
    })
    .join('');
}

/**
 * Retorna o alfabeto completo
 */
export function getAlphabet() {
  return ALPHABET;
}

/**
 * Gera alfabeto deslocado
 * @param {number} shift — deslocamento
 * @returns {string[]}
 */
export function getShiftedAlphabet(shift) {
  return ALPHABET.split('').map((_, i) => ALPHABET[(i + shift) % 26]);
}

export default { caesarEncrypt, caesarDecrypt, getAlphabet, getShiftedAlphabet };

