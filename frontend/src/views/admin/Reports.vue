<script setup>
import { computed, onMounted, ref } from "vue"
import StatCard from "@/components/common/StatCard.vue"
import ChartCard from "@/components/common/ChartCard.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import ErrorState from "@/components/common/ErrorState.vue"
import dashboardService from "@/services/dashboard.service"

const loading = ref(true)
const error = ref(false)
const report = ref(null)

async function load() {
  loading.value = true
  error.value = false
  try {
    const { data } = await dashboardService.adminReports()
    report.value = data.data
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}
onMounted(load)

const branchLabels = computed(() => Object.keys(report.value?.students_by_branch || {}))
const branchData = computed(() => Object.values(report.value?.students_by_branch || {}))
const companyLabels = computed(() => Object.keys(report.value?.selections_by_company || {}))
const companyData = computed(() => Object.values(report.value?.selections_by_company || {}))
const trendLabels = computed(() => Object.keys(report.value?.monthly_application_trend || {}))
const trendData = computed(() => Object.values(report.value?.monthly_application_trend || {}))
</script>

<template>
  <div>
    <h3 class="pp-page-title mb-4">Reports &amp; Placement Statistics</h3>

    <SkeletonLoader v-if="loading" :rows="6" />
    <ErrorState v-else-if="error" @retry="load" />
    <template v-else>
      <div class="row g-3 mb-4">
        <div class="col-6 col-lg-4">
          <StatCard label="Total Students" :value="report.total_students" icon="bi-people" color="primary" />
        </div>
        <div class="col-6 col-lg-4">
          <StatCard label="Placed Students" :value="report.placed_students" icon="bi-trophy" color="success" />
        </div>
        <div class="col-6 col-lg-4">
          <StatCard label="Placement Rate" :value="`${report.placement_rate_percent}%`" icon="bi-graph-up-arrow" color="info" />
        </div>
      </div>

      <div class="row g-3">
        <div class="col-lg-6">
          <ChartCard title="Students by Branch" type="bar" :labels="branchLabels" :data="branchData" />
        </div>
        <div class="col-lg-6">
          <ChartCard title="Top Companies by Selections" type="bar" :labels="companyLabels" :data="companyData" />
        </div>
        <div class="col-12">
          <ChartCard title="Monthly Application Trend" type="bar" :labels="trendLabels" :data="trendData" />
        </div>
      </div>
    </template>
  </div>
</template>
