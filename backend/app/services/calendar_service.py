from calendar import monthrange
from datetime import date
from sqlalchemy.orm import Session

from app.models.daily_entry import DailyEntry


def get_month_calendar(db: Session, user_id: int, year: int, month: int):
    days_in_month = monthrange(year, month)[1]

    entries = (
        db.query(DailyEntry)
        .filter(
            DailyEntry.user_id == user_id,
            DailyEntry.entry_date.between(
                date(year, month, 1),
                date(year, month, days_in_month),
            ),
        )
        .all()
    )

    entry_map = {e.entry_date.day: e for e in entries}

    calendar = []

    for day in range(1, days_in_month + 1):
        entry = entry_map.get(day)

        if not entry:
            status = "missed"
            score = 0
        elif entry.daily_score >= 70:
            status = "completed"
            score = entry.daily_score
        elif entry.daily_score > 0:
            status = "partial"
            score = entry.daily_score
        else:
            status = "missed"
            score = 0

        calendar.append({
            "day": day,
            "status": status,
            "score": score,
        })

    return calendar
