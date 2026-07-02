<script setup>
import { useUiStore } from "@/stores/ui.store"

const ui = useUiStore()

const iconFor = (type) => ({
  success: "bi-check-circle-fill",
  danger: "bi-exclamation-octagon-fill",
  info: "bi-info-circle-fill",
  warning: "bi-exclamation-triangle-fill",
}[type] || "bi-info-circle-fill")
</script>

<template>
  <div class="pp-toast-stack">
    <transition-group name="pp-toast">
      <div
        v-for="toast in ui.toasts"
        :key="toast.id"
        class="toast show align-items-center text-bg-light border shadow-sm mb-2"
        :class="`border-${toast.type}`"
      >
        <div class="d-flex">
          <div class="toast-body d-flex align-items-center gap-2">
            <i :class="['bi', iconFor(toast.type), `text-${toast.type}`]"></i>
            <span>{{ toast.message }}</span>
          </div>
          <button type="button" class="btn-close me-2 m-auto" @click="ui.dismissToast(toast.id)"></button>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<style scoped>
.pp-toast-stack {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 2000;
  min-width: 280px;
}
.pp-toast-enter-active,
.pp-toast-leave-active {
  transition: all 0.25s ease;
}
.pp-toast-enter-from,
.pp-toast-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
