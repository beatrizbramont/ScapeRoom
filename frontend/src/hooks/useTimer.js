
// 📁 Pasta: frontend/src/hooks/useTimer.js
// Hook para formatação e status do timer

import { useMemo } from 'react';

export function useTimer(timeRemaining) {
  const formatted = useMemo(() => {
    const total = Math.max(0, Math.floor(timeRemaining));
    const minutes = Math.floor(total / 60);
    const seconds = total % 60;
    return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  }, [timeRemaining]);

  const status = useMemo(() => {
    if (timeRemaining <= 120) return 'critical';    // 2 min
    if (timeRemaining <= 300) return 'warning';     // 5 min
    return 'normal';
  }, [timeRemaining]);

  const isLowTime = status !== 'normal';
  const percentage = Math.max(0, (timeRemaining / 1800) * 100);

  return { formatted, status, isLowTime, percentage };
}

export default useTimer;

