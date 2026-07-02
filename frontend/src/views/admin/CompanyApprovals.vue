<script setup>
import { onMounted, reactive, ref, watch } from "vue"
import SearchBar from "@/components/common/SearchBar.vue"
import Pagination from "@/components/common/Pagination.vue"
import StatusBadge from "@/components/common/StatusBadge.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import EmptyState from "@/components/common/EmptyState.vue"
import ErrorState from "@/components/common/ErrorState.vue"
import { usePagination } from "@/composables/usePagination"
import { useDebounce } from "@/composables/useDebounce"
import { useToast } from "@/composables/useToast"
import { useConfirm } from "@/composables/useConfirm"
import companyService from "@/services/company.service"
import { formatDate } from "@/utils/formatters"

const { pagination, applyMeta } = usePagination()
const toast = useToast()
const { confirm } = useConfirm()

const companies = ref([])
const loading = ref(true)
const error = ref(false)
const search = ref("")
const statusFilter = ref("PENDING")
const debouncedSearch = useDebounce(search)

async function load() {
  loading.value = true
  error.value = false
  try {
    const { data } = await companyService.listCompanies({
      page: pagination.page,
      per_page: pagination.per_page,
      status: statusFilter.value || undefined,
      search: debouncedSearch.value || undefined,
    })
    companies.value = data.data
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

async function handleApprove(company) {
  const ok = await confirm({
    title: "Approve company?",
    message: `${company.company_name} will be able to create placement drives.`,
    confirmText: "Approve",
    variant: "primary",
  })
  if (!ok) return
  try {
    await companyService.approve(company.id)
    toast.success("Company approved")
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Action failed")
  }
}

async function handleReject(company) {
  const ok = await confirm({
    title: "Reject company?",
    message: `${company.company_name}'s registration will be rejected.`,
    confirmText: "Reject",
    variant: "danger",
  })
  if (!ok) return
  try {
    await companyService.reject(company.id)
    toast.success("Company rejected")
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Action failed")
  }
}
</script>

<template>
  <div>
    <h3 class="pp-page-title mb-4">Company Approvals</h3>

    <div class="pp-card p-3 mb-3">
      <div class="row g-2 align-items-center">
        <div class="col-md-6">
          <SearchBar v-model="search" placeholder="Search by company name or email..." />
        </div>
        <div class="col-md-4">
          <select v-model="statusFilter" class="form-select">
            <option value="">All Statuses</option>
            <option value="PENDING">Pending</option>
            <option value="APPROVED">Approved</option>
            <option value="REJECTED">Rejected</option>
          </select>
        </div>
      </div>
    </div>

    <div class="pp-card p-3">
      <SkeletonLoader v-if="loading" :rows="5" />
      <ErrorState v-else-if="error" @retry="load" />
      <EmptyState
        v-else-if="companies.length === 0"
        icon="bi-building"
        title="No companies found"
        message="Try adjusting your filters"
      />
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr class="small text-uppercase pp-text-muted">
              <th>Company</th>
              <th>HR Contact</th>
              <th>Email</th>
              <th>Registered</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in companies" :key="c.id">
              <td class="fw-semibold">{{ c.company_name }}</td>
              <td>{{ c.hr_name || "-" }}</td>
              <td>{{ c.email }}</td>
              <td>{{ formatDate(c.created_at) }}</td>
              <td><StatusBadge :status="c.approval_status" /></td>
              <td class="text-end">
                <template v-if="c.approval_status === 'PENDING'">
                  <button class="btn btn-sm btn-success me-1" @click="handleApprove(c)">
                    <i class="bi bi-check-lg"></i> Approve
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="handleReject(c)">
                    <i class="bi bi-x-lg"></i> Reject
                  </button>
                </template>
                <span v-else class="pp-text-muted small">No actions</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="d-flex justify-content-end mt-3" v-if="!loading && companies.length">
        <Pagination :page="pagination.page" :total-pages="pagination.total_pages" @change="(p) => (pagination.page = p)" />
      </div>
    </div>
  </div>
</template>
