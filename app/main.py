"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import convert, health

# Ensure directories exist
settings.ensure_directories()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="AI-powered PDF to Word converter with layout preservation",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(convert.router, prefix="/api", tags=["Convert"])


@app.on_event("startup")
async def startup_event():
    """Execute startup tasks."""
    print(f"[STARTUP] {settings.app_name} v{settings.version} starting...")
    print(f"[CONFIG] Output directory: {settings.output_dir.absolute()}")
    print(f"[CONFIG] Max file size: {settings.max_file_size_mb}MB")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute shutdown tasks."""
    print(f"[SHUTDOWN] {settings.app_name} shutting down...")
