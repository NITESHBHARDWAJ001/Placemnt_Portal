import { defineStore } from "pinia"
import notificationService from "@/services/notification.service"

export const useNotificationStore = defineStore("notification", {
  state: () => ({
    items: [],
    unreadCount: 0,
  }),

  actions: {
    async fetchUnreadCount() {
      try {
        const { data } = await notificationService.unreadCount()
        this.unreadCount = data.data.count
      } catch (e) {
        // silent
      }
    },
    async fetchList() {
      const { data } = await notificationService.list({ per_page: 20 })
      this.items = data.data
    },
    async markRead(id) {
      await notificationService.markRead(id)
      const item = this.items.find((n) => n.id === id)
      if (item) item.is_read = true
      this.unreadCount = Math.max(0, this.unreadCount - 1)
    },
  },
})
