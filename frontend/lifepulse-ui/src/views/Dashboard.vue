<script setup>
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "../stores/auth"

import Calendar from "../components/Calendar.vue"
import LanguageCard from "../components/LanguageCard.vue"
import DayInput from "../components/DayInput.vue"
import { calculateScore } from "../utils/score"

const auth = useAuthStore()
const router = useRouter()

const selectedDate = ref(
  new Date().toLocaleDateString("en-CA")
)

/**
 * ✅ USER ID — SINGLE SOURCE OF TRUTH
 * (comes from JWT, stored in auth store)
 */
const userId = computed(() => {
  return auth.userId ? String(auth.userId) : null
})

/**
 * ✅ DAILY KEY (unchanged behavior)
 */
const dailyKey = computed(() => {
  if (!userId.value) return null
  return `lp_${userId.value}_daily_${selectedDate.value}`
})

const dailyData = computed(() => {
  if (!dailyKey.value) return {}
  return JSON.parse(localStorage.getItem(dailyKey.value)) || {}
})

const score = computed(() => calculateScore(dailyData.value))

const logout = () => {
  auth.logout()
  router.push("/login")
}
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">

    <!-- Header -->
    <header class="sticky top-0 z-20 bg-slate-900/80 backdrop-blur px-4 py-3 flex justify-between items-center">
      <h1 class="text-xl font-semibold">LifePulse</h1>
      <button class="text-sm text-red-400" @click="logout">
        Logout
      </button>
    </header>

    <!-- Disclaimer -->
    <p class="text-[11px] text-slate-400 text-center mt-2 px-4">
      ⚠️ LifePulse is under active development. Features, scoring, and data models may evolve.
    </p>

    <main class="max-w-md mx-auto px-4 py-6 space-y-6">

      <!-- Today Metrics -->
      <section class="bg-slate-900 rounded-2xl p-4 shadow">
        <h2 class="text-lg font-semibold mb-4">Today</h2>

        <div class="grid grid-cols-2 gap-3">
          <div class="bg-slate-800 rounded-xl p-3 text-center">
            <div class="text-slate-400 text-xs">🔥 Calories</div>
            <div class="text-lg font-semibold">{{ dailyData.calories || 0 }}</div>
          </div>

          <div class="bg-slate-800 rounded-xl p-3 text-center">
            <div class="text-slate-400 text-xs">🏃 Exercise</div>
            <div class="text-lg font-semibold">
              {{ dailyData.exerciseMinutes || 0 }} min
            </div>
          </div>

          <div class="bg-slate-800 rounded-xl p-3 text-center">
            <div class="text-slate-400 text-xs">💧 Water</div>
            <div class="text-lg font-semibold">{{ dailyData.water || 0 }}</div>
          </div>

          <div class="bg-slate-800 rounded-xl p-3 text-center text-yellow-400">
            <div class="text-xs">⭐ Score</div>
            <div class="text-lg font-semibold">{{ score }}</div>
          </div>
        </div>
      </section>

      <!-- Daily Inputs -->
      <DayInput
        v-if="userId"
        :date="selectedDate"
        :user-id="userId"
      />

      <!-- Language Learning -->
      <section class="space-y-4">
        <LanguageCard
          title="French Practice"
          direction="fr_en"
          :date="selectedDate"
        />
        <LanguageCard
          title="English Practice"
          direction="en_fr"
          :date="selectedDate"
        />
      </section>

      <!-- Calendar -->
      <Calendar @update:date="selectedDate = $event" />

    </main>
  </div>
</template>
