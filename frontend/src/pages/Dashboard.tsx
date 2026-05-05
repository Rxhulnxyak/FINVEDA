import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Search } from 'lucide-react'
import { getCompanies } from '../services/api'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const [companies, setCompanies] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    getCompanies().then(data => {
      setCompanies(data.results || data)
      setLoading(false)
    }).catch(err => {
      console.error(err)
      setLoading(false)
    })
  }, [])

  const filteredCompanies = companies.filter(c => 
    c.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.company_name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="dashboard-container">
      <section className="hero-section">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="hero-title">
            Financial Intelligence <br /> 
            <span className="gradient-text">Operating System</span>
          </h1>
          <p className="hero-subtitle">
            Experience Bloomberg-grade analytics for India's Nifty 100. 
            Real-time insights, ML-driven health scores, and automated ETL pipelines.
          </p>
          
          <div className="search-container" style={{ position: 'relative', width: '100%', maxWidth: '600px', margin: '0 auto' }}>
            <input 
              type="text" 
              placeholder="Search companies (TCS, HDFCBANK, INFY...)" 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                width: '100%',
                padding: '20px 60px',
                borderRadius: '12px',
                border: '1px solid var(--border)',
                background: 'rgba(255,255,255,0.05)',
                color: 'white',
                fontSize: '18px',
                outline: 'none'
              }}
            />
            <Search style={{ position: 'absolute', left: '20px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          </div>
        </motion.div>

        <div className="companies-section" style={{ marginTop: '100px', width: '100%', maxWidth: '1200px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '32px' }}>
            <h2 style={{ textAlign: 'left' }}>Market Overview</h2>
            <p style={{ color: 'var(--text-muted)' }}>Showing {filteredCompanies.length} entities</p>
          </div>
          
          {loading ? (
            <p>Analyzing financial markets...</p>
          ) : (
            <div className="companies-grid" style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', 
              gap: '24px'
            }}>
              {filteredCompanies.map((company) => (
                <CompanyCard key={company.symbol} company={company} />
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  )
}

function CompanyCard({ company }: { company: any }) {
  const score = company.latest_score?.overall_score || 0
  const label = company.latest_score?.health_label?.label_name || 'PENDING'
  const color = company.latest_score?.health_label?.color_hex || 'var(--text-muted)'

  return (
    <motion.div 
      className="glass-card"
      whileHover={{ scale: 1.02 }}
      style={{ textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '16px' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ 
          height: '40px', 
          width: '40px', 
          background: 'white', 
          borderRadius: '8px', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center', 
          padding: '4px',
          overflow: 'hidden'
        }}>
          <img src={company.company_logo} alt={company.symbol} style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }} />
        </div>
        <div style={{ 
          padding: '4px 12px', 
          borderRadius: '20px', 
          fontSize: '12px', 
          fontWeight: 'bold',
          background: `${color}20`,
          color: color,
          border: `1px solid ${color}40`
        }}>
          {label}
        </div>
      </div>
      
      <div>
        <h3 style={{ fontSize: '18px', marginBottom: '4px' }}>{company.company_name}</h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '14px' }}>{company.symbol} • {company.sector?.sector_name || 'Sector'}</p>
      </div>

      <div style={{ display: 'flex', gap: '20px', marginTop: 'auto', marginBottom: '10px' }}>
        <div>
          <p style={{ fontSize: '10px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Health Score</p>
          <p style={{ fontSize: '18px', fontWeight: 'bold', color: color }}>{score.toFixed(1)}</p>
        </div>
        <div>
          <p style={{ fontSize: '10px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Book Value</p>
          <p style={{ fontSize: '18px', fontWeight: 'bold' }}>₹{company.book_value || '—'}</p>
        </div>
      </div>

      <Link 
        to={`/company/${company.symbol}`}
        className="btn-primary" 
        style={{ 
          textDecoration: 'none', 
          textAlign: 'center', 
          background: 'transparent', 
          border: '1px solid var(--border)',
          fontSize: '14px'
        }}
      >
        View Intelligence
      </Link>
    </motion.div>
  )
}
