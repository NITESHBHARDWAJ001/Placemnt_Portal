import api from "./api"

export default {
  register(payload) {
    return api.post("/auth/register", payload)
  },
  login(payload) {
    return api.post("/auth/login", payload)
  },
  me() {
    return api.get("/auth/me")
  },
  logout() {
    return api.post("/auth/logout")
  },
}
