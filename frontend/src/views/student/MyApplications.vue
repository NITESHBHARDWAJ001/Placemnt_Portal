<script setup>
import { onMounted, ref, watch } from "vue"
import Pagination from "@/components/common/Pagination.vue"
import StatusBadge from "@/components/common/StatusBadge.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import EmptyState from "@/components/common/EmptyState.vue"
import ErrorState from "@/components/common/ErrorState.vue"
import { usePagination } from "@/composables/usePagination"
import { useToast } from "@/composables/useToast"
import { useConfirm } from "@/composables/useConfirm"
import applicationService from "@/services/application.service"
import { formatDate } from "@/utils/formatters"

const toast = useToast()
const { confirm } = useConfirm()
const { pagination, applyMeta } = usePagination()

const applications = ref([])
const loading = ref(true)
const error = ref(false)
const exporting = ref(false)

async function load() {
  loading.value = true
  error.value = false
  try {
    const { data } = await applicationService.myApplications({ page: pagination.page, per_page: pagination.per_page })
    applications.value = data.data
    applyMeta(data.meta)
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch(() => pagination.page, load)

async function handleWithdraw(app) {
  const ok = await confirm({
    title: "Withdraw application?",
    message: `Withdraw your application to "${app.drive_title}"?`,
    confirmText: "Withdraw",
    variant: "danger",
  })
  if (!ok) return
  try {
    await applicationService.withdraw(app.id)
    toast.success("Application withdrawn")
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Withdraw failed")
  }
}

async function handleExport() {
  exporting.value = true
  try {
    await applicationService.triggerExport()
    toast.success("Export started — you'll get a notification when it's ready to download")
  } catch (e) {
    toast.error(e.response?.data?.message || "Could not start export")
  } finally {
    exporting.value = false
  }
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="pp-page-title mb-0">My Applications</h3>
      <button
        class="btn btn-outline-primary btn-sm"
        :disabled="exporting || applications.length === 0"
        @click="handleExport"
      >
        <span v-if="exporting" class="spinner-border spinner-border-sm me-1"></span>
        <i v-else class="bi bi-download me-1"></i>
        Export CSV
      </button>
    </div>

    <div class="pp-card p-3">
      <SkeletonLoader v-if="loading" :rows="5" />
      <ErrorState v-else-if="error" @retry="load" />
      <EmptyState v-else-if="applications.length === 0" icon="bi-file-earmark-text" title="No applications yet" message="Browse drives and apply to get started">
        <router-link to="/student/drives" class="btn btn-primary btn-sm">Browse Drives</router-link>
      </EmptyState>
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr class="small text-uppercase pp-text-muted">
              <th>Drive</th>
              <th>Company</th>
              <th>Applied On</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in applications" :key="a.id">
              <td class="fw-semibold">{{ a.drive_title }}</td>
              <td>{{ a.company_name }}</td>
              <td>{{ formatDate(a.applied_at) }}</td>
              <td><StatusBadge :status="a.status" /></td>
              <td class="text-end">
                <button
                  v-if="['APPLIED', 'SHORTLISTED'].includes(a.status)"
                  class="btn btn-sm btn-outline-danger"
                  @click="handleWithdraw(a)"
                >
                  Withdraw
                </button>
              </td>
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
