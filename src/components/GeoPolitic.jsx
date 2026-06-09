// src/components/GeopoliticalPanel.jsx
import { useState, useEffect } from 'react';

const GeopoliticalPanel = () => {
  // Component's exclusive memory
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  // Autonomous network logic
  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/news');
        const result = await response.json();
        console.log("🔴 DATOS RECIBIDOS DE PYTHON:", result);

        if (result.status === "success") {
          setNews(result.data);
        }
      } catch (error) {
        console.error("Error connecting to the API:", error);
        console.error("🔴 ERROR DE CONEXIÓN:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, []);

  // Visual rendering
  return (
    <section className="panel geopolitical-panel">
      <h2>Geopolitical Analysis</h2>
      
      {loading ? (
        <div className="loader">📡 Synchronizing data...</div>
      ) : (
        <div className="news-feed">
          {news.map((item, index) => (
            <div key={index} className="news-card">
              <span className="impact-indicator">
                {item.impact === 'high' ? '🔴' : item.impact === 'medium' ? '🟡' : '🔵'}
              </span>
              <span className="source-badge"> [{item.source}] </span>
              <p className="headline">{item.headline}</p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default GeopoliticalPanel;