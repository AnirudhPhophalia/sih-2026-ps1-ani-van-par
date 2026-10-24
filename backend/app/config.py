import os
import shutil
from pathlib import Path

IS_VERCEL = bool(os.getenv("VERCEL"))

if IS_VERCEL:
    BASE_DIR = Path("/tmp")
    STORAGE_DIR = BASE_DIR / "storage"
    DOCS_DIR = STORAGE_DIR / "documents"
    NOC_DIR = STORAGE_DIR / "nocs"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////tmp/aicte_fdr.db")
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    STORAGE_DIR = BASE_DIR / "storage"
    DOCS_DIR = STORAGE_DIR / "documents"
    NOC_DIR = STORAGE_DIR / "nocs"
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/aicte_fdr.db")

# Ensure writable directories exist
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)
NOC_DIR.mkdir(parents=True, exist_ok=True)

# If on Vercel, copy pre-bundled sample certificate images to /tmp/storage/documents
REPO_DOCS = Path(__file__).resolve().parent.parent / "storage" / "documents"
if IS_VERCEL and REPO_DOCS.exists():
    for f in REPO_DOCS.glob("*.png"):
        dest = DOCS_DIR / f.name
        if not dest.exists():
            try:
                shutil.copy2(f, dest)
            except Exception:
                pass

SECRET_KEY = os.getenv("SECRET_KEY", "aicte-fdr-cryptographic-master-key-2026-sih")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

DISCREPANCY_THRESHOLD = 0.05
