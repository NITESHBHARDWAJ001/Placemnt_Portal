import api from "./api"

export default {
  listPublic(params) {
    return api.get("/drives", { params })
  },
  getDetail(driveId) {
    return api.get(`/drives/${driveId}`)
  },
  checkEligibility(driveId) {
    return api.get(`/drives/${driveId}/eligibility`)
  },
  create(payload) {
    return api.post("/drives", payload)
  },
  update(driveId, payload) {
    return api.put(`/drives/${driveId}`, payload)
  },
  remove(driveId) {
    return api.delete(`/drives/${driveId}`)
  },
  listMine(params) {
    return api.get("/drives/my", { params })
  },
  listPending(params) {
    return api.get("/drives/pending", { params })
  },
  listAll(params) {
    return api.get("/drives/all", { params })
  },
  approve(driveId) {
    return api.patch(`/drives/${driveId}/approve`)
  },
  reject(driveId, reason) {
    return api.patch(`/drives/${driveId}/reject`, { reason })
  },
}
