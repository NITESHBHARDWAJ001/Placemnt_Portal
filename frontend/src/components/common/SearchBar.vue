<script setup>
defineProps({
  modelValue: { type: String, default: "" },
  placeholder: { type: String, default: "Search..." },
})
defineEmits(["update:modelValue"])
</script>

<template>
  <div class="input-group">
    <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
    <input
      type="text"
      class="form-control border-start-0"
      :placeholder="placeholder"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>
