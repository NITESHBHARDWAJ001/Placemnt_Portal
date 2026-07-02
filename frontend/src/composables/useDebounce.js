import { ref, watch } from "vue"

export function useDebounce(source, delay = 350) {
  const debounced = ref(source.value)
  let timeout = null

  watch(source, (value) => {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => {
      debounced.value = value
    }, delay)
  })

  return debounced
}
