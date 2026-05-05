import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import CompanyDetail from './pages/CompanyDetail'
import SectorAnalytics from './pages/SectorAnalytics'

import axios from 'axios'

function App() {
  const handleConnectData = async () => {
    const btn = document.getElementById('connect-btn')
    if (btn) btn.innerText = 'Syncing...'
    
    try {
      await axios.post('http://localhost:8000/api/v1/ingest/trigger/')
      alert('Data pipeline executed successfully! Markets are now updated.')
      window.location.reload()
    } catch (err) {
      console.error(err)
      alert('Failed to connect to data source. Check backend logs.')
    } finally {
      if (btn) btn.innerText = 'Connect Data'
    }
  }

  return (
    <Router>
      <div className="app-container">
        <nav className="navbar">
          <div className="logo">
            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              FIN<span className="gradient-text">VEDA</span>
            </Link>
          </div>
          <div className="nav-links" style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
            <Link to="/" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>Markets</Link>
            <Link to="/sectors" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>Screener</Link>
            <button id="connect-btn" className="btn-primary" onClick={handleConnectData}>Connect Data</button>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/company/:symbol" element={<CompanyDetail />} />
          <Route path="/sectors" element={<SectorAnalytics />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
