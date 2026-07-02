<script setup>
import { onMounted, reactive, ref } from "vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import StatusBadge from "@/components/common/StatusBadge.vue"
import { useToast } from "@/composables/useToast"
import companyService from "@/services/company.service"

const toast = useToast()
const loading = ref(true)
const saving = ref(false)
const profile = reactive({
  company_name: "",
  website: "",
  industry: "",
  description: "",
  hr_name: "",
  hr_designation: "",
  approval_status: "PENDING",
})

async function load() {
  loading.value = true
  try {
    const { data } = await companyService.getProfile()
    Object.assign(profile, data.data)
  } finally {
    loading.value = false
  }
}
onMounted(load)

async function handleSave() {
  saving.value = true
  try {
    const { company_name, website, industry, description, hr_name, hr_designation } = profile
    await companyService.updateProfile({ company_name, website, industry, description, hr_name, hr_designation })
    toast.success("Profile updated successfully")
  } catch (e) {
    toast.error(e.response?.data?.message || "Update failed")
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="pp-page-title mb-0">Company Profile</h3>
      <StatusBadge v-if="!loading" :status="profile.approval_status" />
    </div>

    <div class="pp-card p-4" style="max-width: 720px">
      <SkeletonLoader v-if="loading" :rows="6" />
      <form v-else @submit.prevent="handleSave">
        <div class="row g-3">
          <div class="col-md-6">
            <label class="form-label small fw-semibold">Company Name</label>
            <input v-model="profile.company_name" type="text" class="form-control" required />
          </div>
          <div class="col-md-6">
            <label class="form-label small fw-semibold">Industry</label>
            <input v-model="profile.industry" type="text" class="form-control" placeholder="e.g. Software" />
          </div>
          <div class="col-md-6">
            <label class="form-label small fw-semibold">Website</label>
            <input v-model="profile.website" type="text" class="form-control" placeholder="https://" />
          </div>
          <div class="col-md-6">
            <label class="form-label small fw-semibold">HR Contact Name</label>
            <input v-model="profile.hr_name" type="text" class="form-control" />
          </div>
          <div class="col-md-6">
            <label class="form-label small fw-semibold">HR Designation</label>
            <input v-model="profile.hr_designation" type="text" class="form-control" />
          </div>
          <div class="col-12">
            <label class="form-label small fw-semibold">About the Company</label>
            <textarea v-model="profile.description" class="form-control" rows="4"></textarea>
          </div>
        </div>
        <button type="submit" class="btn btn-primary mt-4" :disabled="saving">
          <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
          Save Changes
        </button>
      </form>
    </div>
  </div>
</template>
