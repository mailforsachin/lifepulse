export function calculateScore(data = {}) {
  let score = 0

  // Exercise
  if (data.exercise) score += 30
  if (data.exerciseMinutes >= 30) score += 20

  // Consistency (any input)
  if (data.calories > 0 || data.water > 0) score += 10

  // Language learning
  if (data.lang_fr) score += 10
  if (data.lang_en) score += 10

  return Math.min(score, 100)
}
