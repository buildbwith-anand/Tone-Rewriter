import { useEffect, useRef } from 'react'

export default function OutputPanel({ text, streaming, toneName }) {
  const ref = useRef(null)

  useEffect(() => {
    if (ref.current) ref.current.scrollTop = ref.current.scrollHeight
  }, [text])

  const isEmpty = !text && !streaming

  return (
    <div style={{
      background: 'var(--surface)',
      border: `1px solid ${streaming ? 'var(--accent)' : 'var(--border)'}`,
      borderRadius: 'var(--radius)',
      display: 'flex',
      flexDirection: 'column',
      flex: 1,
      overflow: 'hidden',
      transition: 'border-color 0.2s ease',
      boxShadow: streaming ? '0 0 24px var(--accent-glow)' : 'none',
    }}>
      {/* Panel header */}
      <div style={{
        padding: '14px 20px',
        borderBottom: '1px solid var(--border)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexShrink: 0,
      }}>
        <span style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-dim)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
          Output
        </span>
        {toneName && (
          <span style={{
            fontSize: 11, padding: '3px 10px',
            borderRadius: 20,
            background: 'var(--accent-glow)',
            border: '1px solid var(--accent-dim)',
            color: 'var(--accent)',
            fontWeight: 500,
          }}>
            {toneName}
          </span>
        )}
      </div>

      {/* Content */}
      <div ref={ref} style={{
        flex: 1,
        padding: 20,
        overflowY: 'auto',
        fontFamily: 'var(--mono)',
        fontSize: 14,
        lineHeight: 1.75,
        color: isEmpty ? 'var(--text-dim)' : 'var(--text)',
      }}>
        {isEmpty ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', gap: 12, opacity: 0.5 }}>
            <div style={{ fontSize: 32 }}>✦</div>
            <div style={{ fontSize: 13 }}>Rewritten text will appear here</div>
          </div>
        ) : (
          <>
            {text}
            {streaming && (
              <span style={{
                display: 'inline-block',
                width: 2, height: '1em',
                background: 'var(--accent)',
                marginLeft: 2,
                verticalAlign: 'text-bottom',
                animation: 'blink 0.8s step-end infinite',
              }} />
            )}
            <style>{`@keyframes blink { 50% { opacity: 0; } }`}</style>
          </>
        )}
      </div>

      {/* Copy button */}
      {text && !streaming && (
        <div style={{ padding: '10px 20px', borderTop: '1px solid var(--border)', flexShrink: 0 }}>
          <button
            onClick={() => navigator.clipboard.writeText(text)}
            style={{
              fontSize: 12, padding: '6px 14px',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border)',
              background: 'transparent',
              color: 'var(--text-dim)',
              cursor: 'pointer',
              fontFamily: 'var(--sans)',
              transition: 'all 0.15s',
            }}
            onMouseEnter={e => { e.target.style.color = '#fff'; e.target.style.borderColor = 'var(--accent)' }}
            onMouseLeave={e => { e.target.style.color = 'var(--text-dim)'; e.target.style.borderColor = 'var(--border)' }}
          >
            Copy
          </button>
        </div>
      )}
    </div>
  )
}
