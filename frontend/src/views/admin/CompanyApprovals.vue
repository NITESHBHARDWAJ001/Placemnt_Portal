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
import { useToast } from "@/composables/useToast"
import { useConfirm } from "@/composables/useConfirm"
import companyService from "@/services/company.service"
import adminService from "@/services/admin.service"
import searchService from "@/services/search.service"
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
const reasonModal = ref({ visible: false, userId: null, reason: "" })

async function load() {
  loading.value = true
  error.value = false
  try {
    const { data } = await searchService.companies(debouncedSearch.value || "", {
      page: pagination.page,
      per_page: pagination.per_page,
      status: statusFilter.value || undefined,
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

function openBlacklist(company) {
  reasonModal.value = { visible: true, userId: company.user_id, reason: "" }
}

async function submitBlacklist() {
  if (!reasonModal.value.reason.trim()) {
    toast.error("Please provide a reason")
    return
  }
  try {
    await adminService.blacklistUser(reasonModal.value.userId, reasonModal.value.reason)
    toast.success("Company blacklisted")
    reasonModal.value.visible = false
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Action failed")
  }
}

async function handleRevoke(company) {
  const ok = await confirm({
    title: "Revoke blacklist?",
    message: `Restore access for ${company.company_name}.`,
    confirmText: "Revoke",
    variant: "primary",
  })
  if (!ok) return
  try {
    await adminService.revokeBlacklist(company.user_id)
    toast.success("Blacklist revoked")
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Action failed")
  }
}

async function handleDeactivate(company) {
  const ok = await confirm({
    title: "Deactivate account?",
    message: `${company.company_name} will not be able to log in.`,
    confirmText: "Deactivate",
    variant: "danger",
  })
  if (!ok) return
  try {
    await adminService.deactivateUser(company.user_id)
    toast.success("Account deactivated")
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Action failed")
  }
}

async function handleActivate(company) {
  try {
    await adminService.activateUser(company.user_id)
    toast.success("Account activated")
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
              <th>Account</th>
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
              <td>
                <span v-if="c.is_blacklisted" class="badge text-bg-danger">Blacklisted</span>
                <span v-else-if="!c.is_active" class="badge text-bg-secondary">Inactive</span>
                <span v-else class="badge text-bg-success">Active</span>
              </td>
              <td class="text-end">
                <template v-if="c.approval_status === 'PENDING'">
                  <button class="btn btn-sm btn-success me-1" @click="handleApprove(c)">
                    <i class="bi bi-check-lg"></i> Approve
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="handleReject(c)">
                    <i class="bi bi-x-lg"></i> Reject
                  </button>
                </template>
                <template v-else>
                  <button class="btn btn-sm btn-outline-danger me-1" @click="openBlacklist(c)">
                    <i class="bi bi-slash-circle"></i> Blacklist
                  </button>
                  <button class="btn btn-sm btn-outline-secondary me-1" @click="handleRevoke(c)">Revoke</button>
                  <button
                    v-if="c.is_active"
                    class="btn btn-sm btn-outline-warning"
                    @click="handleDeactivate(c)"
                  >
                    Deactivate
                  </button>
                  <button v-else class="btn btn-sm btn-outline-success" @click="handleActivate(c)">
                    Activate
                  </button>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="d-flex justify-content-end mt-3" v-if="!loading && companies.length">
        <Pagination :page="pagination.page" :total-pages="pagination.total_pages" @change="(p) => (pagination.page = p)" />
      </div>
    </div>

    <div v-if="reasonModal.visible" class="pp-modal-backdrop">
      <div class="pp-card p-4" style="width: 380px">
        <h6 class="fw-bold mb-3">Blacklist Reason</h6>
        <textarea v-model="reasonModal.reason" class="form-control mb-3" rows="3" placeholder="Reason for blacklisting..."></textarea>
        <div class="d-flex justify-content-end gap-2">
          <button class="btn btn-light" @click="reasonModal.visible = false">Cancel</button>
          <button class="btn btn-danger" @click="submitBlacklist">Blacklist</button>
        </div>
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
