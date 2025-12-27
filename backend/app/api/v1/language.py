from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.daily_entry import DailyEntry
from app.models.user import User
from app.services.scoring_service import calculate_daily_score

router = APIRouter(prefix="/language", tags=["Language"])


@router.post("/complete")
def mark_language_complete(
    lang: str,           # "fr" or "en"
    entry_date: date,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    entry = (
        db.query(DailyEntry)
        .filter(
            DailyEntry.user_id == user.id,
            DailyEntry.entry_date == entry_date,
        )
        .first()
    )

    if not entry:
        entry = DailyEntry(
            user_id=user.id,
            entry_date=entry_date,
            calories_consumed=0,
            water_glasses=0,
            exercise_minutes=0,
            quote_viewed=False,
            french_completed=False,
            english_completed=False,
        )
        db.add(entry)
        db.flush()  # ✅ ensures entry.id exists

    if lang == "fr":
        entry.french_completed = True
    elif lang == "en":
        entry.english_completed = True

    # ✅ SAFE scoring (no crash for past days)
    try:
        entry.daily_score = calculate_daily_score(entry, user)
    except Exception:
        entry.daily_score = entry.daily_score or 0

    db.commit()
    db.refresh(entry)

    return {
        "date": entry.entry_date,
        "french_completed": entry.french_completed,
        "english_completed": entry.english_completed,
        "daily_score": entry.daily_score,
    }
