import { useState, useEffect } from 'react'
import Header from './components/Header'
import ToneGrid from './components/ToneGrid'
import MicButton from './components/MicButton'
import OutputPanel from './components/OutputPanel'

const API = 'http://localhost:8000'

export default function App() {
  const [tones, setTones]         = useState([])
  const [model, setModel]         = useState('')
  const [text, setText]           = useState('')
  const [selectedTone, setTone]   = useState('1')
  const [output, setOutput]       = useState('')
  const [streaming, setStreaming] = useState(false)
  const [error, setError]         = useState('')

  useEffect(() => {
    fetch(`${API}/api/tones`)
      .then(r => r.json())
      .then(d => { setTones(d.tones); setModel(d.model) })
      .catch(() => setError('Cannot connect to the backend. Make sure server.py is running.'))
  }, [])

  const rewrite = async () => {
    if (!text.trim()) return
    setOutput('')
    setError('')
    setStreaming(true)

    try {
      const res = await fetch(`${API}/api/rewrite`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, tone_key: selectedTone }),
      })

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buf = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buf += decoder.decode(value, { stream: true })
        const lines = buf.split('\n')
        buf = lines.pop()

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          const payload = line.slice(6)
          if (payload === '[DONE]') { setStreaming(false); return }
          try {
            const { token } = JSON.parse(payload)
            setOutput(prev => prev + token)
          } catch { /* ignore malformed chunks */ }
        }
      }
    } catch {
      setError('Request failed. Is Ollama running?')
    } finally {
      setStreaming(false)
    }
  }

  const activeTone = tones.find(t => t.key === selectedTone)

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Header model={model} />

      <div style={{ padding: '16px 40px 0', color: 'var(--text-dim)', fontSize: 14 }}>
        Type or speak your text, pick a tone, and get a polished rewrite instantly.
      </div>

      {error && (
        <div style={{
          margin: '16px 40px 0',
          padding: '12px 16px',
          borderRadius: 'var(--radius-sm)',
          background: 'rgba(248,81,73,0.1)',
          border: '1px solid rgba(248,81,73,0.3)',
          color: 'var(--red)',
          fontSize: 13,
        }}>
          {error}
        </div>
      )}

      <div style={{
        flex: 1,
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: 20,
        padding: '20px 40px 32px',
        minHeight: 0,
      }}>

        {/* Left - input + tones + button */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>

          {/* Text input card */}
          <div style={{
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius)',
            display: 'flex', flexDirection: 'column',
            flex: 1, overflow: 'hidden',
          }}>
            <div style={{
              padding: '12px 20px',
              borderBottom: '1px solid var(--border)',
              display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            }}>
              <span style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-dim)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
                Input
              </span>
              <MicButton onTranscript={setText} disabled={streaming} />
            </div>

            <textarea
              value={text}
              onChange={e => setText(e.target.value)}
              placeholder="Type your text here, or click the mic to speak..."
              disabled={streaming}
              style={{
                flex: 1, padding: 20,
                background: 'transparent', border: 'none', outline: 'none',
                resize: 'none', color: 'var(--text)',
                fontFamily: 'var(--mono)', fontSize: 14, lineHeight: 1.75,
                minHeight: 160,
              }}
            />

            <div style={{
              padding: '8px 20px',
              borderTop: '1px solid var(--border)',
              display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            }}>
              <span style={{ fontSize: 12, color: 'var(--text-dim)' }}>{text.length} chars</span>
              {text && (
                <button onClick={() => { setText(''); setOutput('') }} style={{
                  fontSize: 12, padding: '4px 10px', borderRadius: 6,
                  border: '1px solid var(--border)', background: 'transparent',
                  color: 'var(--text-dim)', cursor: 'pointer', fontFamily: 'var(--sans)',
                }}>
                  Clear
                </button>
              )}
            </div>
          </div>

          {/* Tone grid card */}
          <div style={{
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius)',
            padding: 20,
          }}>
            <ToneGrid tones={tones} selected={selectedTone} onSelect={setTone} disabled={streaming} />
          </div>

          {/* Rewrite button */}
          <button
            onClick={rewrite}
            disabled={!text.trim() || streaming || tones.length === 0}
            style={{
              padding: '14px',
              borderRadius: 'var(--radius)',
              border: 'none',
              background: streaming ? 'var(--accent-dim)' : 'linear-gradient(135deg, #7c6aff, #a78bfa)',
              color: '#fff',
              fontSize: 15, fontWeight: 600,
              fontFamily: 'var(--sans)',
              cursor: (!text.trim() || streaming) ? 'not-allowed' : 'pointer',
              opacity: (!text.trim() && !streaming) ? 0.5 : 1,
              transition: 'all 0.2s ease',
              letterSpacing: '-0.2px',
            }}
          >
            {streaming ? 'Rewriting...' : `Rewrite in ${activeTone?.name ?? ''} tone`}
          </button>
        </div>

        {/* Right - output */}
        <OutputPanel text={output} streaming={streaming} toneName={output ? activeTone?.name : null} />
      </div>
    </div>
  )
}
