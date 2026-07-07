<script setup>
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth.store"
import { useNotificationStore } from "@/stores/notification.store"
import { useUiStore } from "@/stores/ui.store"
import { initials } from "@/utils/formatters"
import applicationService from "@/services/application.service"

const auth = useAuthStore()
const notifications = useNotificationStore()
const ui = useUiStore()
const router = useRouter()

const showNotifications = ref(false)

onMounted(() => {
  notifications.fetchUnreadCount()
})

async function handleLogout() {
  const ok = await ui.confirm({
    title: "Log out?",
    message: "You will need to sign in again to access your dashboard.",
    confirmText: "Log out",
    variant: "danger",
  })
  if (!ok) return
  await auth.logout()
  router.push("/login")
}

async function toggleNotifications() {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value) {
    await notifications.fetchList()
  }
}

async function handleNotificationClick(n) {
  await notifications.markRead(n.id)

  if (n.link && n.link.startsWith("/applications/export/") && n.link.endsWith("/download")) {
    const jobId = n.link.split("/applications/export/")[1].split("/")[0]
    try {
      const { data } = await applicationService.downloadExport(jobId)
      const url = window.URL.createObjectURL(new Blob([data], { type: "text/csv" }))
      const link = document.createElement("a")
      link.href = url
      link.download = "my_applications.csv"
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (e) {
      ui.error("Could not download export")
    }
    return
  }

  if (n.link) {
    showNotifications.value = false
    router.push(n.link)
  }
}
</script>

<template>
  <nav class="pp-navbar d-flex align-items-center justify-content-between px-3 px-lg-4">
    <button class="btn btn-light d-lg-none" @click="ui.toggleSidebar">
      <i class="bi bi-list fs-5"></i>
    </button>

    <div class="d-none d-lg-block fw-semibold text-secondary">Placement Portal</div>

    <div class="d-flex align-items-center gap-3">
      <div class="position-relative">
        <button class="btn btn-light position-relative" @click="toggleNotifications">
          <i class="bi bi-bell fs-6"></i>
          <span
            v-if="notifications.unreadCount > 0"
            class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
            style="font-size: 0.6rem"
          >
            {{ notifications.unreadCount }}
          </span>
        </button>
        <div v-if="showNotifications" class="pp-notif-dropdown pp-fade-in">
          <div class="p-3 border-bottom fw-semibold">Notifications</div>
          <div v-if="notifications.items.length === 0" class="p-3 text-muted small">No notifications yet</div>
          <div
            v-for="n in notifications.items"
            :key="n.id"
            class="p-3 border-bottom pp-notif-item"
            :class="{ 'bg-light': !n.is_read }"
            @click="handleNotificationClick(n)"
          >
            <div class="fw-semibold small">{{ n.title }}</div>
            <div class="small text-muted">{{ n.message }}</div>
          </div>
        </div>
      </div>

      <div class="d-flex align-items-center gap-2">
        <div class="pp-avatar">{{ initials(auth.user?.name) }}</div>
        <div class="d-none d-md-block">
          <div class="small fw-semibold">{{ auth.user?.name }}</div>
          <div class="small pp-text-muted">{{ auth.role }}</div>
        </div>
      </div>

      <button class="btn btn-outline-danger btn-sm" @click="handleLogout">
        <i class="bi bi-box-arrow-right"></i>
      </button>
    </div>
  </nav>
</template>

<style scoped>
.pp-navbar {
  height: 64px;
  background: #fff;
  border-bottom: 1px solid var(--pp-border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.pp-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--pp-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 600;
}
.pp-notif-dropdown {
  position: absolute;
  right: 0;
  top: 48px;
  width: 320px;
  max-height: 400px;
  overflow-y: auto;
  background: #fff;
  border: 1px solid var(--pp-border);
  border-radius: var(--pp-radius);
  box-shadow: var(--pp-shadow-lg);
  z-index: 200;
}
.pp-notif-item {
  cursor: pointer;
}
.pp-notif-item:hover {
  background: #f1f5f9 !important;
}
</style>
