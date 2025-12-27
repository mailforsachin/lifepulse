<script setup>
import { ref, watch, computed } from "vue"

const props = defineProps({
  date: {
    type: String,
    required: true,
  },
  userId: {
    type: String,
    required: true,
  },
})

const todayKey = new Date().toLocaleDateString("en-CA")
const isToday = computed(() => props.date === todayKey)

const storageKey = computed(
  () => `lp_${props.userId}_daily_${props.date}`
)

const data = ref({
  exercise: false,
  exerciseMinutes: 0,
  calories: 0,
  water: 0,
})

const load = () => {
  const stored = JSON.parse(localStorage.getItem(storageKey.value))
  if (stored) data.value = stored
}

watch(
  data,
  () => {
    if (isToday.value) {
      localStorage.setItem(storageKey.value, JSON.stringify(data.value))
    }
  },
  { deep: true }
)

watch(() => props.date, load)

load()
</script>

<template>
  <section class="bg-slate-900 rounded-2xl p-4 shadow space-y-3">
    <h3 class="text-sm font-semibold">Daily Inputs</h3>

    <label class="flex items-center gap-2 text-sm">
      <input
        id="exercise"
        type="checkbox"
        v-model="data.exercise"
        :disabled="!isToday"
      />
      Exercised today
    </label>

    <div class="flex items-center gap-2 text-sm">
      <input
        id="exerciseMinutes"
        type="number"
        class="w-20 px-2 py-1 rounded bg-slate-800"
        v-model.number="data.exerciseMinutes"
        :disabled="!isToday || !data.exercise"
        min="0"
      />
      minutes
    </div>

    <div class="flex items-center gap-2 text-sm">
      <span>🔥 Calories</span>
      <input
        id="calories"
        type="number"
        class="w-24 px-2 py-1 rounded bg-slate-800"
        v-model.number="data.calories"
        :disabled="!isToday"
        min="0"
      />
    </div>

    <div class="flex items-center gap-2 text-sm">
      <span>💧 Water (glasses)</span>
      <input
        id="water"
        type="number"
        class="w-20 px-2 py-1 rounded bg-slate-800"
        v-model.number="data.water"
        :disabled="!isToday"
        min="0"
      />
    </div>

    <div v-if="!isToday" class="text-xs text-slate-500 pt-1">
      Past & future days are read-only
    </div>
  </section>
</template>
