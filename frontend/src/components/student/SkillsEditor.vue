<script setup>
import { ref } from "vue"
import { useToast } from "@/composables/useToast"
import studentService from "@/services/student.service"

const props = defineProps({ skills: { type: Array, default: () => [] } })
const emit = defineEmits(["updated"])

const toast = useToast()
const newSkill = ref("")
const adding = ref(false)

async function addSkill() {
  if (!newSkill.value.trim()) return
  adding.value = true
  try {
    await studentService.addSkill(newSkill.value.trim())
    newSkill.value = ""
    emit("updated")
  } catch (e) {
    toast.error(e.response?.data?.message || "Could not add skill")
  } finally {
    adding.value = false
  }
}
</script>

<template>
  <div>
    <div class="d-flex flex-wrap gap-2 mb-3">
      <span v-for="s in skills" :key="s" class="badge text-bg-light border d-flex align-items-center gap-1 py-2 px-3">
        {{ s }}
      </span>
      <span v-if="skills.length === 0" class="pp-text-muted small">No skills added yet</span>
    </div>
    <div class="input-group" style="max-width: 320px">
      <input
        v-model="newSkill"
        type="text"
        class="form-control"
        placeholder="e.g. Python, React..."
        @keyup.enter="addSkill"
      />
      <button class="btn btn-outline-primary" :disabled="adding" @click="addSkill">
        <i class="bi bi-plus-lg"></i>
      </button>
    </div>
  </div>
</template>
