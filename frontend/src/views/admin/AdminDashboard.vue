<script setup>
import { onMounted, ref, computed } from "vue"
import StatCard from "@/components/common/StatCard.vue"
import ChartCard from "@/components/common/ChartCard.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import ErrorState from "@/components/common/ErrorState.vue"
import dashboardService from "@/services/dashboard.service"

const loading = ref(true)
const error = ref(false)
const stats = ref(null)

async function load() {
  loading.value = true
  error.value = false
  try {
    const { data } = await dashboardService.admin()
    stats.value = data.data
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(load)

const appLabels = computed(() => Object.keys(stats.value?.applications_by_status || {}))
const appData = computed(() => Object.values(stats.value?.applications_by_status || {}))
const driveLabels = computed(() => Object.keys(stats.value?.drives_by_status || {}))
const driveData = computed(() => Object.values(stats.value?.drives_by_status || {}))
</script>

<template>
  <div>
    <h3 class="pp-page-title mb-4">Admin Dashboard</h3>

    <SkeletonLoader v-if="loading" :rows="6" />
    <ErrorState v-else-if="error" @retry="load" />
    <template v-else>
      <div class="row g-3 mb-4">
        <div class="col-6 col-lg-3">
          <StatCard label="Total Students" :value="stats.total_students" icon="bi-people" color="primary" />
        </div>
        <div class="col-6 col-lg-3">
          <StatCard label="Total Companies" :value="stats.total_companies" icon="bi-building" color="info" />
        </div>
        <div class="col-6 col-lg-3">
          <StatCard label="Pending Companies" :value="stats.pending_companies" icon="bi-hourglass-split" color="warning" />
        </div>
        <div class="col-6 col-lg-3">
          <StatCard label="Pending Drives" :value="stats.pending_drives" icon="bi-briefcase" color="warning" />
        </div>
        <div class="col-6 col-lg-3">
          <StatCard label="Total Applications" :value="stats.total_applications" icon="bi-file-earmark-text" color="primary" />
        </div>
        <div class="col-6 col-lg-3">
          <StatCard label="Total Selections" :value="stats.total_selections" icon="bi-trophy" color="success" />
        </div>
      </div>

      <div class="row g-3">
        <div class="col-lg-6">
          <ChartCard title="Applications by Status" type="doughnut" :labels="appLabels" :data="appData" />
        </div>
        <div class="col-lg-6">
          <ChartCard title="Drives by Status" type="bar" :labels="driveLabels" :data="driveData" />
        </div>
      </div>
    </template>
  </div>
</template>
