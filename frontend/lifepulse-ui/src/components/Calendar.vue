<script setup>
import { ref } from "vue"

/**
 * Emit selected date to Dashboard
 */
const emit = defineEmits(["update:date"])

const today = new Date()
const year = today.getFullYear()
const month = today.getMonth()
const todayDay = today.getDate()

const monthName = new Date(year, month).toLocaleString("default", {
  month: "long",
  year: "numeric",
})

const daysInMonth = new Date(year, month + 1, 0).getDate()
const days = Array.from({ length: daysInMonth }, (_, i) => i + 1)

const selectedDay = ref(todayDay)

/**
 * Emit selected date (YYYY-MM-DD)
 */
const selectDay = (day) => {
  selectedDay.value = day
  const date = new Date(year, month, day)
  emit("update:date", date.toLocaleDateString("en-CA"))
}

/**
 * Read score from stored daily data
 */
const scoreForDay = (day) => {
  const dateKey = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`
  const data = JSON.parse(localStorage.getItem(`lp_daily_${dateKey}`))
  if (!data) return 0

  let score = 0
  if (data.exercise) score += 30
  if (data.exerciseMinutes >= 30) score += 20
  if (data.calories > 0 || data.water > 0) score += 10

  return score
}
</script>

<template>
  <section class="bg-slate-900 rounded-2xl p-4 shadow space-y-4">
    <h2 class="text-lg font-semibold">{{ monthName }}</h2>

    <div class="grid grid-cols-7 gap-2">
      <button
        v-for="day in days"
        :key="day"
        @click="selectDay(day)"
        class="aspect-square rounded-xl flex flex-col items-center justify-center text-sm transition"
        :class="[
          scoreForDay(day) >= 60
            ? 'bg-green-600 text-white'
            : scoreForDay(day) > 0
            ? 'bg-indigo-600 text-white'
            : 'bg-slate-800',
          selectedDay === day ? 'ring-2 ring-yellow-400' : ''
        ]"
      >
        <span>{{ day }}</span>
        <span v-if="scoreForDay(day) > 0" class="text-yellow-300 text-xs">⭐</span>
      </button>
    </div>
  </section>
</template>
