export default function Header({ model }) {
  return (
    <header style={{
      padding: '24px 40px 0',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{
          width: 36, height: 36, borderRadius: 10,
          background: 'linear-gradient(135deg, #7c6aff, #a78bfa)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 18,
        }}>
          T
        </div>
        <div>
          <div style={{ fontWeight: 600, fontSize: 16, color: '#fff', letterSpacing: '-0.3px' }}>
            Tone Rewriter
          </div>
          <div style={{ fontSize: 12, color: 'var(--text-dim)', marginTop: 1 }}>
            100% local - no data leaves your machine
          </div>
        </div>
      </div>

      {model && (
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8,
          background: 'var(--surface)', border: '1px solid var(--border)',
          borderRadius: 20, padding: '6px 14px',
        }}>
          <div style={{
            width: 7, height: 7, borderRadius: '50%',
            background: 'var(--green)',
            boxShadow: '0 0 6px var(--green)',
          }} />
          <span style={{ fontSize: 12, fontFamily: 'var(--mono)', color: 'var(--text-dim)' }}>
            {model}
          </span>
        </div>
      )}
    </header>
  )
}
