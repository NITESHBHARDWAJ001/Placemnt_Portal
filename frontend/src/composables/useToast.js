import { useUiStore } from "@/stores/ui.store"

export function useToast() {
  const ui = useUiStore()
  return {
    success: (msg) => ui.success(msg),
    error: (msg) => ui.error(msg),
    info: (msg) => ui.info(msg),
  }
}
