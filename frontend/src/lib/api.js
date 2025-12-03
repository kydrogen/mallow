import axios from 'axios'

const API_BASE = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authApi = {
  register: (email, password) =>
    api.post('/api/auth/register', { email, password }),
  login: (email, password) =>
    api.post('/api/auth/login', { email, password }),
  getCurrentUser: () =>
    api.get('/api/auth/me')
}

export const agentApi = {
  query: (question, conversationHistory = null) =>
    api.post('/api/agent/query', { question, conversation_history: conversationHistory }),
  getArtifacts: () =>
    api.get('/api/agent/artifacts'),
  saveArtifacts: (artifacts) =>
    api.post('/api/agent/artifacts', { artifacts })
}

export default api
