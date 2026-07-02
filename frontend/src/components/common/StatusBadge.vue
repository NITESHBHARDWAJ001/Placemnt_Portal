<script setup>
import { computed } from "vue"
import { STATUS_BADGE_MAP } from "@/utils/constants"
import { formatStatusLabel } from "@/utils/formatters"

const props = defineProps({ status: { type: String, required: true } })
const variant = computed(() => STATUS_BADGE_MAP[props.status] || "secondary")
</script>

<template>
  <span class="badge" :class="`text-bg-${variant}`">{{ formatStatusLabel(status) }}</span>
</template>
