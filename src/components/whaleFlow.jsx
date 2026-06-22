import { useState, useEffect } from 'react';

const WhaleFlow = () => {
  const [whales, setWhales] = useState([]);

  useEffect(() => {
    const fetchWhales = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/whales');
        const result = await response.json();
        if (result.status === "success") {
          setWhales(result.data);
        }
      } catch (error) {
        console.error("Error conectando a la API de ballenas:", error);
      }
    };

    // Llamada inicial
    fetchWhales();

    // 🔴 EL LATIDO INSTITUCIONAL: Actualiza silenciosamente cada 10 segundos
    const interval = setInterval(fetchWhales, 10000);
    
    // Limpieza al desmontar el componente
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="panel whale-panel">
      <h3 className="panel-title"> Institutional Order Flow</h3>
      
      <div className="whale-list">
        {whales.map((whale, index) => {
          // 1. ESCUDO DEFENSIVO: Valores por defecto si la base de datos está vacía
          const direction = whale.direction || "Transfer";
          const amount = whale.amount || 0;
          const exchange = whale.exchange || "Desconocido";
          const timestamp = whale.timestamp || "00:00:00";

          // 2. LÓGICA DE DIRECCIÓN (Smart Money Concepts)
          let directionClass = "dir-neutral";
          let directionIcon = "⚪";

          if (direction.toLowerCase() === "long") {
            directionClass = "dir-long";
            directionIcon = "🟢";
          } else if (direction.toLowerCase() === "short") {
            directionClass = "dir-short";
            directionIcon = "🔴";
          }

          return (
            <div key={index} className={`whale-item ${directionClass}`}>
              <div className="whale-left">
                <span className="whale-icon">{directionIcon}</span>
                <div className="whale-details">
                  <span className="whale-type">{direction.toUpperCase()}</span>
                  <span className="whale-exchange">{exchange}</span>
                </div>
              </div>
              
              <div className="whale-right">
                <span className="whale-amount">{amount.toFixed(2)} BTC</span>
                <span className="whale-time">{timestamp.split(' ')[1] || timestamp}</span>
              </div>
            </div>
          );
        })}

        {whales.length === 0 && (
          <div className="empty-state" style={{ textAlign: 'center', color: '#787B86', padding: '20px' }}>
            ⏳ Escaneando la Mempool en busca de liquidez institucional...
          </div>
        )}
      </div>
    </div>
  );
};

export default WhaleFlow;