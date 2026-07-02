import api from "./api"

export default {
  blacklistUser(userId, reason) {
    return api.patch(`/admin/users/${userId}/blacklist`, { reason })
  },
  revokeBlacklist(userId) {
    return api.patch(`/admin/users/${userId}/revoke-blacklist`)
  },
  deactivateUser(userId) {
    return api.patch(`/admin/users/${userId}/deactivate`)
  },
  activateUser(userId) {
    return api.patch(`/admin/users/${userId}/activate`)
  },
}
