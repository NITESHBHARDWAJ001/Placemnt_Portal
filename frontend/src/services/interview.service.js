import api from "./api"

export default {
  schedule(applicationId, payload) {
    return api.post(`/interviews/applications/${applicationId}`, payload)
  },
  listForApplication(applicationId) {
    return api.get(`/interviews/applications/${applicationId}`)
  },
  listForCompany() {
    return api.get("/interviews/company")
  },
  update(interviewId, payload) {
    return api.patch(`/interviews/${interviewId}`, payload)
  },
}
