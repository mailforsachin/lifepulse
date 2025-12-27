from fastapi import APIRouter
from app.services.sentence_loader import load_sentences

router = APIRouter(prefix="/sentences", tags=["Sentences"])

@router.get("")
def get_sentences(language: str = "french"):
    return load_sentences(language)
