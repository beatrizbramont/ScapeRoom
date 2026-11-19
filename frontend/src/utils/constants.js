
// 📁 Pasta: frontend/src/utils/constants.js

// ─── Configurações do jogo ───
export const GAME_DURATION = 1800; // 30 minutos
export const HINT_PENALTY = 120;   // 2 minutos
export const TOTAL_PHASES = 4;

// ─── Cores do Fase 3 (Genius) ───
export const LIGHT_COLORS = [
  { id: 'vermelho', name: 'Vermelho', hex: '#e74c3c', glow: '#ff6b6b' },
  { id: 'verde',    name: 'Verde',    hex: '#27ae60', glow: '#6bff6b' },
  { id: 'azul',     name: 'Azul',     hex: '#2980b9', glow: '#6bb5ff' },
  { id: 'amarelo',  name: 'Amarelo',  hex: '#f1c40f', glow: '#ffe66b' }
];

// ─── Objetos da Fase 1 ───
export const PHASE1_OBJECTS = [
  { id: 'relogio',  name: 'Relógio',  emoji: '🕛', isClue: true  },
  { id: 'carta',    name: 'Carta',    emoji: '✉️',  isClue: true  },
  { id: 'cookie',   name: 'Cookie',   emoji: '🍪', isClue: true  },
  { id: 'estrela',  name: 'Estrela',  emoji: '⭐', isClue: false },
  { id: 'meia',     name: 'Meia',     emoji: '🧦', isClue: false },
  { id: 'presente', name: 'Presente', emoji: '🎁', isClue: false }
];

// ─── Pesos da Fase 4 ───
export const PHASE4_WEIGHTS = [
  { kg: 5,  emoji: '🎁', label: 'Caixinha de Música' },
  { kg: 10, emoji: '📦', label: 'Caixa de Brinquedos' },
  { kg: 15, emoji: '🎀', label: 'Urso de Pelúcia' },
  { kg: 20, emoji: '🧸', label: 'Kit de Jogos' },
  { kg: 25, emoji: '🎄', label: 'Árvore Decorativa' },
  { kg: 30, emoji: '⛄', label: 'Boneco de Neve' },
  { kg: 35, emoji: '🦌', label: 'Rena Mecânica' },
  { kg: 40, emoji: '🛷', label: 'Mini Trenó' }
];

export const SLEIGH_TARGET = 100;

// ─── Símbolos natalinos (Fase 2) ───
export const CHRISTMAS_SYMBOLS = {
  U: '🎄', H: '⛄', Q: '🔔', D: '🦌',
  R: '🎅', E: '🎁', N: '❄️', A: '⭐'
};

// ─── Nomes das fases ───
export const PHASE_NAMES = [
  'Mapa Estelar',
  'Lista Criptografada',
  'Sequência de Luzes',
  'Peso do Trenó'
];

export const PHASE_ICONS = ['⭐', '📜', '💡', '⚖️'];

