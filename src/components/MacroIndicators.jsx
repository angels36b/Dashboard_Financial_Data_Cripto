import { useState, useEffect } from 'react';

const MacroIndicators = () => {
  const [indicators, setIndicators] = useState([]);

  useEffect(() => {
    const fetchMacro = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/macro');
        const result = await response.json();
        if (result.status === "success") {
          setIndicators(result.data);
        }
      } catch (error) {
        console.error("Error conectando a la API macro:", error);
      }
    };
    fetchMacro();
  }, []);

  return (
    <section className="indicators-row">
      {indicators.map((ind, index) => {
        // Lógica condicional para inyectar colores SMC
        const isPositive = ind.surprise > 0;
        const isNegative = ind.surprise < 0;
        const surpriseClass = isPositive ? 'surprise-positive' : isNegative ? 'surprise-negative' : 'surprise-neutral';
        const surpriseSign = isPositive ? '+' : '';

        return (
          <div key={index} className="panel indicator-panel dynamic-indicator">
            <div className="indicator-header">
              <span className="indicator-title">{ind.indicator_name}</span>
              <span className="indicator-time">{ind.updated_at.split(' ')[1]}</span>
            </div>
            
            <h2 className="actual-value">{ind.actual_value}</h2>
            
            <div className="macro-details">
              <span className="forecast-text">Prev: {ind.forecast_value}</span>
              <span className={`surprise-text ${surpriseClass}`}>
                {surpriseSign}{ind.surprise} {isPositive ? '🔼' : isNegative ? '🔽' : '➖'}
              </span>
            </div>
          </div>
        );
      })}
    </section>
  );
};

export default MacroIndicators;