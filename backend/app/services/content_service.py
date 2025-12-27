import random
from datetime import date
from sqlalchemy.orm import Session
from app.models.content import FrenchSentence, EnglishWord, MotivationalQuote
from app.models.user import User


def assign_daily_content(db: Session, user: User, day: date):
    seed = hash(f"{user.id}-{day.isoformat()}")
    random.seed(seed)

    french = db.query(FrenchSentence).all()
    english = db.query(EnglishWord).all()
    quotes = db.query(MotivationalQuote).all()

    return {
        "french": random.sample(french, min(5, len(french))),
        "english": random.sample(english, min(5, len(english))),
        "quote": random.choice(quotes) if quotes else None,
    }
