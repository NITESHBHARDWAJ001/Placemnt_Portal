<script setup>
import { reactive, watch } from "vue"
import { BRANCHES } from "@/utils/constants"

const props = defineProps({ modelValue: { type: Object, required: true } })
const emit = defineEmits(["submit"])

const form = reactive({
  phone: "",
  dob: "",
  gender: "",
  address: "",
  degree: "",
  branch: "",
  batch_year: null,
  cgpa: null,
  backlog_count: 0,
  linkedin_url: "",
  github_url: "",
  portfolio_url: "",
})

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      for (const key of Object.keys(form)) {
        if (val[key] !== undefined) form[key] = val[key]
      }
    }
  },
  { immediate: true }
)

function handleSubmit() {
  emit("submit", { ...form })
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <h6 class="fw-semibold mb-3">Personal Details</h6>
    <div class="row g-3 mb-4">
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Phone</label>
        <input v-model="form.phone" type="text" class="form-control" />
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Date of Birth</label>
        <input v-model="form.dob" type="date" class="form-control" />
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Gender</label>
        <select v-model="form.gender" class="form-select">
          <option value="">Select</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Address</label>
        <input v-model="form.address" type="text" class="form-control" />
      </div>
    </div>

    <h6 class="fw-semibold mb-3">Education Details</h6>
    <div class="row g-3 mb-4">
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Degree</label>
        <input v-model="form.degree" type="text" class="form-control" placeholder="e.g. B.Tech" />
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Branch</label>
        <select v-model="form.branch" class="form-select">
          <option value="">Select branch</option>
          <option v-for="b in BRANCHES" :key="b" :value="b">{{ b }}</option>
        </select>
      </div>
      <div class="col-md-4">
        <label class="form-label small fw-semibold">Batch Year</label>
        <input v-model.number="form.batch_year" type="number" class="form-control" placeholder="e.g. 2026" />
      </div>
      <div class="col-md-4">
        <label class="form-label small fw-semibold">CGPA</label>
        <input v-model.number="form.cgpa" type="number" step="0.01" min="0" max="10" class="form-control" />
      </div>
      <div class="col-md-4">
        <label class="form-label small fw-semibold">Backlogs</label>
        <input v-model.number="form.backlog_count" type="number" min="0" class="form-control" />
      </div>
    </div>

    <h6 class="fw-semibold mb-3">Links</h6>
    <div class="row g-3 mb-4">
      <div class="col-md-4">
        <label class="form-label small fw-semibold">LinkedIn</label>
        <input v-model="form.linkedin_url" type="text" class="form-control" />
      </div>
      <div class="col-md-4">
        <label class="form-label small fw-semibold">GitHub</label>
        <input v-model="form.github_url" type="text" class="form-control" />
      </div>
      <div class="col-md-4">
        <label class="form-label small fw-semibold">Portfolio</label>
        <input v-model="form.portfolio_url" type="text" class="form-control" />
      </div>
    </div>

    <button type="submit" class="btn btn-primary">Save Profile</button>
  </form>
</template>
