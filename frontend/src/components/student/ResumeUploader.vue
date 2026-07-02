<script setup>
import { onMounted, ref } from "vue"
import FileUpload from "@/components/common/FileUpload.vue"
import { useFileUpload } from "@/composables/useFileUpload"
import { useToast } from "@/composables/useToast"
import studentService from "@/services/student.service"
import { formatDate } from "@/utils/formatters"

const toast = useToast()
const { uploading, upload } = useFileUpload()
const resumes = ref([])

async function loadResumes() {
  const { data } = await studentService.listResumes()
  resumes.value = data.data
}
onMounted(loadResumes)

async function handleSelect(file) {
  try {
    await upload(() => studentService.uploadResume(file))
    toast.success("Resume uploaded successfully")
    loadResumes()
  } catch (e) {
    toast.error(e.response?.data?.message || "Upload failed")
  }
}

async function handleDelete(resumeId) {
  try {
    await studentService.deleteResume(resumeId)
    toast.success("Resume deleted")
    loadResumes()
  } catch (e) {
    toast.error(e.response?.data?.message || "Delete failed")
  }
}
</script>

<template>
  <div>
    <FileUpload label="Upload Resume (PDF)" @select="handleSelect" />
    <div v-if="uploading" class="small pp-text-muted mt-2">
      <span class="spinner-border spinner-border-sm me-2"></span>Uploading...
    </div>

    <ul class="list-unstyled mt-3 mb-0">
      <li v-for="r in resumes" :key="r.id" class="d-flex align-items-center justify-content-between border rounded-3 p-2 px-3 mb-2">
        <div class="d-flex align-items-center gap-2">
          <i class="bi bi-file-earmark-pdf text-danger fs-5"></i>
          <div>
            <div class="small fw-semibold">{{ r.file_name }}</div>
            <div class="small pp-text-muted">{{ formatDate(r.created_at) }} <span v-if="r.is_active" class="badge text-bg-success ms-1">Active</span></div>
          </div>
        </div>
        <button class="btn btn-sm btn-outline-danger" @click="handleDelete(r.id)"><i class="bi bi-trash"></i></button>
      </li>
    </ul>
  </div>
</template>
