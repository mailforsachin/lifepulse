from datetime import date
from sqlalchemy.orm import Session
from app.models.daily_entry import DailyEntry
from app.models.leaderboard import LeaderboardScore
from app.services.scoring_service import calculate_daily_score


def get_or_create_daily_entry(db: Session, user):
    today = date.today()

    entry = (
        db.query(DailyEntry)
        .filter(DailyEntry.user_id == user.id, DailyEntry.entry_date == today)
        .first()
    )

    if not entry:
        entry = DailyEntry(user_id=user.id, entry_date=today)
        db.add(entry)
        db.commit()
        db.refresh(entry)

    return entry


def update_score_and_leaderboard(db: Session, entry, user):
    score = calculate_daily_score(entry, user)
    entry.daily_score = score

    lb = (
        db.query(LeaderboardScore)
        .filter(
            LeaderboardScore.user_id == user.id,
            LeaderboardScore.score_date == entry.entry_date,
        )
        .first()
    )

    if not lb:
        lb = LeaderboardScore(
            user_id=user.id,
            score_date=entry.entry_date,
            score=score,
        )
        db.add(lb)
    else:
        lb.score = score

    db.commit()
