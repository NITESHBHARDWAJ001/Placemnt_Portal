<script setup>
import { onMounted, ref, watch } from "vue"
import { useRoute } from "vue-router"
import InterviewScheduler from "@/components/company/InterviewScheduler.vue"
import Pagination from "@/components/common/Pagination.vue"
import StatusBadge from "@/components/common/StatusBadge.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import EmptyState from "@/components/common/EmptyState.vue"
import ErrorState from "@/components/common/ErrorState.vue"
import { usePagination } from "@/composables/usePagination"
import { useToast } from "@/composables/useToast"
import applicationService from "@/services/application.service"
import interviewService from "@/services/interview.service"

const route = useRoute()
const toast = useToast()
const { pagination, applyMeta } = usePagination()

const applicants = ref([])
const loading = ref(true)
const error = ref(false)
const schedulingFor = ref(null)

async function load() {
  loading.value = true
  error.value = false
  try {
    const { data } = await applicationService.listForDrive(route.params.driveId, {
      page: pagination.page,
      per_page: pagination.per_page,
    })
    applicants.value = data.data
    applyMeta(data.meta)
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch(() => pagination.page, load)

async function updateStatus(applicant, status) {
  try {
    await applicationService.updateStatus(applicant.id, status)
    toast.success(`Application marked as ${status.toLowerCase()}`)
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Update failed")
  }
}

function openSchedule(applicant) {
  schedulingFor.value = applicant
}

async function submitInterview(payload) {
  try {
    await interviewService.schedule(schedulingFor.value.id, payload)
    toast.success("Interview scheduled")
    schedulingFor.value = null
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Scheduling failed")
  }
}
</script>

<template>
  <div>
    <h3 class="pp-page-title mb-4">Applicants</h3>

    <div class="pp-card p-3">
      <SkeletonLoader v-if="loading" :rows="5" />
      <ErrorState v-else-if="error" @retry="load" />
      <EmptyState v-else-if="applicants.length === 0" icon="bi-people" title="No applicants yet" />
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr class="small text-uppercase pp-text-muted">
              <th>Student</th>
              <th>Branch</th>
              <th>CGPA</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in applicants" :key="a.id">
              <td>
                <div class="fw-semibold">{{ a.student_name }}</div>
                <div class="small pp-text-muted">{{ a.student_email }}</div>
              </td>
              <td>{{ a.student_branch || "-" }}</td>
              <td>{{ a.student_cgpa ?? "-" }}</td>
              <td><StatusBadge :status="a.status" /></td>
              <td class="text-end">
                <div class="btn-group btn-group-sm">
                  <button class="btn btn-outline-primary" @click="updateStatus(a, 'SHORTLISTED')">Shortlist</button>
                  <button class="btn btn-outline-secondary" @click="openSchedule(a)">Interview</button>
                  <button class="btn btn-outline-success" @click="updateStatus(a, 'SELECTED')">Select</button>
                  <button class="btn btn-outline-danger" @click="updateStatus(a, 'REJECTED')">Reject</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="d-flex justify-content-end mt-3" v-if="!loading && applicants.length">
        <Pagination :page="pagination.page" :total-pages="pagination.total_pages" @change="(p) => (pagination.page = p)" />
      </div>
    </div>

    <div v-if="schedulingFor" class="pp-modal-backdrop">
      <div class="pp-card p-4" style="width: 480px; max-width: 95vw">
        <h5 class="fw-bold mb-3">Schedule Interview — {{ schedulingFor.student_name }}</h5>
        <InterviewScheduler @submit="submitInterview" @cancel="schedulingFor = null" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.pp-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2500;
}
</style>
