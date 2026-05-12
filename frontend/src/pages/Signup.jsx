import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function Signup() {
  const navigate = useNavigate()
  const { signup } = useAuthStore()
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    dosha: '',
    constitution: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const { name, email, password, confirmPassword } = formData
      const dosha = formData.dosha.trim().toLowerCase()
      const constitution = formData.constitution.trim()

      if (!name || !email || !password || !confirmPassword) {
        throw new Error('Please fill in all fields')
      }

      if (!/\S+@\S+\.\S+/.test(email)) {
        throw new Error('Please enter a valid email')
      }

      if (password.length < 6) {
        throw new Error('Password must be at least 6 characters')
      }

      if (password !== confirmPassword) {
        throw new Error('Passwords do not match')
      }

      if (!dosha && !constitution) {
        throw new Error('Please choose a dosha or describe your constitution first')
      }

      await signup(name, email, password, dosha, constitution)
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
          <p className="mt-2 text-slate-500">Create your account</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="glass-panel rounded-[2rem] p-8">
          {error && (
            <div className="mb-4 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-600">
              {error}
            </div>
          )}

          <div className="mb-4">
            <label className="mb-2 block text-sm font-medium text-slate-700">Full Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="John Doe"
              className="input-shell w-full"
            />
          </div>

          <div className="mb-4">
            <label className="mb-2 block text-sm font-medium text-slate-700">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="your@email.com"
              className="input-shell w-full"
            />
          </div>

          <div className="mb-4">
            <label className="mb-2 block text-sm font-medium text-slate-700">Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
              className="input-shell w-full"
            />
            <p className="mt-1 text-xs text-slate-500">At least 6 characters</p>
          </div>

          <div className="mb-4">
            <label className="mb-2 block text-sm font-medium text-slate-700">Known Dosha</label>
            <select
              name="dosha"
              value={formData.dosha}
              onChange={handleChange}
              className="input-shell w-full"
            >
              <option value="">Select your dosha or leave blank if unsure</option>
              <option value="vata">Vata</option>
              <option value="pitta">Pitta</option>
              <option value="kapha">Kapha</option>
            </select>
            <p className="mt-1 text-xs text-slate-500">
              If you do not know your dosha, describe your body type and habits below.
            </p>
          </div>

          <div className="mb-6">
            <label className="mb-2 block text-sm font-medium text-slate-700">Constitution Description</label>
            <textarea
              name="constitution"
              value={formData.constitution}
              onChange={handleChange}
              placeholder="Example: I feel cold easily, have dry skin, irregular appetite, and light sleep."
              rows="4"
              className="input-shell w-full resize-none"
            />
          </div>

          <div className="mb-6">
            <label className="mb-2 block text-sm font-medium text-slate-700">Confirm Password</label>
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="••••••••"
              className="input-shell w-full"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="accent-button w-full px-4 py-3 disabled:opacity-50"
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>

          <div className="mt-4 text-center text-slate-500">
            Already have an account?{' '}
            <Link to="/login" className="font-medium text-emerald-700 hover:text-emerald-800">
              Sign in
            </Link>
          </div>
        </form>

        {/* Footer */}
        <div className="mt-6 text-center text-xs text-slate-500">
          <p className="mb-3">By signing up, you agree to save your dosha profile for Ayurveda guidance.</p>
          <Link to="/" className="hover:text-slate-700">
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  )
}
