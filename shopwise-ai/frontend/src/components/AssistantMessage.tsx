import type { ChatResponse } from '../types'
export function AssistantMessage({ response }: { response: ChatResponse }) { return <div className="assistant-summary"><span className="section-label">ShopWise AI analysis</span><p>{response.assistant_message}</p><small>{response.evidence_count} evidence sources reviewed</small></div> }
