import type { ChatMessage, ChatResponse } from '../types'

export async function sendChat(conversationId: string, message: string, context: ChatMessage[] = []): Promise<ChatResponse> {
  const response = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ conversation_id: conversationId, message, context: context.map(({ role, content }) => ({ role, content })) }) })
  const payload = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(payload.detail || 'The shopping agent could not complete this request.')
  return payload as ChatResponse
}
