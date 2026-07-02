<script setup>
import { useUiStore } from "@/stores/ui.store"

const ui = useUiStore()
</script>

<template>
  <div v-if="ui.confirmDialog.visible" class="pp-confirm-backdrop">
    <div class="pp-confirm-card pp-fade-in">
      <h5 class="fw-bold mb-2">{{ ui.confirmDialog.title }}</h5>
      <p class="pp-text-muted mb-4">{{ ui.confirmDialog.message }}</p>
      <div class="d-flex justify-content-end gap-2">
        <button class="btn btn-light" @click="ui.resolveConfirm(false)">Cancel</button>
        <button :class="`btn btn-${ui.confirmDialog.variant}`" @click="ui.resolveConfirm(true)">
          {{ ui.confirmDialog.confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pp-confirm-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
}
.pp-confirm-card {
  background: #fff;
  border-radius: var(--pp-radius);
  padding: 1.75rem;
  width: 360px;
  box-shadow: var(--pp-shadow-lg);
}
</style>
