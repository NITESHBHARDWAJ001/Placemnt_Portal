<script setup>
import { reactive } from "vue"

const emit = defineEmits(["submit", "cancel"])

const form = reactive({
  round_number: 1,
  round_name: "",
  scheduled_at: "",
  mode: "ONLINE",
  location_or_link: "",
  interviewer_name: "",
})

function handleSubmit() {
  emit("submit", { ...form, scheduled_at: `${form.scheduled_at}:00` })
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <div class="row g-3">
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Round Number</label>
        <input v-model.number="form.round_number" type="number" min="1" class="form-control" required />
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Round Name</label>
        <input v-model="form.round_name" type="text" class="form-control" placeholder="e.g. Technical Round 1" />
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Date & Time</label>
        <input v-model="form.scheduled_at" type="datetime-local" class="form-control" required />
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Mode</label>
        <select v-model="form.mode" class="form-select">
          <option value="ONLINE">Online</option>
          <option value="OFFLINE">Offline</option>
        </select>
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Location / Meeting Link</label>
        <input v-model="form.location_or_link" type="text" class="form-control" />
      </div>
      <div class="col-md-6">
        <label class="form-label small fw-semibold">Interviewer</label>
        <input v-model="form.interviewer_name" type="text" class="form-control" />
      </div>
    </div>
    <div class="d-flex justify-content-end gap-2 mt-4">
      <button type="button" class="btn btn-light" @click="$emit('cancel')">Cancel</button>
      <button type="submit" class="btn btn-primary">Schedule Interview</button>
    </div>
  </form>
</template>
