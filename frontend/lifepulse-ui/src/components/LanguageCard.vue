<script setup>
import { ref, onMounted, watch } from "vue"
import api from "../services/api"

const props = defineProps({
  title: String,
  direction: String, // fr_en | en_fr
  date: String,
})

const sentence = ref(null)
const completed = ref(false)
const loading = ref(false)

/**
 * TEMP sentence pools (unchanged)
 */
const POOLS = {
  fr_en: [
    {
      primary: "Je vais au marché demain.",
      secondary: "I am going to the market tomorrow.",
    },
  ],
  en_fr: [
    {
      primary: "Consistency beats motivation.",
      secondary: "La régularité bat la motivation.",
    },
  ],
}

/**
 * Load sentence + backend completion state
 */
const load = async () => {
  sentence.value = POOLS[props.direction]?.[0] || null
  completed.value = false

  try {
    const res = await api.get("/daily/today", {
      params: {},
    })

    completed.value =
      props.direction === "fr_en"
        ? res.data.french_completed
        : res.data.english_completed
  } catch {
    // silent — calendar navigation should not error
  }
}

/**
 * Mark complete (ONE-WAY ACTION)
 */
const toggleCompleted = async () => {
  if (completed.value || loading.value) return

  loading.value = true
  try {
    const res = await api.post("/language/complete", null, {
      params: {
        lang: props.direction === "fr_en" ? "fr" : "en",
        entry_date: props.date,
      },
    })

    completed.value =
      props.direction === "fr_en"
        ? res.data.french_completed
        : res.data.english_completed
  } catch (e) {
    console.error("Language complete failed", e)
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => props.date, load)
</script>

<template>
  <section class="bg-slate-900 rounded-2xl p-4 shadow space-y-3">
    <div class="flex justify-between items-center">
      <h3 class="text-sm font-semibold">{{ title }}</h3>

      <button
        @click="toggleCompleted"
        :disabled="completed || loading"
        class="text-xs px-3 py-1 rounded-full transition"
        :class="completed
          ? 'bg-green-600 text-white'
          : 'bg-slate-700 text-slate-300 hover:bg-slate-600'"
      >
        {{ completed ? "Done" : "Mark done" }}
      </button>
    </div>

    <div v-if="sentence" class="text-sm space-y-1">
      <div class="font-medium">{{ sentence.primary }}</div>
      <div class="text-slate-400">{{ sentence.secondary }}</div>
    </div>
  </section>
</template>
