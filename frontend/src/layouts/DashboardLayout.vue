<script setup>
import AppSidebar from "@/components/common/AppSidebar.vue"
import AppNavbar from "@/components/common/AppNavbar.vue"
</script>

<template>
  <div class="d-flex">
    <AppSidebar />
    <div class="flex-grow-1 min-vw-0">
      <AppNavbar />
      <main class="p-3 p-lg-4 pp-fade-in">
        <router-view />
      </main>
    </div>
  </div>
</template>
