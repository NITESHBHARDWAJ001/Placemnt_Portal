<script setup>
import { onMounted, ref } from "vue"
import StatusBadge from "@/components/common/StatusBadge.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import EmptyState from "@/components/common/EmptyState.vue"
import applicationService from "@/services/application.service"
import { formatDate } from "@/utils/formatters"

const loading = ref(true)
const selected = ref([])

async function load() {
  loading.value = true
  try {
    const { data } = await applicationService.myApplications({ per_page: 100 })
    selected.value = data.data.filter((a) => a.status === "SELECTED")
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>

<template>
  <div>
    <h3 class="pp-page-title mb-4">Placement History</h3>

    <SkeletonLoader v-if="loading" :rows="4" />
    <EmptyState v-else-if="selected.length === 0" icon="bi-trophy" title="No placements yet" message="Keep applying — your success story starts here" />
    <div v-else class="row g-3">
      <div class="col-md-6" v-for="a in selected" :key="a.id">
        <div class="pp-card p-4 d-flex align-items-center gap-3">
          <i class="bi bi-trophy-fill text-warning display-6"></i>
          <div>
            <h6 class="fw-bold mb-0">{{ a.drive_title }}</h6>
            <div class="small pp-text-muted">{{ a.company_name }}</div>
            <div class="small pp-text-muted">Selected on {{ formatDate(a.applied_at) }}</div>
          </div>
          <StatusBadge status="SELECTED" class="ms-auto" />
        </div>
      </div>
    </div>
  </div>
</template>
