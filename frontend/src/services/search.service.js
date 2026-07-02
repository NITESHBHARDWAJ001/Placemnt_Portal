import api from "./api"

export default {
  students(q, params) {
    return api.get("/search/students", { params: { q, ...params } })
  },
  companies(q, params) {
    return api.get("/search/companies", { params: { q, ...params } })
  },
  drives(q, params) {
    return api.get("/search/drives", { params: { q, ...params } })
  },
  applicants(q, params) {
    return api.get("/search/applicants", { params: { q, ...params } })
  },
}
