<script setup>
defineProps({
  message: { type: String, default: "Something went wrong. Please try again." },
})
defineEmits(["retry"])
</script>

<template>
  <div class="text-center py-5">
    <i class="bi bi-exclamation-triangle display-4 text-danger d-block mb-3"></i>
    <p class="pp-text-muted mb-3">{{ message }}</p>
    <button class="btn btn-outline-danger btn-sm" @click="$emit('retry')">
      <i class="bi bi-arrow-clockwise me-1"></i> Retry
    </button>
  </div>
</template>
