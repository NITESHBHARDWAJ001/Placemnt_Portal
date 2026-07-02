<script setup>
import { onMounted, ref, watch } from "vue"
import DriveCard from "@/components/student/DriveCard.vue"
import SearchBar from "@/components/common/SearchBar.vue"
import Pagination from "@/components/common/Pagination.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import EmptyState from "@/components/common/EmptyState.vue"
import ErrorState from "@/components/common/ErrorState.vue"
import { usePagination } from "@/composables/usePagination"
import { useDebounce } from "@/composables/useDebounce"
import { useToast } from "@/composables/useToast"
import { useConfirm } from "@/composables/useConfirm"
import driveService from "@/services/drive.service"
import applicationService from "@/services/application.service"

const toast = useToast()
const { confirm } = useConfirm()
const { pagination, applyMeta } = usePagination()

const drives = ref([])
const appliedDriveIds = ref(new Set())
const loading = ref(true)
const error = ref(false)
const search = ref("")
const eligibleOnly = ref(false)
const debouncedSearch = useDebounce(search)

async function load() {
  loading.value = true
  error.value = false
  try {
    const [drivesRes, applicationsRes] = await Promise.all([
      driveService.listPublic({
        page: pagination.page,
        per_page: pagination.per_page,
        search: debouncedSearch.value || undefined,
        eligible_only: eligibleOnly.value || undefined,
      }),
      applicationService.myApplications({ per_page: 100 }),
    ])
    drives.value = drivesRes.data.data
    applyMeta(drivesRes.data.meta)
    appliedDriveIds.value = new Set(applicationsRes.data.data.map((a) => a.drive_id))
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch([debouncedSearch, eligibleOnly], () => {
  pagination.page = 1
  load()
})
watch(() => pagination.page, load)

async function handleApply(drive) {
  const ok = await confirm({
    title: "Apply to this drive?",
    message: `You're about to apply to "${drive.title}" at ${drive.company_name}.`,
    confirmText: "Apply",
    variant: "primary",
  })
  if (!ok) return
  try {
    await applicationService.apply(drive.id)
    toast.success("Application submitted successfully")
    load()
  } catch (e) {
    const message = e.response?.data?.message || "Application failed"
    const errors = e.response?.data?.errors
    toast.error(Array.isArray(errors) ? `${message}: ${errors.join(", ")}` : message)
  }
}
</script>

<template>
  <div>
    <h3 class="pp-page-title mb-4">Browse Drives</h3>

    <div class="pp-card p-3 mb-3">
      <div class="row g-2 align-items-center">
        <div class="col-md-8">
          <SearchBar v-model="search" placeholder="Search by title or role..." />
        </div>
        <div class="col-md-4">
          <div class="form-check">
            <input id="eligibleOnly" v-model="eligibleOnly" class="form-check-input" type="checkbox" />
            <label class="form-check-label small" for="eligibleOnly">Show eligible drives only</label>
          </div>
        </div>
      </div>
    </div>

    <SkeletonLoader v-if="loading" :rows="6" />
    <ErrorState v-else-if="error" @retry="load" />
    <EmptyState
      v-else-if="drives.length === 0"
      icon="bi-briefcase"
      title="No drives available"
      :message="eligibleOnly ? 'No drives match your eligibility right now — try turning off the filter' : 'Check back later for new opportunities'"
    />
    <template v-else>
      <div class="row g-3">
        <div class="col-md-6 col-xl-4" v-for="d in drives" :key="d.id">
          <DriveCard :drive="d" :applied="appliedDriveIds.has(d.id)" @apply="handleApply" />
        </div>
      </div>
      <div class="d-flex justify-content-end mt-4">
        <Pagination :page="pagination.page" :total-pages="pagination.total_pages" @change="(p) => (pagination.page = p)" />
      </div>
    </template>
  </div>
</template>
