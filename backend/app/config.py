import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
DOCS_DIR = STORAGE_DIR / "documents"
NOC_DIR = STORAGE_DIR / "nocs"

# Ensure directories exist
STORAGE_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)
NOC_DIR.mkdir(exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/aicte_fdr.db")
SECRET_KEY = os.getenv("SECRET_KEY", "aicte-fdr-cryptographic-master-key-2026-sih")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

DISCREPANCY_THRESHOLD = 0.05
