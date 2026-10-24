from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.config import STORAGE_DIR, DOCS_DIR, NOC_DIR
from backend.app.database import engine, Base, SessionLocal
from backend.app.services.seed_data import seed_database_if_empty
from backend.app.routers import (
    auth, institutions, fdrs, scrutiny, bank_gateway, maturity, release, audit, analytics
)

DIST_DIR = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database_if_empty(db)
    finally:
        db.close()

# Initialize immediately for serverless environments
init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="AICTE Security Deposit & FDR Management Portal",
    description="Enterprise Government-grade Zero-Trust FDR Lifecycle, AI OCR Scrutiny, Tri-Modal Banking & Merkle Audit API",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file mounts for document inspection
app.mount("/storage/documents", StaticFiles(directory=str(DOCS_DIR)), name="documents")
app.mount("/storage/nocs", StaticFiles(directory=str(NOC_DIR)), name="nocs")

# Register Routers
app.include_router(auth.router)
app.include_router(institutions.router)
app.include_router(fdrs.router)
app.include_router(scrutiny.router)
app.include_router(bank_gateway.router)
app.include_router(maturity.router)
app.include_router(release.router)
app.include_router(audit.router)
app.include_router(analytics.router)

# Mount frontend assets if built
if (DIST_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="frontend-assets")

@app.get("/api/health")
def health_check():
    return {
        "portal": "AICTE Security Deposit & FDR Management System",
        "authority": "All India Council for Technical Education (AICTE)",
        "ministry": "Ministry of Education, Government of India",
        "status": "OPERATIONAL",
        "version": "2.0.0-PROD",
        "zero_trust_status": "ENFORCED",
        "documentation": "/docs"
    }

@app.get("/{full_path:path}")
def serve_frontend_spa(full_path: str):
    # If file exists in dist, serve it
    target_file = DIST_DIR / full_path
    if full_path and target_file.is_file():
        return FileResponse(str(target_file))
    # Otherwise fallback to index.html for SPA routing
    if (DIST_DIR / "index.html").exists():
        return FileResponse(str(DIST_DIR / "index.html"))
    return health_check()
