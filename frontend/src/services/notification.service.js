import api from "./api"

export default {
  list(params) {
    return api.get("/notifications", { params })
  },
  unreadCount() {
    return api.get("/notifications/unread-count")
  },
  markRead(notificationId) {
    return api.patch(`/notifications/${notificationId}/read`)
  },
}
