import { defineStore } from "pinia"
import authService from "@/services/auth.service"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: JSON.parse(localStorage.getItem("pp_user") || "null"),
    accessToken: localStorage.getItem("pp_access_token") || null,
    refreshToken: localStorage.getItem("pp_refresh_token") || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken && !!state.user,
    role: (state) => state.user?.role || null,
  },

  actions: {
    setSession({ user, access_token, refresh_token }) {
      this.user = user
      this.accessToken = access_token
      this.refreshToken = refresh_token
      localStorage.setItem("pp_user", JSON.stringify(user))
      localStorage.setItem("pp_access_token", access_token)
      localStorage.setItem("pp_refresh_token", refresh_token)
    },

    async login(credentials) {
      const { data } = await authService.login(credentials)
      this.setSession(data.data)
      return data.data.user
    },

    async register(payload) {
      const { data } = await authService.register(payload)
      return data.data
    },

    async logout() {
      try {
        await authService.logout()
      } catch (e) {
        // ignore network errors on logout
      }
      this.clearSession()
    },

    clearSession() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem("pp_user")
      localStorage.removeItem("pp_access_token")
      localStorage.removeItem("pp_refresh_token")
    },

    homeRouteForRole() {
      const map = {
        ADMIN: "/admin/dashboard",
        COMPANY: "/company/dashboard",
        STUDENT: "/student/dashboard",
      }
      return map[this.role] || "/login"
    },
  },
})
