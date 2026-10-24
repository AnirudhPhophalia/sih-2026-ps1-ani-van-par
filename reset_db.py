import os
from pathlib import Path
from backend.app.database import engine, Base, SessionLocal
from backend.app.services.seed_data import seed_database_if_empty
from backend.app.models import Institution, FDRInstrument, FDRDocument, FDRVerification, FDRReleaseRequest, FDRAlert, AuditLedger, BankVerificationToken

def reset_database():
    db_file = Path(__file__).resolve().parent / "backend" / "aicte_fdr.db"
    db = SessionLocal()
    try:
        # Drop and re-create tables cleanly
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        seed_database_if_empty(db)
        print("Database cleanly reset and re-seeded with pristine Merkle ledger!")
    finally:
        db.close()

if __name__ == "__main__":
    reset_database()
