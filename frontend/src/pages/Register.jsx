import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import useAuthStore from '../store/auth'
import { authApi } from '../lib/api'

export default function Register() {
  const navigate = useNavigate()
  const { setToken, setUser, setLoading, setError, error, loading } = useAuthStore()
  const [formData, setFormData] = useState({ email: '', password: '', passwordConfirm: '' })
  const [formError, setFormError] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    setFormError(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setFormError(null)

    if (formData.password !== formData.passwordConfirm) {
      setFormError('Passwords do not match')
      return
    }

    if (formData.password.length < 8) {
      setFormError('Password must be at least 8 characters')
      return
    }

    setLoading(true)

    try {
      const response = await authApi.register(formData.email, formData.password)
      const { access_token, user_id } = response.data

      setToken(access_token)
      setUser({ id: user_id, email: formData.email })
      navigate('/chat')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-earth-50 flex items-center justify-center px-4">
      <div className="card w-full max-w-md p-8">
        <div className="mb-8">
          <h1 className="text-3xl mb-2">Create Account</h1>
          <p className="text-earth-600">Join the archaeological exploration</p>
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

          <div>
            <label className="block text-sm font-medium mb-2">Confirm Password</label>
            <input
              type="password"
              name="passwordConfirm"
              value={formData.passwordConfirm}
              onChange={handleChange}
              required
              className="input-field"
              placeholder="••••••••"
            />
          </div>

          {(error || formError) && (
            <div className="error-message">{error || formError}</div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full disabled:opacity-50"
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-earth-600">
            Already have an account?{' '}
            <Link to="/login" className="text-earth-700 hover:underline font-medium">
              Login
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
