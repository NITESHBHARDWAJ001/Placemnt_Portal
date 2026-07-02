<script setup>
import { onMounted, ref } from "vue"
import StatusBadge from "@/components/common/StatusBadge.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import EmptyState from "@/components/common/EmptyState.vue"
import ErrorState from "@/components/common/ErrorState.vue"
import interviewService from "@/services/interview.service"
import { formatDateTime } from "@/utils/formatters"

const interviews = ref([])
const loading = ref(true)
const error = ref(false)

async function load() {
  loading.value = true
  error.value = false
  try {
    const { data } = await interviewService.listForCompany()
    interviews.value = data.data
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>

<template>
  <div>
    <h3 class="pp-page-title mb-4">Interview Schedule</h3>

    <div class="pp-card p-3">
      <SkeletonLoader v-if="loading" :rows="5" />
      <ErrorState v-else-if="error" @retry="load" />
      <EmptyState v-else-if="interviews.length === 0" icon="bi-calendar-event" title="No interviews scheduled" />
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr class="small text-uppercase pp-text-muted">
              <th>Round</th>
              <th>Scheduled At</th>
              <th>Mode</th>
              <th>Interviewer</th>
              <th>Status</th>
              <th>Result</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="i in interviews" :key="i.id">
              <td>{{ i.round_number }} — {{ i.round_name || "Round" }}</td>
              <td>{{ formatDateTime(i.scheduled_at) }}</td>
              <td>{{ i.mode }}</td>
              <td>{{ i.interviewer_name || "-" }}</td>
              <td><StatusBadge :status="i.status" /></td>
              <td><StatusBadge :status="i.result" /></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
