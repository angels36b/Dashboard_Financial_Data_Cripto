import React from 'react';
import './App.css';
import TradingViewChart from './features/tradingview/TradingViewChart';
import TradingChart from './components/TradingChart';
import GeopoliticalPanel from './components/GeoPolitic';
import MacroIndicators from './components/MacroIndicators';
import WhaleFlow from './components/whaleFlow';


function App() {
  return (
    <div className="dashboard-container">
      {/* MAIN HEADER */}
      <header className="top-bar">
        <div className="status">Economic Analisis</div>
        <div className="tickers"> You have the power</div>
      </header>

      {/* SCROLLABLE CONTENT AREA */}
      <main className="main-layout">
        
        {/* ROW 1: CHART WINDOWS (50/50 en PC, 1 columna en móvil) */}
        <section className="charts-row">
          <div className="panel chart-panel">
            {/* The chart fills the entire panel without margins */}
           
            <div className="panel-header"> Market Chart</div>           
               <TradingViewChart />
          </div>

          <div className="panel chart-panel">
            <div className="panel-header">Solana ML Prediction (Python)</div>
            <p style={{ padding: '16px' }}>Predictive Chart Placeholder</p>
          </div>
        </section>

        {/* ROW 2: LLM WINDOW (Fila independiente, 100% ancho) */}
        <section className="full-width-row">
          <div className="panel text-panel">
            <div className="panel-header"> LLM Market Sentiment</div>
            <div className="panel-content">
              <p>Sentiment analysis data will appear here...</p>
            </div>
          </div>
        </section>

        {/* ROW 3: GEOPOLITICAL (Fila independiente, 100% ancho) */}
        <section className="full-width-row">
          <div className="panel text-panel">
            <div className="panel-header"> News dayli</div> 
            <GeopoliticalPanel />
          </div>
        </section>

        {/*Macro indicators dinamicos*/}
        <MacroIndicators />
         {/*Row 5: Institutional order Flow (Whales)*/}
        
        {/*Institutional Order Flow*/}
        <section className="full-width-row" style={{marginTop: '20px'}}>
          <div className = "panel text-panel">
            <div className="panel-header"> Institutional Order Flow (Whales) </div>
            <WhaleFlow/>
          </div>
        </section>

      </main>
    </div>
  );
}


export default App;