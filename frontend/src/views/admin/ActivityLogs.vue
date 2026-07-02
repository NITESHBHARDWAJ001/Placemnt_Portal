<script setup>
import { onMounted, ref, watch } from "vue"
import Pagination from "@/components/common/Pagination.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import EmptyState from "@/components/common/EmptyState.vue"
import ErrorState from "@/components/common/ErrorState.vue"
import { usePagination } from "@/composables/usePagination"
import dashboardService from "@/services/dashboard.service"
import { formatDateTime } from "@/utils/formatters"

const { pagination, applyMeta } = usePagination()
const logs = ref([])
const loading = ref(true)
const error = ref(false)

async function load() {
  loading.value = true
  error.value = false
  try {
    const { data } = await dashboardService.activityLogs({ page: pagination.page, per_page: pagination.per_page })
    logs.value = data.data
    applyMeta(data.meta)
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => pagination.page, load)
</script>

<template>
  <div>
    <h3 class="pp-page-title mb-4">Activity Logs</h3>

    <div class="pp-card p-3">
      <SkeletonLoader v-if="loading" :rows="6" />
      <ErrorState v-else-if="error" @retry="load" />
      <EmptyState v-else-if="logs.length === 0" icon="bi-clock-history" title="No activity yet" />
      <ul v-else class="list-unstyled mb-0">
        <li v-for="log in logs" :key="log.id" class="pp-log-item d-flex gap-3 py-3 border-bottom">
          <div class="pp-log-icon"><i class="bi bi-activity"></i></div>
          <div>
            <div class="fw-semibold small">{{ log.actor_name }} — {{ log.action.replaceAll('_', ' ') }}</div>
            <div class="pp-text-muted small">{{ log.description }}</div>
            <div class="pp-text-muted small">{{ formatDateTime(log.created_at) }}</div>
          </div>
        </li>
      </ul>
      <div class="d-flex justify-content-end mt-3" v-if="!loading && logs.length">
        <Pagination :page="pagination.page" :total-pages="pagination.total_pages" @change="(p) => (pagination.page = p)" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.pp-log-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #eff6ff;
  color: var(--pp-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
</style>
