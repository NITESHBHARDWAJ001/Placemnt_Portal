import { useUiStore } from "@/stores/ui.store"

export function useConfirm() {
  const ui = useUiStore()
  return {
    confirm: (options) => ui.confirm(options),
  }
}
