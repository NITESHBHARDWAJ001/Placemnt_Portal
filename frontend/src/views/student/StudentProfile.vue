<script setup>
import { onMounted, ref } from "vue"
import ProfileForm from "@/components/student/ProfileForm.vue"
import SkillsEditor from "@/components/student/SkillsEditor.vue"
import ResumeUploader from "@/components/student/ResumeUploader.vue"
import SkeletonLoader from "@/components/common/SkeletonLoader.vue"
import { useToast } from "@/composables/useToast"
import studentService from "@/services/student.service"

const toast = useToast()
const loading = ref(true)
const profile = ref(null)

async function load() {
  loading.value = true
  try {
    const { data } = await studentService.getProfile()
    profile.value = data.data
  } finally {
    loading.value = false
  }
}
onMounted(load)

async function handleSave(payload) {
  try {
    const { data } = await studentService.updateProfile(payload)
    profile.value = data.data
    toast.success("Profile updated successfully")
  } catch (e) {
    toast.error(e.response?.data?.message || "Update failed")
  }
}
</script>

<template>
  <div>
    <h3 class="pp-page-title mb-4">My Profile</h3>

    <SkeletonLoader v-if="loading" :rows="8" />
    <div v-else class="row g-3">
      <div class="col-lg-8">
        <div class="pp-card p-4">
          <ProfileForm :model-value="profile" @submit="handleSave" />
        </div>
      </div>
      <div class="col-lg-4">
        <div class="pp-card p-4 mb-3">
          <h6 class="fw-semibold mb-2">Profile Completion</h6>
          <div class="progress mb-1" style="height: 8px">
            <div class="progress-bar bg-primary" :style="{ width: profile.profile_completion_percent + '%' }"></div>
          </div>
          <div class="small pp-text-muted">{{ profile.profile_completion_percent }}% complete</div>
        </div>
        <div class="pp-card p-4 mb-3">
          <h6 class="fw-semibold mb-3">Skills</h6>
          <SkillsEditor :skills="profile.skills" @updated="load" />
        </div>
        <div class="pp-card p-4">
          <h6 class="fw-semibold mb-3">Resume</h6>
          <ResumeUploader />
        </div>
      </div>
    </div>
  </div>
</template>
