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
import driveService from "@/services/drive.service"
import { formatCurrency, formatDate } from "@/utils/formatters"

const { pagination, applyMeta } = usePagination()
const toast = useToast()
const { confirm } = useConfirm()

const drives = ref([])
const loading = ref(true)
const error = ref(false)
const statusFilter = ref("PENDING")

async function load() {
  loading.value = true
  error.value = false
  try {
    const params = { page: pagination.page, per_page: pagination.per_page }
    const { data } =
      statusFilter.value === "PENDING"
        ? await driveService.listPending(params)
        : await driveService.listAll({ ...params, status: statusFilter.value || undefined })
    drives.value = data.data
    applyMeta(data.meta)
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(statusFilter, () => {
  pagination.page = 1
  load()
})
watch(() => pagination.page, load)

async function handleApprove(drive) {
  const ok = await confirm({ title: "Approve drive?", message: `"${drive.title}" will go live for students.`, confirmText: "Approve", variant: "primary" })
  if (!ok) return
  try {
    await driveService.approve(drive.id)
    toast.success("Drive approved")
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Action failed")
  }
}

async function handleReject(drive) {
  const ok = await confirm({ title: "Reject drive?", message: `"${drive.title}" will be rejected.`, confirmText: "Reject", variant: "danger" })
  if (!ok) return
  try {
    await driveService.reject(drive.id)
    toast.success("Drive rejected")
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Action failed")
  }
}
</script>

<template>
  <div>
    <h3 class="pp-page-title mb-4">Drive Approvals</h3>

    <div class="pp-card p-3 mb-3">
      <select v-model="statusFilter" class="form-select w-auto">
        <option value="PENDING">Pending</option>
        <option value="APPROVED">Approved</option>
        <option value="REJECTED">Rejected</option>
        <option value="">All</option>
      </select>
    </div>

    <div class="pp-card p-3">
      <SkeletonLoader v-if="loading" :rows="5" />
      <ErrorState v-else-if="error" @retry="load" />
      <EmptyState v-else-if="drives.length === 0" icon="bi-briefcase" title="No drives found" message="Try a different filter" />
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr class="small text-uppercase pp-text-muted">
              <th>Drive</th>
              <th>Company</th>
              <th>Package</th>
              <th>Deadline</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in drives" :key="d.id">
              <td class="fw-semibold">{{ d.title }}</td>
              <td>{{ d.company_name }}</td>
              <td>{{ formatCurrency(d.package_min) }} - {{ formatCurrency(d.package_max) }}</td>
              <td>{{ formatDate(d.application_deadline) }}</td>
              <td><StatusBadge :status="d.status" /></td>
              <td class="text-end">
                <template v-if="d.status === 'PENDING'">
                  <button class="btn btn-sm btn-success me-1" @click="handleApprove(d)"><i class="bi bi-check-lg"></i> Approve</button>
                  <button class="btn btn-sm btn-outline-danger" @click="handleReject(d)"><i class="bi bi-x-lg"></i> Reject</button>
                </template>
                <span v-else class="pp-text-muted small">No actions</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="d-flex justify-content-end mt-3" v-if="!loading && drives.length">
        <Pagination :page="pagination.page" :total-pages="pagination.total_pages" @change="(p) => (pagination.page = p)" />
      </div>
    </div>
  </div>
</template>
