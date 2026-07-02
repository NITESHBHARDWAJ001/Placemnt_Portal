<script setup>
import ErrorLayout from "@/layouts/ErrorLayout.vue"
</script>

<template>
  <ErrorLayout>
    <i class="bi bi-signpost-split display-1 text-primary"></i>
    <h1 class="fw-bold mt-3">404</h1>
    <p class="pp-text-muted mb-4">The page you're looking for doesn't exist.</p>
    <router-link to="/" class="btn btn-primary">Go Home</router-link>
  </ErrorLayout>
</template>
