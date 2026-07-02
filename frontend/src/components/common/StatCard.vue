<script setup>
defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  icon: { type: String, default: "bi-graph-up" },
  color: { type: String, default: "primary" },
})
</script>

<template>
  <div class="pp-card p-3 p-lg-4 h-100">
    <div class="d-flex align-items-center gap-3">
      <div class="pp-stat-icon" :class="`bg-${color}-subtle text-${color}`">
        <i :class="['bi', icon]"></i>
      </div>
      <div>
        <div class="pp-text-muted small">{{ label }}</div>
        <div class="fs-3 fw-bold">{{ value }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pp-stat-icon {
  width: 52px;
  height: 52px;
  border-radius: var(--pp-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
}
</style>
