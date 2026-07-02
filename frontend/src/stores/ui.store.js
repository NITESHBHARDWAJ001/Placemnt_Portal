import { defineStore } from "pinia"

let idCounter = 0

export const useUiStore = defineStore("ui", {
  state: () => ({
    toasts: [],
    globalLoading: false,
    confirmDialog: {
      visible: false,
      title: "",
      message: "",
      confirmText: "Confirm",
      variant: "danger",
      resolve: null,
    },
    sidebarCollapsed: false,
  }),

  actions: {
    pushToast({ message, type = "info", timeout = 3500 }) {
      const id = ++idCounter
      this.toasts.push({ id, message, type })
      if (timeout) {
        setTimeout(() => this.dismissToast(id), timeout)
      }
    },
    success(message) {
      this.pushToast({ message, type: "success" })
    },
    error(message) {
      this.pushToast({ message, type: "danger" })
    },
    info(message) {
      this.pushToast({ message, type: "info" })
    },
    dismissToast(id) {
      this.toasts = this.toasts.filter((t) => t.id !== id)
    },
    setLoading(value) {
      this.globalLoading = value
    },
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    confirm({ title = "Are you sure?", message = "", confirmText = "Confirm", variant = "danger" }) {
      this.confirmDialog = { visible: true, title, message, confirmText, variant, resolve: null }
      return new Promise((resolve) => {
        this.confirmDialog.resolve = resolve
      })
    },
    resolveConfirm(result) {
      if (this.confirmDialog.resolve) this.confirmDialog.resolve(result)
      this.confirmDialog.visible = false
    },
  },
})
