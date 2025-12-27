from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.daily import router as daily_router
from app.api.v1.user import router as user_router
from app.api.v1.language import router as language_router

app = FastAPI(
    title="LifePulse API",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
)

# ✅ CORS MUST COME BEFORE ROUTERS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://51.222.13.241:5173",
        "https://lifepulse.omchat.ovh",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

# ✅ Routers AFTER middleware
app.include_router(auth_router, prefix="/api/v1")
app.include_router(daily_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(language_router, prefix="/api/v1")
