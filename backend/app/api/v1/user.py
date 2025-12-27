from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.utils.streaks import calculate_streaks

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/streaks")
def get_streaks(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return calculate_streaks(db, current_user.id)
