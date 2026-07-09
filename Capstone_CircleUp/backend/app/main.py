"""
CircleUp API entrypoint.

Run: uvicorn app.main:app --reload
Swagger: http://localhost:8000/docs
"""
import logging
import os

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routers import auth, users, activities

# ---------- Logging ----------
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(LOG_DIR, "app.log")),
    ],
)
logger = logging.getLogger("circleup")

app = FastAPI(
    title=settings.APP_NAME,
    description="CircleUp: discover and organize social activities.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all: log the real error server-side, never expose a traceback."""
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Something went wrong on our end. Please try again."},
    )


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(activities.router)


@app.get("/", tags=["Health"])
def root():
    return {"service": settings.APP_NAME, "status": "running"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}