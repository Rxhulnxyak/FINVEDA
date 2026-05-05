import { useEffect, useState } from 'react'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { ArrowLeft, PieChart } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function SectorAnalytics() {
  const [sectors, setSectors] = useState<any[]>([])
  const [selectedSector, setSelectedSector] = useState<any>(null)
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    axios.get('http://localhost:8000/api/v1/sectors/').then(res => {
      setSectors(res.data)
      setLoading(false)
    })
  }, [])

  useEffect(() => {
    if (selectedSector) {
      axios.get(`http://localhost:8000/api/v1/sectors/${selectedSector.id}/stats/`).then(res => {
        setStats(res.data)
      })
    }
  }, [selectedSector])

  if (loading) return <div style={{ padding: '100px', textAlign: 'center' }}>Loading sector metrics...</div>

  return (
    <div className="sector-container" style={{ padding: '40px', maxWidth: '1400px', margin: '0 auto' }}>
      <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)', textDecoration: 'none', marginBottom: '32px' }}>
        <ArrowLeft size={20} /> Back to Markets
      </Link>

      <header style={{ marginBottom: '48px' }}>
        <h1 style={{ fontSize: '32px', marginBottom: '16px' }}>Sector <span className="gradient-text">Intelligence</span></h1>
        <p style={{ color: 'var(--text-muted)', marginBottom: '24px' }}>Analyze and compare company performance across industry sectors.</p>
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          {sectors.map(s => (
            <button 
              key={s.id} 
              onClick={() => setSelectedSector(s)}
              className={selectedSector?.id === s.id ? 'active-sector' : ''}
              style={{ 
                padding: '10px 24px', 
                borderRadius: '30px', 
                border: '1px solid var(--border)', 
                background: selectedSector?.id === s.id ? 'var(--primary)' : 'rgba(255,255,255,0.05)',
                color: selectedSector?.id === s.id ? 'black' : 'white',
                cursor: 'pointer',
                fontWeight: 'bold',
                transition: 'all 0.3s ease'
              }}
            >
              {s.sector_name}
            </button>
          ))}
        </div>
      </header>

      {stats && stats.companies?.length > 0 ? (
        <div className="stats-layout" style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '32px' }}>
          <div className="summary-cards" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div className="glass-card">
              <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginBottom: '8px' }}>Average Sector Score</p>
              <h2 style={{ fontSize: '36px', color: 'var(--primary)' }}>{stats.avg_overall_score}</h2>
            </div>
            <div className="glass-card">
              <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginBottom: '8px' }}>Top Performance</p>
              <h2 style={{ fontSize: '36px', color: '#10B981' }}>{stats.max_overall_score}</h2>
            </div>
            <div className="glass-card">
              <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginBottom: '8px' }}>Company Concentration</p>
              <h2 style={{ fontSize: '36px' }}>{stats.company_count}</h2>
            </div>
          </div>

          <div className="chart-section glass-card">
            <h3 style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <PieChart size={20} color="var(--primary)" /> {stats.sector_name} Peer Comparison
            </h3>
            <div style={{ height: '400px', width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stats.companies}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                  <XAxis dataKey="symbol" stroke="var(--text-muted)" />
                  <YAxis stroke="var(--text-muted)" />
                  <Tooltip 
                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                    contentStyle={{ background: 'rgba(20,20,20,0.9)', border: '1px solid var(--border)', borderRadius: '8px' }}
                  />
                  <Bar dataKey="score" radius={[4, 4, 0, 0]}>
                    {stats.companies.map((entry: any, index: number) => (
                      <Cell key={`cell-${index}`} fill={entry.score >= stats.avg_overall_score ? 'var(--primary)' : 'rgba(255,255,255,0.2)'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      ) : (
        <div style={{ textAlign: 'center', padding: '100px', opacity: 0.5 }}>
          Select a sector to view comparative analytics.
        </div>
      )}
    </div>
  )
}
