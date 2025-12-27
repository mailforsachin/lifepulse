from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    display_name: Mapped[str | None] = mapped_column(String(100))
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")

    calorie_goal: Mapped[int] = mapped_column(Integer, default=2000)
    water_goal: Mapped[int] = mapped_column(Integer, default=8)
    exercise_goal: Mapped[int] = mapped_column(Integer, default=30)

    privacy_public: Mapped[bool] = mapped_column(Boolean, default=True)
    leaderboard_opt_out: Mapped[bool] = mapped_column(Boolean, default=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
