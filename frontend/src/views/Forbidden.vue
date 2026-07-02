<script setup>
import ErrorLayout from "@/layouts/ErrorLayout.vue"
</script>

<template>
  <ErrorLayout>
    <i class="bi bi-shield-lock display-1 text-danger"></i>
    <h1 class="fw-bold mt-3">403</h1>
    <p class="pp-text-muted mb-4">You don't have permission to access this page.</p>
    <router-link to="/login" class="btn btn-primary">Back to Login</router-link>
  </ErrorLayout>
</template>
