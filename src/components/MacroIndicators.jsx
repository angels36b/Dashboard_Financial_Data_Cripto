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
        // 1. ESCUDO DEFENSIVO: Si la variable viene nula, asignamos un valor por defecto
        const status = ind.status || "Actual";
        const surprise = ind.surprise || 0;
        const actualValue = ind.actual_value || "N/A";
        const forecastValue = ind.forecast_value || "N/A";
        const eventDate = ind.event_date || "";
        const indicatorName = ind.indicator_name || "Dato Desconocido";

        // 2. LÓGICA DE ESTADOS
        const isPrevious = status === "Anterior";
        
        const isPositive = !isPrevious && surprise > 0;
        const isNegative = !isPrevious && surprise < 0;
        
        const surpriseClass = isPositive ? 'surprise-positive' : isNegative ? 'surprise-negative' : 'surprise-neutral';
        const surpriseSign = isPositive ? '+' : '';

        return (
          <div key={index} className="panel indicator-panel dynamic-indicator">
            <div className="indicator-header">
              <span className="indicator-title">{indicatorName}</span>
              <span className="indicator-time">{eventDate}</span>
            </div>
            
            <div className="value-container">
               <h2 className={`actual-value ${isPrevious ? 'value-faded' : ''}`}>
                 {actualValue}
               </h2>
               {isPrevious && <span className="status-badge">Dato Anterior</span>}
            </div>
            
            <div className="macro-details">
              <span className="forecast-text">Prev: {forecastValue}</span>
              <span className={`surprise-text ${surpriseClass}`}>
                {surpriseSign}{surprise} {isPositive ? '🔼' : isNegative ? '🔽' : '➖'}
              </span>
            </div>
          </div>
        );
      })}
    </section>
  );
};

export default MacroIndicators;