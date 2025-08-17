'use client'

import { useState } from 'react'

interface SentimentResponse {
  label: string
  confidence: number
}

export default function Home() {
  const [text, setText] = useState('')
  const [sentiment, setSentiment] = useState<SentimentResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const analyzeSentiment = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze')
      return
    }

    setLoading(true)
    setError(null)
    setSentiment(null)

    try {
      const base = process.env.NEXT_PUBLIC_API_BASE || "";
      const response = await fetch(`${base}/sentiment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text.trim() }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data: SentimentResponse = await response.json()
      setSentiment(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze sentiment')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ minHeight: '100vh', padding: '2rem' }}>
      <div style={{ maxWidth: '42rem', margin: '0 auto' }}>
        <h1 style={{ 
          fontSize: '2.25rem', 
          fontWeight: 'bold', 
          textAlign: 'center', 
          marginBottom: '2rem',
          color: '#1f2937'
        }}>
          Sentiment Analyzer
        </h1>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div>
            <label htmlFor="text" style={{ 
              display: 'block', 
              fontSize: '0.875rem', 
              fontWeight: '500', 
              color: '#374151',
              marginBottom: '0.5rem'
            }}>
              Enter text to analyze:
            </label>
            <textarea
              id="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Type or paste your text here..."
              style={{ 
                width: '100%', 
                height: '8rem', 
                resize: 'none'
              }}
              disabled={loading}
            />
          </div>

          <button
            onClick={analyzeSentiment}
            disabled={loading || !text.trim()}
            style={{ width: '100%' }}
          >
            {loading ? 'Analyzing...' : 'Analyze Sentiment'}
          </button>

          {error && (
            <div style={{ 
              backgroundColor: '#fef2f2', 
              border: '1px solid #fecaca', 
              borderRadius: '0.375rem', 
              padding: '1rem'
            }}>
              <p style={{ color: '#991b1b' }}>{error}</p>
            </div>
          )}

          {sentiment && (
            <div style={{ 
              backgroundColor: '#f0fdf4', 
              border: '1px solid #bbf7d0', 
              borderRadius: '0.375rem', 
              padding: '1.5rem'
            }}>
              <h3 style={{ 
                fontSize: '1.125rem', 
                fontWeight: '600', 
                color: '#166534',
                marginBottom: '1rem'
              }}>
                Analysis Result
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <p style={{ color: '#15803d' }}>
                  <span style={{ fontWeight: '500' }}>Label:</span> {sentiment.label}
                </p>
                <p style={{ color: '#15803d' }}>
                  <span style={{ fontWeight: '500' }}>Confidence:</span> {(sentiment.confidence * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
