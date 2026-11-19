
// 📁 Pasta: frontend/src/components/shared/Snowflakes.jsx
import React, { useMemo } from 'react';

function Snowflakes({ count = 20 }) {
  const flakes = useMemo(() =>
    Array.from({ length: count }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      delay: Math.random() * 5,
      duration: 3 + Math.random() * 4,
      size: 10 + Math.random() * 10
    })),
    [count]
  );

  return (
    <div className="snowflakes" aria-hidden="true">
      {flakes.map(flake => (
        <div
          key={flake.id}
          className="snowflake"
          style={{
            left: `${flake.left}%`,
            animationDelay: `${flake.delay}s`,
            animationDuration: `${flake.duration}s`,
            fontSize: `${flake.size}px`
          }}
        >
          ❄
        </div>
      ))}
    </div>
  );
}

export default Snowflakes;

