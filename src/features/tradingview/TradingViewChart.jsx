// src/features/tradingview/TradingViewChart.jsx
import React, { useEffect, useRef, memo } from 'react';

const TradingViewChart = () => {
  const container = useRef();

  useEffect(() => {
    // 1. Clean up any existing chart to prevent duplicates on hot-reload
    if (container.current) {
      container.current.innerHTML = '';
    }

    // 2. Create the official TradingView script element
    const script = document.createElement("script");
    script.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
    script.type = "text/javascript";
    script.async = true;
    
    // 3. Inject the configuration JSON exactly as TradingView requires it
    script.innerHTML = `
      {
        "autosize": true,
        "symbol": "BINANCE:SOLUSDT",
        "interval": "60",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "enable_publishing": false,
        "backgroundColor": "#1E222D",
        "gridColor": "#2A2E39",
        "hide_top_toolbar": false,
        "hide_legend": false,
        "save_image": false,
        "container_id": "tradingview_solana",
        "support_host": "https://www.tradingview.com"
      }`;
      
    // 4. Append the script to our container
    container.current.appendChild(script);

    // Cleanup function
    return () => {
      if (container.current) {
        container.current.innerHTML = '';
      }
    };
  }, []); // Empty array ensures this only runs once on mount

  return (
    // We use a relative wrapper to force the chart to respect the panel size
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <div 
        className="tradingview-widget-container" 
        ref={container} 
        style={{ height: "100%", width: "100%" }}
      >
        <div className="tradingview-widget-container__widget" style={{ height: "100%", width: "100%" }}></div>
      </div>
    </div>
  );
};

// React.memo prevents the component from re-rendering unnecessarily
export default memo(TradingViewChart);