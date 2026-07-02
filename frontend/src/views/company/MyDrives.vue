<script setup>
import { onMounted, ref, watch } from "vue"
import { useRouter } from "vue-router"
import DriveForm from "@/components/company/DriveForm.vue"
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

const router = useRouter()
const toast = useToast()
const { confirm } = useConfirm()
const { pagination, applyMeta } = usePagination()

const drives = ref([])
const loading = ref(true)
const error = ref(false)
const showForm = ref(false)
const editing = ref(null)

async function load() {
  loading.value = true
  error.value = false
  try {
    const { data } = await driveService.listMine({ page: pagination.page, per_page: pagination.per_page })
    drives.value = data.data
    applyMeta(data.meta)
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch(() => pagination.page, load)

function openCreate() {
  editing.value = null
  showForm.value = true
}
function openEdit(drive) {
  editing.value = drive
  showForm.value = true
}

async function handleSubmit(payload) {
  const body = { ...payload, application_deadline: `${payload.application_deadline}:00` }
  try {
    if (editing.value) {
      await driveService.update(editing.value.id, body)
      toast.success("Drive updated and resubmitted for approval")
    } else {
      await driveService.create(body)
      toast.success("Drive created and submitted for approval")
    }
    showForm.value = false
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Save failed")
  }
}

async function handleDelete(drive) {
  const ok = await confirm({ title: "Delete drive?", message: `"${drive.title}" and its applications will be permanently removed.`, confirmText: "Delete", variant: "danger" })
  if (!ok) return
  try {
    await driveService.remove(drive.id)
    toast.success("Drive deleted")
    load()
  } catch (e) {
    toast.error(e.response?.data?.message || "Delete failed")
  }
}

function viewApplicants(drive) {
  router.push({ name: "company-drive-applicants", params: { driveId: drive.id } })
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="pp-page-title mb-0">My Drives</h3>
      <button class="btn btn-primary" @click="openCreate"><i class="bi bi-plus-lg me-1"></i>New Drive</button>
    </div>

    <div class="pp-card p-3">
      <SkeletonLoader v-if="loading" :rows="5" />
      <ErrorState v-else-if="error" @retry="load" />
      <EmptyState v-else-if="drives.length === 0" icon="bi-briefcase" title="No drives yet" message="Create your first placement drive to get started">
        <button class="btn btn-primary btn-sm" @click="openCreate">Create Drive</button>
      </EmptyState>
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr class="small text-uppercase pp-text-muted">
              <th>Title</th>
              <th>Package</th>
              <th>Deadline</th>
              <th>Applicants</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in drives" :key="d.id">
              <td class="fw-semibold">{{ d.title }}</td>
              <td>{{ formatCurrency(d.package_min) }} - {{ formatCurrency(d.package_max) }}</td>
              <td>{{ formatDate(d.application_deadline) }}</td>
              <td>
                <button class="btn btn-sm btn-outline-primary" @click="viewApplicants(d)">
                  {{ d.applicant_count }} <i class="bi bi-people ms-1"></i>
                </button>
              </td>
              <td><StatusBadge :status="d.status" /></td>
              <td class="text-end">
                <button class="btn btn-sm btn-outline-secondary me-1" @click="openEdit(d)"><i class="bi bi-pencil"></i></button>
                <button class="btn btn-sm btn-outline-danger" @click="handleDelete(d)"><i class="bi bi-trash"></i></button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="d-flex justify-content-end mt-3" v-if="!loading && drives.length">
        <Pagination :page="pagination.page" :total-pages="pagination.total_pages" @change="(p) => (pagination.page = p)" />
      </div>
    </div>

    <div v-if="showForm" class="pp-modal-backdrop">
      <div class="pp-card p-4 pp-modal-panel">
        <h5 class="fw-bold mb-3">{{ editing ? "Edit Drive" : "New Placement Drive" }}</h5>
        <DriveForm :model-value="editing" @submit="handleSubmit" @cancel="showForm = false" />
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
  padding: 1rem;
}
.pp-modal-panel {
  width: 100%;
  max-width: 720px;
  max-height: 90vh;
  overflow-y: auto;
}
</style>
