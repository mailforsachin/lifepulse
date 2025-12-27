from sqlalchemy import Text, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class FrenchSentence(Base):
    __tablename__ = "french_sentences"

    id: Mapped[int] = mapped_column(primary_key=True)
    french_text: Mapped[str] = mapped_column(Text)
    english_translation: Mapped[str] = mapped_column(Text)
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1)


class EnglishWord(Base):
    __tablename__ = "english_words"

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(String(100))
    definition: Mapped[str] = mapped_column(Text)
    example_sentence: Mapped[str] = mapped_column(Text)


class MotivationalQuote(Base):
    __tablename__ = "motivational_quotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    quote_text: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(String(100))
