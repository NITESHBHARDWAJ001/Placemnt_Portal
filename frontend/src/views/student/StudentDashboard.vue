<script setup>
import { onMounted, ref } from "vue"
import StatCard from "@/components/common/StatCard.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import ErrorState from "@/components/common/ErrorState.vue"
import dashboardService from "@/services/dashboard.service"
import studentService from "@/services/student.service"

const loading = ref(true)
const error = ref(false)
const stats = ref(null)
const profile = ref(null)

async function load() {
  loading.value = true
  error.value = false
  try {
    const [statsRes, profileRes] = await Promise.all([dashboardService.student(), studentService.getProfile()])
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
    <h3 class="pp-page-title mb-4">Student Dashboard</h3>

    <SkeletonLoader v-if="loading" :rows="6" />
    <ErrorState v-else-if="error" @retry="load" />
    <template v-else>
      <div v-if="profile.profile_completion_percent < 100" class="alert alert-info d-flex align-items-center gap-2 mb-4">
        <i class="bi bi-info-circle fs-5"></i>
        <div>
          Your profile is {{ profile.profile_completion_percent }}% complete.
          <router-link to="/student/profile" class="fw-semibold">Complete it</router-link> to improve your eligibility for drives.
        </div>
      </div>

      <div class="row g-3">
        <div class="col-6 col-lg-3">
          <StatCard label="Eligible Drives" :value="stats.eligible_drives" icon="bi-briefcase" color="primary" />
        </div>
        <div class="col-6 col-lg-3">
          <StatCard label="Applied" :value="stats.applied_drives" icon="bi-file-earmark-text" color="info" />
        </div>
        <div class="col-6 col-lg-3">
          <StatCard label="Selected" :value="stats.selected_drives" icon="bi-trophy" color="success" />
        </div>
        <div class="col-6 col-lg-3">
          <StatCard label="Rejected" :value="stats.rejected_drives" icon="bi-x-circle" color="danger" />
        </div>
      </div>
    </template>
  </div>
</template>
