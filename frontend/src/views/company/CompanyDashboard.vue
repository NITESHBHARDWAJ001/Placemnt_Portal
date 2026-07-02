<script setup>
import { onMounted, ref } from "vue"
import StatCard from "@/components/common/StatCard.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import ErrorState from "@/components/common/ErrorState.vue"
import dashboardService from "@/services/dashboard.service"
import companyService from "@/services/company.service"
import StatusBadge from "@/components/common/StatusBadge.vue"

const loading = ref(true)
const error = ref(false)
const stats = ref(null)
const profile = ref(null)

async function load() {
  loading.value = true
  error.value = false
  try {
    const [statsRes, profileRes] = await Promise.all([dashboardService.company(), companyService.getProfile()])
    stats.value = statsRes.data.data
    profile.value = profileRes.data.data
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
    <h3 class="pp-page-title mb-4">Company Dashboard</h3>

    <SkeletonLoader v-if="loading" :rows="6" />
    <ErrorState v-else-if="error" @retry="load" />
    <template v-else>
      <div v-if="profile.approval_status !== 'APPROVED'" class="alert alert-warning d-flex align-items-center gap-2 mb-4">
        <i class="bi bi-hourglass-split fs-5"></i>
        <div>
          Your company profile is <StatusBadge :status="profile.approval_status" /> by the administrator.
          <span v-if="profile.approval_status === 'PENDING'">You'll be able to post drives once approved.</span>
        </div>
      </div>

      <div class="row g-3">
        <div class="col-6 col-lg-3">
          <StatCard label="Total Drives" :value="stats.total_drives" icon="bi-briefcase" color="primary" />
        </div>
        <div class="col-6 col-lg-3">
          <StatCard label="Total Applicants" :value="stats.total_applicants" icon="bi-people" color="info" />
        </div>
        <div class="col-6 col-lg-3">
          <StatCard label="Selections" :value="stats.total_selections" icon="bi-trophy" color="success" />
        </div>
        <div class="col-6 col-lg-3">
          <StatCard label="Upcoming Interviews" :value="stats.upcoming_interviews" icon="bi-calendar-event" color="warning" />
        </div>
      </div>
    </template>
  </div>
</template>
