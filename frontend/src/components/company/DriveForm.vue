<script setup>
import { reactive, watch } from "vue"
import { BRANCHES, JOB_TYPES } from "@/utils/constants"

const props = defineProps({
  modelValue: { type: Object, default: null },
})
const emit = defineEmits(["submit", "cancel"])

const form = reactive({
  title: "",
  job_role: "",
  job_type: "FULL_TIME",
  description: "",
  location: "",
  package_min: null,
  package_max: null,
  min_cgpa: 0,
  max_backlogs: 0,
  allowed_branches: [],
  eligible_batch: null,
  application_deadline: "",
})

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      for (const key of Object.keys(form)) {
        if (val[key] !== undefined) form[key] = val[key]
      }
      form.application_deadline = val.application_deadline ? val.application_deadline.slice(0, 16) : ""
    }
  },
  { immediate: true }
)

function toggleBranch(branch) {
  const idx = form.allowed_branches.indexOf(branch)
  if (idx >= 0) form.allowed_branches.splice(idx, 1)
  else form.allowed_branches.push(branch)
}

function handleSubmit() {
  emit("submit", { ...form })
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <div class="row g-3">
      <div class="col-md-8">
        <label class="form-label small fw-semibold">Drive Title</label>
        <input v-model="form.title" type="text" class="form-control" required placeholder="e.g. Software Engineer Hiring" />
      </div>
      <div class="col-md-4">
        <label class="form-label small fw-semibold">Job Type</label>
        <select v-model="form.job_type" class="form-select">
          <option v-for="t in JOB_TYPES" :key="t" :value="t">{{ t.replaceAll('_', ' ') }}</option>
        </select>
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Job Role</label>
        <input v-model="form.job_role" type="text" class="form-control" placeholder="e.g. Backend Developer" />
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Location</label>
        <input v-model="form.location" type="text" class="form-control" placeholder="e.g. Bengaluru / Remote" />
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Package Min (LPA)</label>
        <input v-model.number="form.package_min" type="number" step="0.1" class="form-control" />
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Package Max (LPA)</label>
        <input v-model.number="form.package_max" type="number" step="0.1" class="form-control" />
      </div>
      <div class="col-md-4">
        <label class="form-label small fw-semibold">Minimum CGPA</label>
        <input v-model.number="form.min_cgpa" type="number" step="0.1" min="0" max="10" class="form-control" />
      </div>
      <div class="col-md-4">
        <label class="form-label small fw-semibold">Max Backlogs</label>
        <input v-model.number="form.max_backlogs" type="number" min="0" class="form-control" />
      </div>
      <div class="col-md-4">
        <label class="form-label small fw-semibold">Eligible Batch</label>
        <input v-model.number="form.eligible_batch" type="number" class="form-control" placeholder="e.g. 2026" />
      </div>
      <div class="col-12">
        <label class="form-label small fw-semibold">Allowed Branches</label>
        <div class="d-flex flex-wrap gap-2">
          <button
            v-for="b in BRANCHES"
            :key="b"
            type="button"
            class="btn btn-sm"
            :class="form.allowed_branches.includes(b) ? 'btn-primary' : 'btn-outline-secondary'"
            @click="toggleBranch(b)"
          >
            {{ b }}
          </button>
        </div>
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Application Deadline</label>
        <input v-model="form.application_deadline" type="datetime-local" class="form-control" required />
      </div>
      <div class="col-12">
        <label class="form-label small fw-semibold">Description</label>
        <textarea v-model="form.description" class="form-control" rows="3"></textarea>
      </div>
    </div>

    <div class="d-flex justify-content-end gap-2 mt-4">
      <button type="button" class="btn btn-light" @click="$emit('cancel')">Cancel</button>
      <button type="submit" class="btn btn-primary">Save Drive</button>
    </div>
  </form>
</template>
