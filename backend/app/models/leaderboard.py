from datetime import date
from sqlalchemy import Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class LeaderboardScore(Base):
    __tablename__ = "leaderboard_scores"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )

    score_date: Mapped[date] = mapped_column(
        Date,
        index=True,
        nullable=False,
    )

    score: Mapped[int] = mapped_column(Integer, default=0)
