import { reactive } from "vue"

export function usePagination(initial = {}) {
  const pagination = reactive({
    page: 1,
    per_page: 10,
    total: 0,
    total_pages: 0,
    has_next: false,
    has_prev: false,
    ...initial,
  })

  function applyMeta(meta) {
    if (!meta) return
    Object.assign(pagination, meta)
  }

  function goToPage(page) {
    pagination.page = page
  }

  return { pagination, applyMeta, goToPage }
}
