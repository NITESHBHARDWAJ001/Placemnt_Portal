<script setup>
import { ref } from "vue"
import StatusBadge from "@/components/common/StatusBadge.vue"
import { formatCurrency, formatDate } from "@/utils/formatters"
import { useEligibility } from "@/composables/useEligibility"

const props = defineProps({
  drive: { type: Object, required: true },
  applied: { type: Boolean, default: false },
})
const emit = defineEmits(["apply"])

const { checking, result, check } = useEligibility()
const expanded = ref(false)

async function toggleEligibility() {
  expanded.value = !expanded.value
  if (expanded.value && !result.value) {
    await check(props.drive.id)
  }
}
</script>

<template>
  <div class="pp-card p-4 h-100 d-flex flex-column">
    <div class="d-flex justify-content-between align-items-start mb-2">
      <div>
        <h6 class="fw-bold mb-0">{{ drive.title }}</h6>
        <div class="small pp-text-muted">{{ drive.company_name }}</div>
      </div>
      <span class="badge text-bg-light border">{{ drive.job_type.replaceAll('_', ' ') }}</span>
    </div>

    <div class="small pp-text-muted mb-3">{{ drive.job_role }} · {{ drive.location || "Location TBD" }}</div>

    <div class="d-flex flex-wrap gap-3 small mb-3">
      <div><i class="bi bi-cash-coin text-success me-1"></i>{{ formatCurrency(drive.package_min) }} - {{ formatCurrency(drive.package_max) }}</div>
      <div><i class="bi bi-calendar-event text-danger me-1"></i>Apply by {{ formatDate(drive.application_deadline) }}</div>
    </div>

    <button class="btn btn-sm btn-outline-secondary mb-2 align-self-start" @click="toggleEligibility">
      <span v-if="checking" class="spinner-border spinner-border-sm me-1"></span>
      Check Eligibility
    </button>

    <div v-if="expanded && result" class="mb-3 small">
      <div v-if="result.eligible" class="text-success"><i class="bi bi-check-circle-fill me-1"></i>You are eligible for this drive</div>
      <div v-else class="text-danger">
        <div><i class="bi bi-x-circle-fill me-1"></i>Not eligible:</div>
        <ul class="mb-0 ps-3">
          <li v-for="r in result.reasons" :key="r">{{ r }}</li>
        </ul>
      </div>
    </div>

    <div class="mt-auto d-flex justify-content-between align-items-center">
      <StatusBadge v-if="applied" status="APPLIED" />
      <button v-else class="btn btn-primary btn-sm ms-auto" @click="$emit('apply', drive)">
        Apply Now
      </button>
    </div>
  </div>
</template>
