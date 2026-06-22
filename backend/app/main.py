from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.projects import router as projects_router
from app.api.media import router as media_router
from app.core.config import settings
from app.core.database import init_db

app = FastAPI(title="AI Manga Translator Pro", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health():
    return {"ok": True, "env": settings.app_env}


app.include_router(projects_router)
app.include_router(media_router)
