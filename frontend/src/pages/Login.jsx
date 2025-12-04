import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import useAuthStore from '../store/auth'
import { authApi } from '../lib/api'

export default function Login() {
  const navigate = useNavigate()
  const { setToken, setUser, setLoading, setError, error, loading } = useAuthStore()
  const [formData, setFormData] = useState({ email: '', password: '' })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await authApi.login(formData.email, formData.password)
      const { access_token, user_id } = response.data

      setToken(access_token)
      setUser({ id: user_id, email: formData.email })
      navigate('/chat')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-earth-50 flex items-center justify-center px-4">
      <div className="card w-full max-w-md p-8">
        <div className="mb-8">
          <h1 className="text-3xl mb-2">Archaeologist Agent</h1>
          <p className="text-earth-600">Login to explore artifacts</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="input-field"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              className="input-field"
              placeholder="••••••••"
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-earth-600">
            Don't have an account?{' '}
            <Link to="/register" className="text-earth-700 hover:underline font-medium">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
