import api from "./api"

export default {
  getProfile() {
    return api.get("/company/profile")
  },
  updateProfile(payload) {
    return api.put("/company/profile", payload)
  },
  dashboard() {
    return api.get("/company/dashboard")
  },
  listCompanies(params) {
    return api.get("/admin/companies", { params })
  },
  approve(companyId) {
    return api.patch(`/admin/companies/${companyId}/approve`)
  },
  reject(companyId, reason) {
    return api.patch(`/admin/companies/${companyId}/reject`, { reason })
  },
}
