import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function Login() {
  const navigate = useNavigate()
  const { login } = useAuthStore()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (!email || !password) {
        throw new Error('Please fill in all fields')
      }
      if (!/\S+@\S+\.\S+/.test(email)) {
        throw new Error('Please enter a valid email')
      }

      await login(email, password)
      navigate('/chat')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center px-4 py-10">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-600 via-emerald-500 to-amber-300 text-2xl font-bold text-white shadow-[0_18px_35px_rgba(71,128,82,0.25)]">
            ॐ
          </div>
          <h1 className="text-3xl font-semibold tracking-tight text-slate-950">AyurAI</h1>
          <p className="mt-2 text-slate-500">Welcome back</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="glass-panel rounded-[2rem] p-8">
          {error && (
            <div className="mb-4 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-600">
              {error}
            </div>
          )}

          <div className="mb-4">
            <label className="mb-2 block text-sm font-medium text-slate-700">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              className="input-shell w-full"
            />
          </div>

          <div className="mb-6">
            <label className="mb-2 block text-sm font-medium text-slate-700">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="input-shell w-full"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="accent-button w-full px-4 py-3 disabled:opacity-50"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

          <div className="mt-4 text-center text-slate-500">
            Don't have an account?{' '}
            <Link to="/signup" className="font-medium text-emerald-700 hover:text-emerald-800">
              Sign up
            </Link>
          </div>

          <div className="mt-6 border-t border-white/70 pt-6">
            <button
              type="button"
              onClick={() => {
                setEmail('demo@example.com')
                setPassword('demo123')
              }}
              className="secondary-button w-full px-4 py-2 text-sm"
            >
              Demo: Click to fill demo credentials
            </button>
          </div>
        </form>

        {/* Footer */}
        <div className="mt-6 text-center text-sm text-slate-500">
          <Link to="/" className="hover:text-slate-700">
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  )
}
