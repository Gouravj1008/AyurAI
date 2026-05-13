const trimTrailingSlash = (value) => value.replace(/\/+$/, '')

export const API_BASE_URL = trimTrailingSlash(
  import.meta.env.VITE_API_BASE_URL || '/api'
)

export const isUsingLocalApiFallback = API_BASE_URL === '/api'

export function getApiErrorMessage(error, fallback = 'Request failed') {
  if (error?.response?.data?.error) return error.response.data.error
  if (error?.response?.data?.message) return error.response.data.message

  if (error?.code === 'ERR_NETWORK' || error?.message === 'Network Error') {
    if (isUsingLocalApiFallback && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
      return 'Cannot reach the backend. Set VITE_API_BASE_URL to your Render backend URL ending in /api, then redeploy the frontend.'
    }

    return 'Cannot reach the backend. Check that the Render service is awake and that CORS_ORIGINS includes this frontend domain.'
  }

  if (error?.message) return error.message
  return fallback
}
