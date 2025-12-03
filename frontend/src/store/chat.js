import { create } from 'zustand'

const useChatStore = create((set) => ({
  messages: [],
  artifacts: [],
  loading: false,
  error: null,

  addMessage: (role, content) =>
    set((state) => ({
      messages: [...state.messages, {
        role,
        content,
        timestamp: new Date().toISOString()
      }]
    })),

  setMessages: (messages) => set({ messages }),
  setArtifacts: (artifacts) => set({ artifacts }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),

  clearChat: () => set({
    messages: [],
    error: null
  }),

  clearError: () => set({ error: null })
}))

export default useChatStore
