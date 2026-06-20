const ICONS = {
  '1': '💼', '2': '👋', '3': '🙏',
  '4': '💪', '5': '⚡', '6': '😄', '7': '🌧️',
}

export default function ToneGrid({ tones, selected, onSelect, disabled }) {
  return (
    <div>
      <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-dim)', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 10 }}>
        Choose a tone
      </div>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: 8,
      }}>
        {tones.map(t => {
          const active = selected === t.key
          return (
            <button
              key={t.key}
              onClick={() => !disabled && onSelect(t.key)}
              disabled={disabled}
              title={t.description}
              style={{
                padding: '10px 8px',
                borderRadius: 'var(--radius-sm)',
                border: `1px solid ${active ? 'var(--accent)' : 'var(--border)'}`,
                background: active ? 'var(--accent-glow)' : 'var(--surface2)',
                color: active ? '#fff' : 'var(--text)',
                cursor: disabled ? 'not-allowed' : 'pointer',
                opacity: disabled ? 0.5 : 1,
                fontSize: 12,
                fontFamily: 'var(--sans)',
                fontWeight: active ? 600 : 400,
                transition: 'all 0.15s ease',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: 4,
                lineHeight: 1.3,
              }}
            >
              <span style={{ fontSize: 16 }}>{ICONS[t.key]}</span>
              {t.name}
            </button>
          )
        })}
      </div>
    </div>
  )
}
