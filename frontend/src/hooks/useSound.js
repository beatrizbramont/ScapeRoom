
// 📁 Pasta: frontend/src/hooks/useSound.js
// Hook para efeitos sonoros (opcional — funciona mesmo sem arquivos de áudio)

import { useCallback, useRef } from 'react';

export function useSound() {
  const audioRef = useRef(null);

  const play = useCallback((soundName) => {
    try {
      const soundMap = {
        click: '/assets/sounds/click.mp3',
        correct: '/assets/sounds/correct.mp3',
        wrong: '/assets/sounds/wrong.mp3',
        hint: '/assets/sounds/hint.mp3',
        victory: '/assets/sounds/victory.mp3',
        gameover: '/assets/sounds/gameover.mp3'
      };

      const src = soundMap[soundName];
      if (!src) return;

      if (audioRef.current) {
        audioRef.current.pause();
      }

      audioRef.current = new Audio(src);
      audioRef.current.volume = 0.5;
      audioRef.current.play().catch(() => {
        // Silencia erro caso o arquivo não exista
      });
    } catch {
      // Sons são opcionais
    }
  }, []);

  const stop = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
  }, []);

  return { play, stop };
}

export default useSound;

