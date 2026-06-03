import React from 'react';
import './App.css';
import TradingViewChart from './features/tradingview/TradingViewChart';
import TradingChart from './components/TradingChart';

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
        
        {/* ROW 1: CHART WINDOWS */}
        <section className="charts-row">
          <div className="panel" style={{ padding: 0 }}>
            {/* The chart fills the entire panel without margins */}
            <TradingViewChart />
          </div>
          <div className="panel">
            <div className="panel-header">📈 Solana ML Prediction (Python)</div>
            <p>Predictive Chart Placeholder</p>
          </div>
        </section>

        {/* ROW 2: LLM WINDOWS (NEWS) */}
        <section className="llm-news-row">
          <div className="panel" style={{ justifyContent: 'flex-start' }}>
            <div className="panel-header">🧠 LLM Market Sentiment</div>
            <p>Sentiment analysis data will appear here...</p>
          </div>
          <div className="panel" style={{ justifyContent: 'flex-start' }}>
            <div className="panel-header">🌍 Geopolitical & Macro Events</div>
            <p>Political comments and alerts will appear here...</p>
          </div>
        </section>

        {/* ROW 3: MACRO INDICATORS AND WHALES */}
        <section className="indicators-row">
          <div className="panel" style={{ minHeight: '150px' }}>
            <div className="panel-header">CPI</div>
            <h2>3.4%</h2>
          </div>
          <div className="panel" style={{ minHeight: '150px' }}>
            <div className="panel-header">FOMC</div>
            <h2>5.25%</h2>
          </div>
          <div className="panel" style={{ minHeight: '150px' }}>
            <div className="panel-header">NFP</div>
            <h2>175K</h2>
          </div>
          <div className="panel" style={{ minHeight: '150px' }}>
            <div className="panel-header">ISM / ADP</div>
            <h2>49.2</h2>
          </div>
          <div className="panel" style={{ minHeight: '150px' }}>
            <div className="panel-header">Whale Flow</div>
            <h2 style={{ color: '#34D399' }}>+1,200 BTC</h2>
          </div>
        </section>

      </main>
    </div>
  );
}

export default App;