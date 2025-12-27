from pydantic import BaseModel


class DailyEntryOut(BaseModel):
    calories_consumed: int
    water_glasses: int
    exercise_minutes: int

    french_completed: bool
    english_completed: bool
    quote_viewed: bool

    daily_score: int

    class Config:
        from_attributes = True


class DailyEntryUpdate(BaseModel):
    calories_consumed: int | None = None
    water_glasses: int | None = None
    exercise_minutes: int | None = None

    french_completed: bool | None = None
    english_completed: bool | None = None
    quote_viewed: bool | None = None
