<script setup>
import { computed } from "vue"
import { useAuthStore } from "@/stores/auth.store"
import { useUiStore } from "@/stores/ui.store"

const auth = useAuthStore()
const ui = useUiStore()

const menus = {
  ADMIN: [
    { to: "/admin/dashboard", icon: "bi-speedometer2", label: "Dashboard" },
    { to: "/admin/companies", icon: "bi-building", label: "Companies" },
    { to: "/admin/drives", icon: "bi-briefcase", label: "Drives" },
    { to: "/admin/students", icon: "bi-people", label: "Students" },
    { to: "/admin/activity-logs", icon: "bi-clock-history", label: "Activity Logs" },
  ],
  COMPANY: [
    { to: "/company/dashboard", icon: "bi-speedometer2", label: "Dashboard" },
    { to: "/company/profile", icon: "bi-building", label: "Profile" },
    { to: "/company/drives", icon: "bi-briefcase", label: "My Drives" },
    { to: "/company/interviews", icon: "bi-calendar-event", label: "Interviews" },
  ],
  STUDENT: [
    { to: "/student/dashboard", icon: "bi-speedometer2", label: "Dashboard" },
    { to: "/student/profile", icon: "bi-person", label: "Profile" },
    { to: "/student/drives", icon: "bi-briefcase", label: "Browse Drives" },
    { to: "/student/applications", icon: "bi-file-earmark-text", label: "My Applications" },
    { to: "/student/placement-history", icon: "bi-trophy", label: "Placement History" },
  ],
}

const items = computed(() => menus[auth.role] || [])

function handleLinkClick() {
  if (window.innerWidth <= 991) ui.sidebarCollapsed = false
}
</script>

<template>
  <div v-if="ui.sidebarCollapsed" class="pp-sidebar-backdrop d-lg-none" @click="ui.toggleSidebar"></div>
  <aside class="pp-sidebar" :class="{ open: ui.sidebarCollapsed }">
    <div class="pp-sidebar-brand d-flex align-items-center gap-2 px-3 py-4">
      <i class="bi bi-mortarboard-fill fs-4 text-primary"></i>
      <span class="fw-bold fs-5">PlacePortal</span>
    </div>
    <nav class="px-2">
      <router-link
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        class="pp-sidebar-link"
        active-class="active"
        @click="handleLinkClick"
      >
        <i :class="['bi', item.icon]"></i>
        <span>{{ item.label }}</span>
      </router-link>
    </nav>
  </aside>
</template>

<style scoped>
.pp-sidebar {
  width: 250px;
  min-height: 100vh;
  background: var(--pp-secondary);
  color: #cbd5e1;
  flex-shrink: 0;
}
.pp-sidebar-brand {
  color: #fff;
}
.pp-sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 1rem;
  border-radius: var(--pp-radius-sm);
  color: #cbd5e1;
  text-decoration: none;
  margin-bottom: 0.25rem;
  font-size: 0.92rem;
  transition: background 0.15s ease;
}
.pp-sidebar-link:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #fff;
}
.pp-sidebar-link.active {
  background: var(--pp-primary);
  color: #fff;
}
.pp-sidebar-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  z-index: 999;
}
@media (max-width: 991px) {
  .pp-sidebar {
    position: fixed;
    z-index: 1000;
    top: 0;
    left: 0;
    transform: translateX(-100%);
    transition: transform 0.2s ease;
  }
  .pp-sidebar.open {
    transform: translateX(0);
  }
}
</style>
