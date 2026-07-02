<script setup>
import { Bar, Doughnut } from "vue-chartjs"
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
} from "chart.js"

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)

const props = defineProps({
  title: { type: String, required: true },
  type: { type: String, default: "bar" },
  labels: { type: Array, required: true },
  data: { type: Array, required: true },
  colors: {
    type: Array,
    default: () => ["#2563EB", "#06B6D4", "#16A34A", "#DC2626", "#F59E0B", "#0F172A"],
  },
})

const chartData = {
  labels: props.labels,
  datasets: [
    {
      label: props.title,
      data: props.data,
      backgroundColor: props.colors,
      borderRadius: 6,
    },
  ],
}

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: props.type !== "bar" } },
}
</script>

<template>
  <div class="pp-card p-3 p-lg-4 h-100">
    <h6 class="fw-semibold mb-3">{{ title }}</h6>
    <div style="height: 260px">
      <Bar v-if="type === 'bar'" :data="chartData" :options="options" />
      <Doughnut v-else :data="chartData" :options="options" />
    </div>
  </div>
</template>
