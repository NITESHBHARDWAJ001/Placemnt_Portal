<script setup>
import { ref } from "vue"

const props = defineProps({
  accept: { type: String, default: ".pdf" },
  label: { type: String, default: "Upload file" },
})
const emit = defineEmits(["select"])

const fileName = ref("")
const inputRef = ref(null)

function onChange(e) {
  const file = e.target.files[0]
  if (file) {
    fileName.value = file.name
    emit("select", file)
  }
}

function trigger() {
  inputRef.value.click()
}
</script>

<template>
  <div>
    <input ref="inputRef" type="file" class="d-none" :accept="accept" @change="onChange" />
    <button type="button" class="btn btn-outline-primary d-flex align-items-center gap-2" @click="trigger">
      <i class="bi bi-cloud-arrow-up"></i> {{ label }}
    </button>
    <div v-if="fileName" class="small pp-text-muted mt-2">
      <i class="bi bi-file-earmark-pdf text-danger me-1"></i>{{ fileName }}
    </div>
  </div>
</template>
