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
import studentService from "@/services/student.service"
import adminService from "@/services/admin.service"

const { pagination, applyMeta } = usePagination()
const toast = useToast()
const { confirm } = useConfirm()

const students = ref([])
const loading = ref(true)
const error = ref(false)
const search = ref("")
const debouncedSearch = useDebounce(search)
const reasonModal = ref({ visible: false, userId: null, reason: "" })

async function load() {
  loading.value = true
  error.value = false
  try {
    const { data } = await studentService.listStudents({
      page: pagination.page,
      per_page: pagination.per_page,
      search: debouncedSearch.value || undefined,
    })
    students.value = data.data
    applyMeta(data.meta)
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(debouncedSearch, () => {
  pagination.page = 1
  load()
})
watch(() => pagination.page, load)

function openBlacklist(student) {
  reasonModal.value = { visible: true, userId: student.user_id, reason: "" }
}

async function submitBlacklist() {
  if (!reasonModal.value.reason.trim()) {
    toast.error("Please provide a reason")
    return
  }
  try {
    await adminService.blacklistUser(reasonModal.value.userId, reasonModal.value.reason)
    toast.success("Student blacklisted")
    reasonModal.value.visible = false
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Action failed")
  }
}

async function handleRevoke(student) {
  const ok = await confirm({ title: "Revoke blacklist?", message: `Restore access for ${student.name}.`, confirmText: "Revoke", variant: "primary" })
  if (!ok) return
  try {
    await adminService.revokeBlacklist(student.user_id)
    toast.success("Blacklist revoked")
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Action failed")
  }
}

async function handleDeactivate(student) {
  const ok = await confirm({ title: "Deactivate account?", message: `${student.name} will not be able to log in.`, confirmText: "Deactivate", variant: "danger" })
  if (!ok) return
  try {
    await adminService.deactivateUser(student.user_id)
    toast.success("Account deactivated")
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Action failed")
  }
}
</script>

<template>
  <div>
    <h3 class="pp-page-title mb-4">Student Management</h3>

    <div class="pp-card p-3 mb-3">
      <SearchBar v-model="search" placeholder="Search by name, email or branch..." />
    </div>

    <div class="pp-card p-3">
      <SkeletonLoader v-if="loading" :rows="5" />
      <ErrorState v-else-if="error" @retry="load" />
      <EmptyState v-else-if="students.length === 0" icon="bi-people" title="No students found" />
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr class="small text-uppercase pp-text-muted">
              <th>Name</th>
              <th>Email</th>
              <th>Branch</th>
              <th>CGPA</th>
              <th>Placement</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in students" :key="s.id">
              <td class="fw-semibold">{{ s.name }}</td>
              <td>{{ s.email }}</td>
              <td>{{ s.branch || "-" }}</td>
              <td>{{ s.cgpa ?? "-" }}</td>
              <td><StatusBadge :status="s.placement_status" /></td>
              <td class="text-end">
                <button class="btn btn-sm btn-outline-danger me-1" @click="openBlacklist(s)">
                  <i class="bi bi-slash-circle"></i> Blacklist
                </button>
                <button class="btn btn-sm btn-outline-secondary me-1" @click="handleRevoke(s)">Revoke</button>
                <button class="btn btn-sm btn-outline-warning" @click="handleDeactivate(s)">Deactivate</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="d-flex justify-content-end mt-3" v-if="!loading && students.length">
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
