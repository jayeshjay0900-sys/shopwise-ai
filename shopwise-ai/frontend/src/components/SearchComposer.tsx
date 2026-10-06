import { ArrowUp, Sparkles } from 'lucide-react'
import { useState } from 'react'

const prompts = ['Best phones under ₹50,000', 'Gaming laptop under ₹1 lakh', 'ANC headphones under ₹10,000', 'Best camera for travel']

export function SearchComposer({ onSubmit, busy }: { onSubmit: (value: string) => void; busy: boolean }) {
  const [value, setValue] = useState('')
  const submit = () => { const next = value.trim(); if (next && !busy) { onSubmit(next); setValue('') } }
  return <div className="composer-wrap">
    <div className="composer surface">
      <div className="composer-icon"><Sparkles size={18}/></div>
      <textarea className="focus-ring" rows={2} value={value} onChange={e => setValue(e.target.value)} onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit() } }} placeholder="Tell us the purchase decision you’re trying to make…" aria-label="Shopping research request" />
      <button className="send-button focus-ring" onClick={submit} disabled={busy || !value.trim()} aria-label="Send request"><ArrowUp size={18}/></button>
    </div>
    <div className="prompt-row">{prompts.map(prompt => <button key={prompt} className="prompt-chip focus-ring" onClick={() => setValue(prompt)}>{prompt}</button>)}</div>
    <style>{`.composer-wrap{width:min(780px,100%);margin:28px auto 0}.composer{display:flex;align-items:flex-end;gap:12px;padding:16px 16px 16px 18px;box-shadow:0 18px 55px rgba(20,32,43,.11)}.composer-icon{color:#0f766e;padding-bottom:10px}.composer textarea{flex:1;resize:none;border:0;outline:0;background:transparent;color:#14202b;font-size:16px;line-height:1.55}.composer textarea::placeholder{color:#899399}.send-button{width:42px;height:42px;display:grid;place-items:center;border:0;border-radius:14px;background:#0f766e;color:white;transition:transform .2s,background .2s}.send-button:hover:not(:disabled){background:#0b5f59;transform:translateY(-2px)}.send-button:disabled{opacity:.35;cursor:not-allowed}.prompt-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.prompt-chip{border:1px solid #d9dfdc;border-radius:999px;background:transparent;color:#52606a;padding:8px 12px;font-size:12px;transition:background .2s,color .2s,border .2s}.prompt-chip:hover{background:#e5f1ef;color:#0f766e;border-color:#a9d5d0}`}</style>
  </div>
}
