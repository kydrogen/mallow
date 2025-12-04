import { create } from 'zustand'

const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('auth_token'),
  loading: false,
  error: null,

  setUser: (user) => set({ user }),
  setToken: (token) => {
    if (token) {
      localStorage.setItem('auth_token', token)
    } else {
      localStorage.removeItem('auth_token')
    }
    set({ token })
  },
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),

  logout: () => set({
    user: null,
    token: null,
    error: null
  }),

  clearError: () => set({ error: null })
}))

export default useAuthStore
