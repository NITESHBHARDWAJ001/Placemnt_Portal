import api from "./api"

export default {
  getProfile() {
    return api.get("/student/profile")
  },
  updateProfile(payload) {
    return api.put("/student/profile", payload)
  },
  addSkill(name) {
    return api.post("/student/skills", { name })
  },
  removeSkill(skillId) {
    return api.delete(`/student/skills/${skillId}`)
  },
  uploadResume(file) {
    const formData = new FormData()
    formData.append("resume", file)
    return api.post("/student/resume", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
  },
  listResumes() {
    return api.get("/student/resume")
  },
  deleteResume(resumeId) {
    return api.delete(`/student/resume/${resumeId}`)
  },
  dashboard() {
    return api.get("/student/dashboard")
  },
  listStudents(params) {
    return api.get("/admin/students", { params })
  },
}
