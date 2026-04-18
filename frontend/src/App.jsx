import { useState } from 'react';
import './index.css';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [toastMsg, setToastMsg] = useState(null);

  const showToast = (msg) => {
    setToastMsg(msg);
    setTimeout(() => setToastMsg(null), 3000);
  };

  const handleAnalyze = async () => {
    if (!text.trim() || text.length < 2) {
      showToast("Please enter at least 2 characters.");
      return;
    }
    
    setLoading(true);
    setResult(null);

    try {
      // Simulate a small delay for the thoughtful UI effect
      await new Promise(r => setTimeout(r, 400));

      const response = await fetch('http://localhost:8080/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `API Error: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      showToast(err.message || 'API Connection Failed. Please check if the server is running.');
    } finally {
      setLoading(false);
    }
  };

  const StatusClass = result 
    ? `status-${result.sentiment.toLowerCase()}`
    : '';

  return (
    <>
      <div className={`toast-notification ${toastMsg ? 'show' : ''}`}>
        {toastMsg}
      </div>

      <div className="mesh-bg"></div>

      <nav className="navbar">
        <div className="logo">
          <div className="logo-dot"></div>
          Sentiment Studio
        </div>
      </nav>

      <div className="main-wrapper">
        <div className="app-card">
          
          <div className="hero-text">
            <h1>Analyze Context & Tone</h1>
            <p>Harness our machine learning model to uncover the underlying sentiment of any textual data.</p>
          </div>

          <div className="input-group">
            <textarea 
              className="custom-textarea" 
              placeholder="Paste or type your review, tweet, or feedback here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={(e) => {
                if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
                  handleAnalyze();
                }
              }}
            />
          </div>

          <button 
            className="btn-analyze" 
            onClick={handleAnalyze} 
            disabled={loading}
          >
            {!loading && <span>Run Analysis</span>}
            {loading && (
              <div className="loader-dots">
                <div></div><div></div><div></div>
              </div>
            )}
          </button>

          <div className={`result-box ${result ? 'active' : ''} ${StatusClass}`}>
            {result && (
              <div className="result-inner">
                <div className="result-glow"></div>
                <div className="badge">{result.sentiment.toUpperCase()}</div>
                
                <div style={{ display: 'flex', justifyContent: 'space-around', marginTop: '10px' }}>
                  <div>
                    <p className="metric-label">Confidence Score</p>
                    <p className="metric-value">{(result.confidence).toFixed(1)}%</p>
                  </div>
                  <div>
                    <p className="metric-label">Latency</p>
                    <p className="metric-value">{(result.latency_ms)}ms</p>
                  </div>
                </div>
              </div>
            )}
          </div>

        </div>
      </div>

      <div className="footer">
        Powered by FastAPI & HuggingFace Transformers
      </div>
    </>
  );
}

export default App;
