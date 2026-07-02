import api from "./api"

export default {
  admin() {
    return api.get("/admin/dashboard")
  },
  company() {
    return api.get("/company/dashboard")
  },
  student() {
    return api.get("/student/dashboard")
  },
  activityLogs(params) {
    return api.get("/admin/activity-logs", { params })
  },
  adminReports() {
    return api.get("/admin/reports/summary")
  },
}
