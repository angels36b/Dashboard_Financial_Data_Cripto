import React from 'react';
import './App.css';
import TradingViewChart from './features/tradingview/TradingViewChart';
import TradingChart from './components/TradingChart';
import GeopoliticalPanel from './components/GeoPolitic';



function App() {
  return (
    <div className="dashboard-container">
      {/* MAIN HEADER */}
      <header className="top-bar">
        <div className="status">🟢 Data Agent: Online</div>
        <div className="tickers">DXY: 104.50 &nbsp;|&nbsp; BTC: $64,200 &nbsp;|&nbsp; SOL: $145.30</div>
      </header>

      {/* SCROLLABLE CONTENT AREA */}
      <main className="main-layout">
        
        {/* ROW 1: CHART WINDOWS (50/50 en PC, 1 columna en móvil) */}
        <section className="charts-row">
          <div className="panel chart-panel">
            {/* The chart fills the entire panel without margins */}
           
            <div className="panel-header">📊 Market Chart</div>           
               <TradingViewChart />
          </div>

          <div className="panel chart-panel">
            <div className="panel-header">📈 Solana ML Prediction (Python)</div>
            <p style={{ padding: '16px' }}>Predictive Chart Placeholder</p>
          </div>
        </section>

        {/* ROW 2: LLM WINDOW (Fila independiente, 100% ancho) */}
        <section className="full-width-row">
          <div className="panel text-panel">
            <div className="panel-header">🧠 LLM Market Sentiment</div>
            <div className="panel-content">
              <p>Sentiment analysis data will appear here...</p>
            </div>
          </div>
        </section>

        {/* ROW 3: GEOPOLITICAL (Fila independiente, 100% ancho) */}
        <section className="full-width-row">
          <div className="panel text-panel">
            <div className="panel-header">📊 News dayli</div> 
            <GeopoliticalPanel />
          </div>
        </section>

        {/* ROW 4: MACRO INDICATORS AND WHALES (Auto-ajustable) */}
        <section className="indicators-row">
          <div className="panel indicator-panel">
            <div className="panel-header">CPI</div>
            <h2>3.4%</h2>
          </div>
          <div className="panel indicator-panel">
            <div className="panel-header">FOMC</div>
            <h2>5.25%</h2>
          </div>
          <div className="panel indicator-panel">
            <div className="panel-header">NFP</div>
            <h2>175K</h2>
          </div>
          <div className="panel indicator-panel">
            <div className="panel-header">ISM / ADP</div>
            <h2>49.2</h2>
          </div>
          <div className="panel indicator-panel">
            <div className="panel-header">Whale Flow</div>
            <h2 style={{ color: '#34D399' }}>+1,200 BTC</h2>
          </div>
        </section>

      </main>
    </div>
  );
}


export default App;