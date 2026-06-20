import { useState, useRef } from 'react'

export default function MicButton({ onTranscript, disabled }) {
  const [listening, setListening] = useState(false)
  const recRef = useRef(null)

  const toggle = () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SR) {
      alert('Speech recognition is not supported in this browser. Try Chrome.')
      return
    }

    if (listening) {
      recRef.current?.stop()
      return
    }

    const rec = new SR()
    rec.lang = 'en-US'
    rec.interimResults = false
    recRef.current = rec

    rec.onstart  = () => setListening(true)
    rec.onend    = () => setListening(false)
    rec.onerror  = () => setListening(false)
    rec.onresult = (e) => onTranscript(e.results[0][0].transcript)
    rec.start()
  }

  const pulse = listening ? {
    animation: 'pulse 1.2s ease-in-out infinite',
    background: 'var(--red)',
    borderColor: 'var(--red)',
    color: '#fff',
  } : {}

  return (
    <>
      <style>{`
        @keyframes pulse {
          0%, 100% { box-shadow: 0 0 0 0 rgba(248,81,73,0.5); }
          50%       { box-shadow: 0 0 0 8px rgba(248,81,73,0); }
        }
      `}</style>
      <button
        onClick={toggle}
        disabled={disabled}
        title={listening ? 'Stop listening' : 'Speak your text'}
        style={{
          width: 38, height: 38,
          borderRadius: 'var(--radius-sm)',
          border: '1px solid var(--border)',
          background: 'var(--surface2)',
          color: 'var(--text-dim)',
          cursor: disabled ? 'not-allowed' : 'pointer',
          opacity: disabled ? 0.5 : 1,
          fontSize: 16,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0,
          transition: 'all 0.15s ease',
          ...pulse,
        }}
      >
        {listening ? '⏹' : '🎤'}
      </button>
    </>
  )
}
