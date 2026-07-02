<script setup>
import { reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import AuthLayout from "@/layouts/AuthLayout.vue"
import { useAuthStore } from "@/stores/auth.store"
import { useToast } from "@/composables/useToast"
import { isEmail, isRequired, runValidators } from "@/utils/validators"

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const toast = useToast()

const form = reactive({ email: "", password: "" })
const errors = reactive({ email: "", password: "" })
const loading = ref(false)
const showPassword = ref(false)

function validate() {
  errors.email = runValidators(form.email, [isRequired, isEmail]) || ""
  errors.password = runValidators(form.password, [isRequired]) || ""
  return !errors.email && !errors.password
}

async function handleSubmit() {
  if (!validate()) return
  loading.value = true
  try {
    const user = await auth.login(form)
    toast.success(`Welcome back, ${user.name.split(" ")[0]}!`)
    router.push(route.query.redirect || auth.homeRouteForRole())
  } catch (e) {
    toast.error(e.response?.data?.message || "Login failed")
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <AuthLayout>
    <h3 class="fw-bold mb-1">Welcome back</h3>
    <p class="pp-text-muted mb-4">Sign in to continue to your dashboard</p>

    <form @submit.prevent="handleSubmit" novalidate>
      <div class="mb-3">
        <label class="form-label small fw-semibold">Email</label>
        <input
          v-model.trim="form.email"
          type="email"
          class="form-control"
          :class="{ 'is-invalid': errors.email }"
          placeholder="you@example.com"
          autocomplete="username"
        />
        <div class="invalid-feedback">{{ errors.email }}</div>
      </div>

      <div class="mb-3">
        <label class="form-label small fw-semibold">Password</label>
        <div class="input-group">
          <input
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            class="form-control"
            :class="{ 'is-invalid': errors.password }"
            placeholder="••••••••"
            autocomplete="current-password"
          />
          <button class="btn btn-outline-secondary" type="button" @click="showPassword = !showPassword">
            <i :class="['bi', showPassword ? 'bi-eye-slash' : 'bi-eye']"></i>
          </button>
          <div class="invalid-feedback">{{ errors.password }}</div>
        </div>
      </div>

      <button type="submit" class="btn btn-primary w-100 py-2 mt-2" :disabled="loading">
        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
        Sign In
      </button>
    </form>

    <p class="text-center mt-4 small pp-text-muted">
      Don't have an account?
      <router-link to="/register" class="fw-semibold">Register here</router-link>
    </p>

    <div class="pp-demo-hint mt-4 p-3 small">
      <strong>Demo Admin:</strong> admin@placement.com / admin123
    </div>
  </AuthLayout>
</template>

<style scoped>
.pp-demo-hint {
  background: #eff6ff;
  border-radius: var(--pp-radius-sm);
  color: #1e40af;
}
</style>
