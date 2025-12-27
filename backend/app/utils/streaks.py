from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.models.daily_entry import DailyEntry


def calculate_streaks(db: Session, user_id: int):
    entries = (
        db.query(DailyEntry)
        .filter(DailyEntry.user_id == user_id)
        .order_by(DailyEntry.entry_date.desc())
        .all()
    )

    dates = {
        e.entry_date
        for e in entries
        if e.daily_score >= 70
    }

    today = date.today()

    # Current streak
    current = 0
    d = today
    while d in dates:
        current += 1
        d -= timedelta(days=1)

    # Longest streak
    longest = 0
    streak = 0
    prev = None

    for d in sorted(dates):
        if prev and d == prev + timedelta(days=1):
            streak += 1
        else:
            streak = 1
        longest = max(longest, streak)
        prev = d

    return {
        "current_streak": current,
        "longest_streak": longest,
    }
