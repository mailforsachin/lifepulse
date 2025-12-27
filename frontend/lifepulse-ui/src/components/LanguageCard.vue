<script setup>
import { ref, onMounted, watch, computed } from "vue"
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
 * Date helpers
 */
const today = new Date().toLocaleDateString("en-CA")
const isFuture = computed(() => props.date > today)

/**
 * Deterministic date → index mapping (NO REPEATS)
 */
const dateToIndex = (date, length) => {
  const epoch = new Date(date).getTime()
  const dayNumber = Math.floor(epoch / (1000 * 60 * 60 * 24))
  return dayNumber % length
}

/**
 * Load sentence + completion
 */
const load = async () => {
  sentence.value = null
  completed.value = false

  try {
    loading.value = true

    // 1️⃣ Load full sentence pool (once per load)
    const poolRes = await api.get("/sentences", {
      params: { language: "french" },
    })

    const pool = poolRes.data
    if (!pool || pool.length === 0) return

    // 2️⃣ Pick unique sentence per date
    const idx = dateToIndex(props.date, pool.length)
    const picked = pool[idx]

    // 3️⃣ STRICT language separation
    sentence.value =
      props.direction === "fr_en"
        ? { primary: picked.fr, secondary: picked.en }
        : { primary: picked.en, secondary: picked.fr }

    // 4️⃣ Completion state
    const statusRes = await api.get("/daily/by-date", {
      params: { entry_date: props.date },
    })

    completed.value =
      props.direction === "fr_en"
        ? !!statusRes.data.french_completed
        : !!statusRes.data.english_completed
  } catch (e) {
    console.error("LanguageCard load failed", e)
  } finally {
    loading.value = false
  }
}

const toggleCompleted = async () => {
  if (isFuture.value) return

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
        :disabled="isFuture || loading"
        class="text-xs px-3 py-1 rounded-full transition"
        :class="
          isFuture
            ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
            : completed
              ? 'bg-green-600 text-white'
              : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
        "
      >
        {{ completed ? "Done" : "Mark done" }}
      </button>
    </div>

    <div v-if="sentence" class="text-sm space-y-1">
      <div class="font-medium">{{ sentence.primary }}</div>
      <div class="text-slate-400">{{ sentence.secondary }}</div>
    </div>

    <div v-if="isFuture" class="text-xs text-slate-500">
      Future entries are read-only
    </div>
  </section>
</template>
