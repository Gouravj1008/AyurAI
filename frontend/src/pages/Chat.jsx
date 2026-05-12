import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { motion } from 'framer-motion'
import { useAuthStore } from '../store/authStore'
import ChatMessage from '../components/ChatMessage'
import Sidebar from '../components/Sidebar'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

export default function Chat() {
  const navigate = useNavigate()
  const { user, logout, token } = useAuthStore()
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: 'Namaste. I am your calm Ayurveda assistant. Ask about dosha balance, routines, herbs, or daily wellness support.',
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const messagesEndRef = useRef(null)

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!input.trim() || loading) return

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post(
        `${API_BASE_URL}/chat`,
        {
          message: input,
          dosha: user?.dosha || '',
          constitution: user?.constitution || '',
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          timeout: 120000, // 2 min — AI model may be loading on first request
        }
      )

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data?.message || 'I could not generate a response.',
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, botMessage])
    } catch (error) {
      console.error('Chat error:', error)

      // Extract a meaningful error from the backend response if available
      let errorContent =
        error?.response?.data?.error ||
        error?.response?.data?.message ||
        null

      if (!errorContent) {
        if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
          errorContent =
            '⏳ The AI model is still loading (this takes ~30s on first request). Please wait a moment and try again.'
        } else if (error.code === 'ERR_NETWORK' || !error.response) {
          errorContent =
            '🔌 Cannot reach the backend server. Make sure `python api_server.py` is running in e:\\Jarvis.'
        } else {
          errorContent = `Error ${error?.response?.status || ''}: ${error.message || 'Something went wrong. Please try again.'}`
        }
      }

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          type: 'bot',
          content: errorContent,
          timestamp: new Date(),
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const handleNewChat = () => {
    setMessages([
      {
        id: 1,
        type: 'bot',
        content: 'Namaste. A fresh consultation is ready. How can I support your wellness today?',
        timestamp: new Date(),
      },
    ])
  }

  return (
    <div className="relative flex h-screen overflow-hidden bg-[radial-gradient(circle_at_top,_rgba(184,221,196,0.28),_transparent_34%),linear-gradient(180deg,_#f7f6ef_0%,_#eef3ea_100%)] text-slate-900">
      <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.28)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.28)_1px,transparent_1px)] bg-[size:72px_72px] opacity-20" />

      {/* Sidebar */}
      <Sidebar
        isOpen={sidebarOpen}
        onNewChat={handleNewChat}
        onLogout={handleLogout}
        user={user}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Main Chat Area */}
      <div className="relative z-10 flex flex-1 flex-col">
        {/* Header */}
        <div className="border-b border-white/70 bg-white/55 px-4 py-4 backdrop-blur-xl sm:px-6">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="rounded-full border border-emerald-100 bg-white/80 p-2.5 shadow-sm transition duration-300 hover:-translate-y-0.5 hover:border-emerald-200 hover:bg-white"
              title="Toggle sidebar"
            >
              <svg
                className="h-5 w-5 text-emerald-900"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
            <div>
              <h1 className="text-lg font-semibold tracking-tight text-slate-950">AyurAI</h1>
              <p className="text-sm text-slate-500">AI-powered wellness guide</p>
            </div>
          </div>
          <div className="text-right text-sm text-slate-500">
            <div className="font-medium text-slate-800">{user?.name || user?.email}</div>
            {user?.dosha && <div className="mt-1 text-xs font-semibold uppercase tracking-[0.22em] text-emerald-700">{user.dosha} dosha</div>}
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="mx-auto flex max-w-5xl flex-col gap-4">
            {messages.map((message, index) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.28, delay: index * 0.03 }}
              >
                <ChatMessage message={message} />
              </motion.div>
            ))}
          </div>
          {loading && (
            <div className="mx-auto mt-4 flex max-w-5xl justify-start">
              <div className="rounded-[1.5rem] border border-emerald-100 bg-white/80 px-4 py-3 shadow-[0_14px_30px_rgba(65,95,72,0.08)] backdrop-blur-sm">
                <div className="flex gap-2">
                  <div className="h-2.5 w-2.5 animate-bounce rounded-full bg-emerald-500"></div>
                  <div className="h-2.5 w-2.5 animate-bounce rounded-full bg-emerald-500" style={{ animationDelay: '0.12s' }}></div>
                  <div className="h-2.5 w-2.5 animate-bounce rounded-full bg-emerald-500" style={{ animationDelay: '0.24s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-white/70 bg-white/60 px-4 py-4 backdrop-blur-xl sm:px-6">
          <div className="mx-auto max-w-5xl">
            <div className="flex gap-3 rounded-[1.75rem] border border-white/80 bg-white/75 p-3 shadow-[0_18px_50px_rgba(62,78,65,0.09)] backdrop-blur-md">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={`Ask about ${user?.dosha ? user.dosha.toUpperCase() : 'Vata, Pitta, or Kapha'} balance, herbs, or routine...`}
                rows="3"
                disabled={loading}
                className="min-h-[84px] flex-1 resize-none rounded-[1.35rem] border border-emerald-100 bg-[linear-gradient(180deg,rgba(255,255,255,0.96),rgba(248,250,246,0.92))] px-4 py-3 text-sm leading-7 text-slate-800 outline-none placeholder:text-slate-400 focus:border-emerald-300 focus:ring-2 focus:ring-emerald-100 disabled:opacity-50"
              />
              <button
                onClick={handleSendMessage}
                disabled={loading || !input.trim()}
                className="self-end rounded-[1.35rem] bg-gradient-to-br from-emerald-600 via-emerald-500 to-amber-300 p-4 text-white shadow-[0_16px_34px_rgba(73,139,85,0.3)] transition duration-300 hover:-translate-y-0.5 hover:shadow-[0_20px_40px_rgba(73,139,85,0.34)] disabled:cursor-not-allowed disabled:opacity-50"
                title="Send message (Ctrl+Enter)"
              >
                <svg
                  className="h-5 w-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M16.6915026,12.4744748 L3.50612381,13.2599618 C3.19218622,13.2599618 3.03521743,13.4170592 3.03521743,13.5741566 L1.15159189,20.0151496 C0.8376543,20.8006365 0.99,21.89 1.77946707,22.52 C2.41,22.99 3.50612381,23.1 4.13399899,22.8429026 L21.714504,14.0454487 C22.6563168,13.5741566 23.1272231,12.6315722 22.9702544,11.6889879 L4.13399899,1.16946437 C3.34915502,0.9123669 2.40734225,1.02348325 1.77946707,1.4947753 C0.994623095,2.13399899 0.837654326,3.22286166 1.15159189,3.99799429 L3.03521743,10.4389873 C3.03521743,10.5960847 3.19218622,10.753182 3.50612381,10.753182 L16.6915026,11.5386689 C16.6915026,11.5386689 17.1624089,11.5386689 17.1624089,12.0099611 C17.1624089,12.4744748 16.6915026,12.4744748 16.6915026,12.4744748 Z" />
                </svg>
              </button>
            </div>
            <p className="mt-3 text-center text-xs text-slate-500">
              Shift + Enter adds a new line. Responses stay focused on your saved dosha profile and wellness goals.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
