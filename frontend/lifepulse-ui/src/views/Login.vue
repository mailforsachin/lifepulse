<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "../stores/auth"

const email = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)

const auth = useAuthStore()
const router = useRouter()

const submit = async () => {
  error.value = ""
  loading.value = true

  try {
    await auth.login(email.value, password.value)
    router.push("/")
  } catch (e) {
    error.value = "Invalid email or password"
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 text-white">
    <div class="w-full max-w-sm p-6 bg-gray-800 rounded-xl shadow">
      <h1 class="text-2xl font-bold mb-4 text-center">LifePulse</h1>

      <input
        id="email"
        name="email"
        v-model="email"
        placeholder="Email"
        class="w-full mb-3 p-2 rounded bg-gray-700 outline-none"
      />

      <input
        id="password"
        name="password"
        v-model="password"
        type="password"
        placeholder="Password"
        class="w-full mb-4 p-2 rounded bg-gray-700 outline-none"
      />

      <button
        @click="submit"
        :disabled="loading"
        class="w-full bg-indigo-600 py-2 rounded font-semibold hover:bg-indigo-500 disabled:opacity-50"
      >
        {{ loading ? "Signing in..." : "Login" }}
      </button>

      <p v-if="error" class="text-red-400 mt-3 text-center">
        {{ error }}
      </p>
    </div>
  </div>
</template>
