from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.app.database import get_db
from backend.app.models import FDRInstrument, BankVerificationToken, FDRDocument
from backend.app.services.bank_gateway_service import (
    verify_via_cbs_api, generate_bank_officer_token, submit_bank_officer_verification, verify_via_nesl_digilocker
)

router = APIRouter(prefix="/api/bank-gateway", tags=["Tri-Modal Bank Verification Gateway"])

class GenerateTokenRequest(BaseModel):
    fdr_id: str
    branch_email: str

class BankDeskSubmitRequest(BaseModel):
    manager_name: str
    manager_emp_id: str
    is_approved: bool
    notes: Optional[str] = "Statutory lien confirmed in bank CBS ledger."

@router.post("/cbs-verify/{fdr_id}")
def run_cbs_api_verification(fdr_id: str, db: Session = Depends(get_db)):
    """
    Mode 1: Core Banking System (CBS) / SFMS real-time verification query.
    """
    fdr = db.query(FDRInstrument).filter(FDRInstrument.id == fdr_id).first()
    if not fdr:
        raise HTTPException(status_code=404, detail="FDR instrument not found")

    result = verify_via_cbs_api(db, fdr)
    return result

@router.post("/generate-token")
def create_branch_token(body: GenerateTokenRequest, db: Session = Depends(get_db)):
    """
    Mode 2: Generates a secure branch manager digital verification token.
    """
    fdr = db.query(FDRInstrument).filter(FDRInstrument.id == body.fdr_id).first()
    if not fdr:
        raise HTTPException(status_code=404, detail="FDR instrument not found")

    token_obj = generate_bank_officer_token(db, fdr, body.branch_email)
    return {
        "success": True,
        "token": token_obj.token,
        "branch_email": token_obj.branch_email,
        "verification_desk_url": f"/bank-verification/{token_obj.token}",
        "status": token_obj.status
    }

@router.get("/desk/{token}")
def get_verification_desk_data(token: str, db: Session = Depends(get_db)):
    """
    Mode 2: Loads the Bank Officer Verification Desk for a specific token.
    """
    token_obj = db.query(BankVerificationToken).filter(BankVerificationToken.token == token).first()
    if not token_obj:
        raise HTTPException(status_code=404, detail="Verification token not found or expired")

    fdr = db.query(FDRInstrument).filter(FDRInstrument.id == token_obj.fdr_id).first()
    if not fdr:
        raise HTTPException(status_code=404, detail="FDR not found")

    inst = fdr.institution
    doc = db.query(FDRDocument).filter(FDRDocument.fdr_id == fdr.id).first()

    return {
        "token": token_obj.token,
        "status": token_obj.status,
        "branch_email": token_obj.branch_email,
        "bank_name": token_obj.bank_name,
        "fdr": {
            "id": fdr.id,
            "fdr_number": fdr.fdr_number,
            "account_number": fdr.account_number,
            "bank_name": fdr.bank_name,
            "branch_name": fdr.branch_name,
            "ifsc_code": fdr.ifsc_code,
            "deposit_amount": fdr.deposit_amount,
            "issue_date": fdr.issue_date,
            "maturity_date": fdr.maturity_date,
            "lien_marked": fdr.lien_marked,
            "institution_name": inst.name if inst else "Unknown",
            "institution_pid": inst.pid if inst else "N/A",
            "document_url": f"/storage/documents/{doc.file_name}" if doc else None
        }
    }

@router.post("/desk/{token}/submit")
def submit_verification_desk_decision(
    token: str,
    body: BankDeskSubmitRequest,
    db: Session = Depends(get_db)
):
    """
    Mode 2: Branch Manager submits digital verification certificate.
    """
    result = submit_bank_officer_verification(
        db=db,
        token_str=token,
        manager_name=body.manager_name,
        manager_emp_id=body.manager_emp_id,
        is_approved=body.is_approved,
        manager_notes=body.notes
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Verification submission failed"))

    return result

@router.post("/nesl-verify/{fdr_id}")
def run_nesl_digilocker_verification(fdr_id: str, db: Session = Depends(get_db)):
    """
    Mode 3: NeSL / DigiLocker Information Utility verification.
    """
    fdr = db.query(FDRInstrument).filter(FDRInstrument.id == fdr_id).first()
    if not fdr:
        raise HTTPException(status_code=404, detail="FDR instrument not found")

    result = verify_via_nesl_digilocker(db, fdr)
    return result
