<script setup>
import { computed } from "vue"

const props = defineProps({
  page: { type: Number, required: true },
  totalPages: { type: Number, required: true },
})
const emit = defineEmits(["change"])

const pages = computed(() => {
  const total = props.totalPages || 1
  const current = props.page
  const range = []
  const start = Math.max(1, current - 2)
  const end = Math.min(total, current + 2)
  for (let i = start; i <= end; i++) range.push(i)
  return range
})
</script>

<template>
  <nav v-if="totalPages > 1" aria-label="Pagination">
    <ul class="pagination pagination-sm mb-0">
      <li class="page-item" :class="{ disabled: page <= 1 }">
        <button class="page-link" @click="emit('change', page - 1)">
          <i class="bi bi-chevron-left"></i>
        </button>
      </li>
      <li v-for="p in pages" :key="p" class="page-item" :class="{ active: p === page }">
        <button class="page-link" @click="emit('change', p)">{{ p }}</button>
      </li>
      <li class="page-item" :class="{ disabled: page >= totalPages }">
        <button class="page-link" @click="emit('change', page + 1)">
          <i class="bi bi-chevron-right"></i>
        </button>
      </li>
    </ul>
  </nav>
</template>
