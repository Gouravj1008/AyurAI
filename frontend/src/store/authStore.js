import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

const getApiErrorMessage = (error, fallback) => {
  if (error?.response?.data?.error) return error.response.data.error
  if (error?.response?.data?.message) return error.response.data.message
  if (error?.message) return error.message
  return fallback
}

export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      token: null,

      login: async (email, password) => {
        let response
        try {
          response = await apiClient.post('/auth/login', {
            email,
            password,
          })
        } catch (error) {
          throw new Error(getApiErrorMessage(error, 'Login failed'))
        }

        if (!response.data?.success) {
          throw new Error(response.data?.error || 'Login failed')
        }

        set({
          user: response.data.user,
          isAuthenticated: true,
          token: response.data.token,
        })

        return response.data
      },

      signup: async (name, email, password, dosha = '', constitution = '') => {
        let response
        try {
          response = await apiClient.post('/auth/signup', {
            name,
            email,
            password,
            dosha,
            constitution,
          })
        } catch (error) {
          throw new Error(getApiErrorMessage(error, 'Signup failed'))
        }

        if (!response.data?.success) {
          throw new Error(response.data?.error || 'Signup failed')
        }

        set({
          user: response.data.user,
          isAuthenticated: true,
          token: response.data.token,
        })

        return response.data
      },

      logout: () => {
        set({
          user: null,
          isAuthenticated: false,
          token: null,
        })
      },

      setUser: (user) => set({ user }),
    }),
    {
      name: 'auth-store',
    }
  )
)
