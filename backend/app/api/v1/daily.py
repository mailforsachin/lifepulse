from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.daily import DailyEntryOut, DailyEntryUpdate
from app.services.daily_service import (
    get_or_create_daily_entry,
    update_score_and_leaderboard,
)
from app.services.calendar_service import get_month_calendar


router = APIRouter(prefix="/daily", tags=["Daily"])


@router.get("/today", response_model=DailyEntryOut)
def get_today(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = get_or_create_daily_entry(db, current_user)
    return entry


@router.post("/today", response_model=DailyEntryOut)
def update_today(
    payload: DailyEntryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = get_or_create_daily_entry(db, current_user)

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(entry, field, value)

    update_score_and_leaderboard(db, entry, current_user)

    db.refresh(entry)
    return entry

@router.get("/calendar/{year}/{month}")
def get_calendar(
    year: int,
    month: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_month_calendar(
        db=db,
        user_id=current_user.id,
        year=year,
        month=month,
    )
