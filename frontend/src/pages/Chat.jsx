import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import useAuthStore from '../store/auth'
import useChatStore from '../store/chat'
import { agentApi } from '../lib/api'
import MessageBubble from '../components/MessageBubble'
import ArtifactPanel from '../components/ArtifactPanel'

export default function Chat() {
  const navigate = useNavigate()
  const { token, logout } = useAuthStore()
  const { messages, addMessage, setMessages, artifacts, setArtifacts, loading, setLoading, error, setError } = useChatStore()
  const [input, setInput] = useState('')
  const [showArtifacts, setShowArtifacts] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    if (!token) {
      navigate('/login')
      return
    }
    fetchArtifacts()
  }, [token, navigate])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const fetchArtifacts = async () => {
    try {
      const response = await agentApi.getArtifacts()
      setArtifacts(response.data || [])
    } catch (err) {
      console.error('Failed to fetch artifacts:', err)
    }
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    addMessage('user', userMessage)
    setLoading(true)
    setError(null)

    try {
      const response = await agentApi.query(userMessage, messages)
      addMessage('assistant', response.data.response)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to query agent')
      addMessage('assistant', 'Sorry, I encountered an error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="h-screen flex flex-col bg-earth-50">
      <header className="bg-earth-800 text-white shadow-lg px-6 py-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-serif">Archaeologist Agent</h1>
          <p className="text-earth-200 text-sm">Explore artifacts and discoveries</p>
        </div>
        <div className="flex gap-4">
          <button
            onClick={() => setShowArtifacts(!showArtifacts)}
            className="px-4 py-2 bg-earth-600 hover:bg-earth-700 rounded-lg transition-colors text-sm font-medium"
          >
            {showArtifacts ? 'Hide' : 'Show'} Artifacts
          </button>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-colors text-sm font-medium"
          >
            Logout
          </button>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden gap-6 p-6">
        <div className="flex-1 flex flex-col bg-white rounded-lg shadow-md overflow-hidden">
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 && (
              <div className="flex items-center justify-center h-full text-earth-400">
                <div className="text-center">
                  <p className="text-lg mb-2">Start a conversation</p>
                  <p className="text-sm">Ask about artifacts or get archaeological insights</p>
                </div>
              </div>
            )}
            {messages.map((msg, idx) => (
              <MessageBubble key={idx} role={msg.role} content={msg.content} />
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-earth-100 rounded-lg px-4 py-3 max-w-sm">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-earth-600 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-earth-600 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-earth-600 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSendMessage} className="border-t border-earth-200 p-4 bg-earth-50">
            {error && <div className="error-message mb-3">{error}</div>}
            <div className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={loading}
                placeholder="Ask about artifacts..."
                className="input-field flex-1 disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="btn-primary disabled:opacity-50"
              >
                Send
              </button>
            </div>
          </form>
        </div>

        {showArtifacts && (
          <aside className="w-80">
            <ArtifactPanel artifacts={artifacts} onRefresh={fetchArtifacts} />
          </aside>
        )}
      </div>
    </div>
  )
}
