import axios from "axios"

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api/v1",
  headers: { "Content-Type": "application/json" },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("pp_access_token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

let isRefreshing = false
let pendingQueue = []

function resolveQueue(token) {
  pendingQueue.forEach((cb) => cb(token))
  pendingQueue = []
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const status = error.response?.status

    if (status === 401 && !originalRequest._retry && !originalRequest.url.includes("/auth/")) {
      const refreshToken = localStorage.getItem("pp_refresh_token")
      if (!refreshToken) {
        return Promise.reject(error)
      }

      if (isRefreshing) {
        return new Promise((resolve) => {
          pendingQueue.push((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            resolve(api(originalRequest))
          })
        })
      }

      originalRequest._retry = true
      isRefreshing = true
      try {
        const { data } = await axios.post(
          `${import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api/v1"}/auth/refresh`,
          {},
          { headers: { Authorization: `Bearer ${refreshToken}` } }
        )
        const newToken = data.data.access_token
        localStorage.setItem("pp_access_token", newToken)
        resolveQueue(newToken)
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return api(originalRequest)
      } catch (refreshError) {
        localStorage.removeItem("pp_access_token")
        localStorage.removeItem("pp_refresh_token")
        localStorage.removeItem("pp_user")
        window.location.href = "/login"
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export default api
