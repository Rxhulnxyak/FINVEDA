import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowLeft, TrendingUp, Shield, BarChart3, Info } from 'lucide-react'
import { getCompanyDetail } from '../services/api'
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, RadarChart, PolarGrid, PolarAngleAxis, Radar } from 'recharts'

export default function CompanyDetail() {
  const { symbol } = useParams<{ symbol: string }>()
  const [company, setCompany] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (symbol) {
      getCompanyDetail(symbol).then(data => {
        setCompany(data)
        setLoading(false)
      }).catch(err => {
        console.error(err)
        setLoading(false)
      })
    }
  }, [symbol])

  if (loading) return <div style={{ padding: '100px', textAlign: 'center' }}>Analysing {symbol} intelligence...</div>
  if (!company) return <div style={{ padding: '100px', textAlign: 'center' }}>Company not found.</div>

  const plData = [...company.profit_loss].sort((a, b) => a.year_label.localeCompare(b.year_label))
  const score = company.latest_score || {}
  const color = score.health_label?.color_hex || 'var(--primary)'

  return (
    <div className="detail-container" style={{ padding: '40px', maxWidth: '1400px', margin: '0 auto' }}>
      <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)', textDecoration: 'none', marginBottom: '32px' }}>
        <ArrowLeft size={20} /> Back to Markets
      </Link>

      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '48px' }}>
        <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
          <div style={{ 
            height: '64px', 
            width: '64px', 
            background: 'white', 
            borderRadius: '12px', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center', 
            padding: '8px'
          }}>
            <img src={company.company_logo} alt={company.symbol} style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }} />
          </div>
          <div>
            <h1 style={{ fontSize: '32px', marginBottom: '4px' }}>{company.company_name}</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '18px' }}>{company.symbol} • {company.sector?.sector_name} • {company.sub_sector}</p>
          </div>
        </div>
        
        <div className="health-card" style={{ 
          background: 'rgba(255,255,255,0.03)', 
          border: `1px solid ${color}40`, 
          padding: '20px 32px', 
          borderRadius: '16px',
          textAlign: 'right'
        }}>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px' }}>Market Health Label</p>
          <h2 style={{ color: color, fontSize: '28px' }}>{score.health_label?.label_name}</h2>
          <p style={{ fontSize: '14px', marginTop: '4px' }}>Overall Score: <strong>{score.overall_score}</strong></p>
        </div>
      </header>

      <div className="grid-layout" style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '32px' }}>
        <div className="main-stats">
          <section className="glass-card" style={{ marginBottom: '32px', height: '400px' }}>
            <h3 style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <TrendingUp size={20} color="var(--primary)" /> Revenue & Profit Trends (INR Cr)
            </h3>
            <ResponsiveContainer width="100%" height="80%">
              <AreaChart data={plData}>
                <defs>
                  <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--primary)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                <XAxis dataKey="year_label" stroke="var(--text-muted)" fontSize={12} />
                <YAxis stroke="var(--text-muted)" fontSize={12} />
                <Tooltip 
                  contentStyle={{ background: 'rgba(20,20,20,0.9)', border: '1px solid var(--border)', borderRadius: '8px' }}
                  itemStyle={{ color: 'white' }}
                />
                <Area type="monotone" dataKey="sales" name="Revenue" stroke="var(--primary)" fillOpacity={1} fill="url(#colorSales)" />
                <Area type="monotone" dataKey="net_profit" name="Net Profit" stroke="#10B981" fillOpacity={0} />
              </AreaChart>
            </ResponsiveContainer>
          </section>

          <section className="glass-card">
            <h3 style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <BarChart3 size={20} color="var(--primary)" /> Profit & Loss Summary
            </h3>
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}>
                    <th style={{ padding: '12px', color: 'var(--text-muted)' }}>Year</th>
                    <th style={{ padding: '12px', color: 'var(--text-muted)' }}>Sales</th>
                    <th style={{ padding: '12px', color: 'var(--text-muted)' }}>Operating Profit</th>
                    <th style={{ padding: '12px', color: 'var(--text-muted)' }}>OPM %</th>
                    <th style={{ padding: '12px', color: 'var(--text-muted)' }}>Net Profit</th>
                  </tr>
                </thead>
                <tbody>
                  {plData.map((row: any, index: number) => {
                    const prevRow = index > 0 ? plData[index - 1] : null
                    const salesGrowth = prevRow ? ((row.sales - prevRow.sales) / prevRow.sales * 100).toFixed(1) : '—'
                    const profitGrowth = prevRow ? ((row.net_profit - prevRow.net_profit) / prevRow.net_profit * 100).toFixed(1) : '—'
                    
                    return (
                      <tr key={row.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                        <td style={{ padding: '12px', fontWeight: 'bold' }}>{row.year_label}</td>
                        <td style={{ padding: '12px' }}>
                          ₹{row.sales}
                          {salesGrowth !== '—' && (
                            <span style={{ fontSize: '10px', marginLeft: '8px', color: '#10B981' }}>↑{salesGrowth}%</span>
                          )}
                        </td>
                        <td style={{ padding: '12px' }}>₹{row.operating_profit}</td>
                        <td style={{ padding: '12px' }}>{row.opm_pct}%</td>
                        <td style={{ padding: '12px', color: '#10B981' }}>
                          ₹{row.net_profit}
                          {profitGrowth !== '—' && (
                            <span style={{ fontSize: '10px', marginLeft: '8px', color: '#10B981' }}>↑{profitGrowth}%</span>
                          )}
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </section>
        </div>

        <div className="sidebar">
          <section className="glass-card" style={{ marginBottom: '32px' }}>
            <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <TrendingUp size={20} color="var(--primary)" /> Growth Metrics (CAGR)
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div style={{ padding: '16px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--border)' }}>
                <p style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '4px' }}>Sales Growth (3Y)</p>
                <p style={{ fontSize: '20px', fontWeight: 'bold', color: (company.analysis?.[0]?.compounded_sales_growth_pct > 0 ? '#10B981' : 'var(--text-muted)') }}>
                  {company.analysis?.[0]?.compounded_sales_growth_pct ? `${company.analysis[0].compounded_sales_growth_pct}%` : 'N/A'}
                </p>
              </div>
              <div style={{ padding: '16px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--border)' }}>
                <p style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '4px' }}>Profit Growth (3Y)</p>
                <p style={{ fontSize: '20px', fontWeight: 'bold', color: (company.analysis?.[0]?.compounded_profit_growth_pct > 0 ? '#10B981' : 'var(--text-muted)') }}>
                  {company.analysis?.[0]?.compounded_profit_growth_pct ? `${company.analysis[0].compounded_profit_growth_pct}%` : 'N/A'}
                </p>
              </div>
              <div style={{ padding: '16px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--border)' }}>
                <p style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '4px' }}>Return on Equity</p>
                <p style={{ fontSize: '20px', fontWeight: 'bold' }}>{company.analysis?.[0]?.roe_pct || '0'}%</p>
              </div>
              <div style={{ padding: '16px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--border)' }}>
                <p style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '4px' }}>Price CAGR</p>
                <p style={{ fontSize: '20px', fontWeight: 'bold', color: 'var(--primary)' }}>{company.analysis?.[0]?.stock_price_cagr_pct || '0'}%</p>
              </div>
            </div>
          </section>

          <section className="glass-card" style={{ marginBottom: '32px' }}>
            <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <Shield size={20} color="var(--primary)" /> ML Score Analysis
            </h3>
            <div style={{ height: '300px', width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={[
                  { subject: 'Profit', A: score.profitability_score, fullMark: 100 },
                  { subject: 'Growth', A: score.growth_score, fullMark: 100 },
                  { subject: 'Leverage', A: score.leverage_score, fullMark: 100 },
                  { subject: 'Cash', A: score.cashflow_score, fullMark: 100 },
                  { subject: 'Dividend', A: score.dividend_score, fullMark: 100 },
                  { subject: 'Trend', A: score.trend_score, fullMark: 100 },
                ]}>
                  <PolarGrid stroke="rgba(255,255,255,0.1)" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: 'var(--text-muted)', fontSize: 10 }} />
                  <Radar
                    name="Score"
                    dataKey="A"
                    stroke={color}
                    fill={color}
                    fillOpacity={0.6}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '12px' }}>
              <ScoreMetric label="Profitability" value={score.profitability_score} color="#10B981" />
              <ScoreMetric label="Growth" value={score.growth_score} color="#3B82F6" />
              <ScoreMetric label="Leverage" value={score.leverage_score} color="#F59E0B" />
              <ScoreMetric label="Cash Flow" value={score.cashflow_score} color="#8B5CF6" />
            </div>
          </section>

          <section className="glass-card" style={{ marginBottom: '32px' }}>
            <h3 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <Shield size={20} color="var(--primary)" /> Intelligence Pros & Cons
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div>
                <p style={{ fontSize: '11px', color: '#10B981', fontWeight: 'bold', marginBottom: '12px', textTransform: 'uppercase', letterSpacing: '1px' }}>Pros</p>
                {company.pros_cons?.filter((pc: any) => pc.is_pro).map((pro: any) => (
                  <div key={pro.id} style={{ display: 'flex', gap: '12px', marginBottom: '10px', fontSize: '14px', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                    <span style={{ color: '#10B981', fontWeight: 'bold' }}>✓</span> {pro.text}
                  </div>
                ))}
              </div>
              <div style={{ borderTop: '1px solid var(--border)', paddingTop: '20px' }}>
                <p style={{ fontSize: '11px', color: '#EF4444', fontWeight: 'bold', marginBottom: '12px', textTransform: 'uppercase', letterSpacing: '1px' }}>Cons</p>
                {company.pros_cons?.filter((pc: any) => !pc.is_pro).map((con: any) => (
                  <div key={con.id} style={{ display: 'flex', gap: '12px', marginBottom: '10px', fontSize: '14px', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                    <span style={{ color: '#EF4444', fontWeight: 'bold' }}>✗</span> {con.text}
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section className="glass-card">
            <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <Info size={20} color="var(--primary)" /> About Company
            </h3>
            <p style={{ color: 'var(--text-muted)', lineHeight: '1.6', fontSize: '14px' }}>
              {company.about_company}
            </p>
            <div style={{ marginTop: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <a href={company.website} target="_blank" className="link" style={{ color: 'var(--primary)', textDecoration: 'none' }}>Official Website ↗</a>
              <a href={company.nse_url} target="_blank" className="link" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>NSE Profile ↗</a>
              <a href={company.bse_url} target="_blank" className="link" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>BSE Profile ↗</a>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}

function ScoreMetric({ label, value, color }: { label: string, value: number, color: string }) {
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ fontSize: '13px' }}>{label}</span>
        <span style={{ fontSize: '13px', fontWeight: 'bold' }}>{value?.toFixed(1)}%</span>
      </div>
      <div style={{ height: '6px', background: 'rgba(255,255,255,0.05)', borderRadius: '3px', overflow: 'hidden' }}>
        <motion.div 
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 1 }}
          style={{ height: '100%', background: color }}
        />
      </div>
    </div>
  )
}
