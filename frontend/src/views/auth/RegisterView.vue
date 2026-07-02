<script setup>
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"
import AuthLayout from "@/layouts/AuthLayout.vue"
import { useAuthStore } from "@/stores/auth.store"
import { useToast } from "@/composables/useToast"
import { isEmail, isRequired, minLength, runValidators } from "@/utils/validators"

const auth = useAuthStore()
const router = useRouter()
const toast = useToast()

const form = reactive({ name: "", email: "", password: "", role: "STUDENT", company_name: "" })
const errors = reactive({ name: "", email: "", password: "", company_name: "" })
const loading = ref(false)
const success = ref(false)

function validate() {
  errors.name = runValidators(form.name, [isRequired, minLength(2)]) || ""
  errors.email = runValidators(form.email, [isRequired, isEmail]) || ""
  errors.password = runValidators(form.password, [isRequired, minLength(6)]) || ""
  errors.company_name =
    form.role === "COMPANY" ? runValidators(form.company_name, [isRequired]) || "" : ""
  return !errors.name && !errors.email && !errors.password && !errors.company_name
}

async function handleSubmit() {
  if (!validate()) return
  loading.value = true
  try {
    await auth.register(form)
    success.value = true
    toast.success("Account created! You can now log in.")
    setTimeout(() => router.push("/login"), 1200)
  } catch (e) {
    toast.error(e.response?.data?.message || "Registration failed")
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <AuthLayout>
    <h3 class="fw-bold mb-1">Create your account</h3>
    <p class="pp-text-muted mb-4">Join as a student or a hiring company</p>

    <div class="btn-group w-100 mb-4" role="group">
      <input type="radio" class="btn-check" id="role-student" value="STUDENT" v-model="form.role" />
      <label class="btn btn-outline-primary" for="role-student"><i class="bi bi-mortarboard me-1"></i>Student</label>

      <input type="radio" class="btn-check" id="role-company" value="COMPANY" v-model="form.role" />
      <label class="btn btn-outline-primary" for="role-company"><i class="bi bi-building me-1"></i>Company</label>
    </div>

    <form @submit.prevent="handleSubmit" novalidate>
      <div class="mb-3">
        <label class="form-label small fw-semibold">Full Name</label>
        <input v-model.trim="form.name" type="text" class="form-control" :class="{ 'is-invalid': errors.name }" placeholder="Jane Doe" />
        <div class="invalid-feedback">{{ errors.name }}</div>
      </div>

      <div v-if="form.role === 'COMPANY'" class="mb-3">
        <label class="form-label small fw-semibold">Company Name</label>
        <input v-model.trim="form.company_name" type="text" class="form-control" :class="{ 'is-invalid': errors.company_name }" placeholder="Acme Corp" />
        <div class="invalid-feedback">{{ errors.company_name }}</div>
      </div>

      <div class="mb-3">
        <label class="form-label small fw-semibold">Email</label>
        <input v-model.trim="form.email" type="email" class="form-control" :class="{ 'is-invalid': errors.email }" placeholder="you@example.com" />
        <div class="invalid-feedback">{{ errors.email }}</div>
      </div>

      <div class="mb-3">
        <label class="form-label small fw-semibold">Password</label>
        <input v-model="form.password" type="password" class="form-control" :class="{ 'is-invalid': errors.password }" placeholder="At least 6 characters" />
        <div class="invalid-feedback">{{ errors.password }}</div>
      </div>

      <div v-if="form.role === 'COMPANY'" class="alert alert-info small py-2">
        <i class="bi bi-info-circle me-1"></i> Company accounts require admin approval before you can post drives.
      </div>

      <button type="submit" class="btn btn-primary w-100 py-2 mt-2" :disabled="loading || success">
        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
        Create Account
      </button>
    </form>

    <p class="text-center mt-4 small pp-text-muted">
      Already have an account?
      <router-link to="/login" class="fw-semibold">Sign in</router-link>
    </p>
  </AuthLayout>
</template>
