def calculate_daily_score(entry, user) -> int:
    score = 0

    # Health (70)
    if entry.calories_consumed <= user.calorie_goal:
        score += 30
    if entry.water_glasses >= user.water_goal:
        score += 20
    if entry.exercise_minutes >= user.exercise_goal:
        score += 20

    # Learning (30)
    if entry.french_completed:
        score += 10
    if entry.english_completed:
        score += 10
    if entry.quote_viewed:
        score += 10

    # Perfect bonus
    if score >= 100:
        score = 100

    return score
