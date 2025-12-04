import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import useAuthStore from './store/auth'
import Login from './pages/Login'
import Register from './pages/Register'
import Chat from './pages/Chat'

function ProtectedRoute({ children }) {
  const { token } = useAuthStore()
  return token ? children : <Navigate to="/login" />
}

export default function App() {
  const { token } = useAuthStore()

  useEffect(() => {
    if (token) {
      // Optional: verify token validity with API
    }
  }, [token])

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/chat"
          element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={token ? <Navigate to="/chat" /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  )
}
