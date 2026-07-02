<script setup>
defineProps({
  rows: { type: Number, default: 4 },
  height: { type: String, default: "18px" },
})
</script>

<template>
  <div>
    <div
      v-for="r in rows"
      :key="r"
      class="pp-skeleton mb-2"
      :style="{ height, width: r % 3 === 0 ? '70%' : '100%' }"
    ></div>
  </div>
</template>
