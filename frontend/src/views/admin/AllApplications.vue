<script setup>
import { onMounted, ref, watch } from "vue"
import SearchBar from "@/components/common/SearchBar.vue"
import Pagination from "@/components/common/Pagination.vue"
import StatusBadge from "@/components/common/StatusBadge.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import EmptyState from "@/components/common/EmptyState.vue"
import ErrorState from "@/components/common/ErrorState.vue"
import { usePagination } from "@/composables/usePagination"
import { useDebounce } from "@/composables/useDebounce"
import applicationService from "@/services/application.service"
import { formatDate } from "@/utils/formatters"

const { pagination, applyMeta } = usePagination()

const applications = ref([])
const loading = ref(true)
const error = ref(false)
const search = ref("")
const statusFilter = ref("")
const debouncedSearch = useDebounce(search)

async function load() {
  loading.value = true
  error.value = false
  try {
    const { data } = await applicationService.allApplications({
      page: pagination.page,
      per_page: pagination.per_page,
      search: debouncedSearch.value || undefined,
      status: statusFilter.value || undefined,
    })
    applications.value = data.data
    applyMeta(data.meta)
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch([debouncedSearch, statusFilter], () => {
  pagination.page = 1
  load()
})
watch(() => pagination.page, load)
</script>

<template>
  <div>
    <h3 class="pp-page-title mb-4">All Applications</h3>

    <div class="pp-card p-3 mb-3">
      <div class="row g-2 align-items-center">
        <div class="col-md-6">
          <SearchBar v-model="search" placeholder="Search by student name or email..." />
        </div>
        <div class="col-md-4">
          <select v-model="statusFilter" class="form-select">
            <option value="">All Statuses</option>
            <option value="APPLIED">Applied</option>
            <option value="SHORTLISTED">Shortlisted</option>
            <option value="INTERVIEW_SCHEDULED">Interview Scheduled</option>
            <option value="SELECTED">Selected</option>
            <option value="REJECTED">Rejected</option>
            <option value="WITHDRAWN">Withdrawn</option>
          </select>
        </div>
      </div>
    </div>

    <div class="pp-card p-3">
      <SkeletonLoader v-if="loading" :rows="5" />
      <ErrorState v-else-if="error" @retry="load" />
      <EmptyState v-else-if="applications.length === 0" icon="bi-file-earmark-text" title="No applications found" />
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr class="small text-uppercase pp-text-muted">
              <th>Student</th>
              <th>Drive</th>
              <th>Company</th>
              <th>Applied On</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in applications" :key="a.id">
              <td>
                <div class="fw-semibold">{{ a.student_name }}</div>
                <div class="small pp-text-muted">{{ a.student_email }}</div>
              </td>
              <td>{{ a.drive_title }}</td>
              <td>{{ a.company_name }}</td>
              <td>{{ formatDate(a.applied_at) }}</td>
              <td><StatusBadge :status="a.status" /></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="d-flex justify-content-end mt-3" v-if="!loading && applications.length">
        <Pagination :page="pagination.page" :total-pages="pagination.total_pages" @change="(p) => (pagination.page = p)" />
      </div>
    </div>
  </div>
</template>
