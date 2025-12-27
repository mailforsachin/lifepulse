from datetime import date
from sqlalchemy import Date, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class DailyEntry(Base):
    __tablename__ = "daily_entries"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )

    entry_date: Mapped[date] = mapped_column(
        Date,
        index=True,
        nullable=False,
    )

    calories_consumed: Mapped[int] = mapped_column(Integer, default=0)
    water_glasses: Mapped[int] = mapped_column(Integer, default=0)
    exercise_minutes: Mapped[int] = mapped_column(Integer, default=0)

    french_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    english_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    quote_viewed: Mapped[bool] = mapped_column(Boolean, default=False)

    daily_score: Mapped[int] = mapped_column(Integer, default=0)
