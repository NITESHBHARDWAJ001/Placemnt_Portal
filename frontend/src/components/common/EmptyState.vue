<script setup>
defineProps({
  icon: { type: String, default: "bi-inbox" },
  title: { type: String, default: "Nothing here yet" },
  message: { type: String, default: "" },
})
</script>

<template>
  <div class="text-center py-5">
    <i :class="['bi', icon]" class="display-4 pp-text-muted d-block mb-3"></i>
    <h6 class="fw-semibold mb-1">{{ title }}</h6>
    <p class="pp-text-muted small mb-3">{{ message }}</p>
    <slot />
  </div>
</template>
