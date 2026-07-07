import api from "./api"

export default {
  apply(driveId, resumeId) {
    return api.post(`/applications/drives/${driveId}/apply`, { resume_id: resumeId })
  },
  listForDrive(driveId, params) {
    return api.get(`/applications/drives/${driveId}`, { params })
  },
  myApplications(params) {
    return api.get("/applications/mine", { params })
  },
  triggerExport() {
    return api.post("/applications/export")
  },
  exportStatus(jobId) {
    return api.get(`/applications/export/${jobId}/status`)
  },
  downloadExport(jobId) {
    return api.get(`/applications/export/${jobId}/download`, { responseType: "blob" })
  },
  companyApplicants(params) {
    return api.get("/applications/company", { params })
  },
  allApplications(params) {
    return api.get("/admin/applications", { params })
  },
  withdraw(applicationId) {
    return api.patch(`/applications/${applicationId}/withdraw`)
  },
  updateStatus(applicationId, status) {
    return api.patch(`/applications/${applicationId}/status`, { status })
  },
}
