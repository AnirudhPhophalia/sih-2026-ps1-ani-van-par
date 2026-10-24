import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.app.database import get_db
from backend.app.config import DOCS_DIR
from backend.app.models import FDRInstrument, Institution, FDRDocument, FDRVerification, AuditLedger
from backend.app.services.ocr_service import compute_file_sha256, extract_fdr_metadata, calculate_discrepancy
from backend.app.services.audit_service import log_audit_event
from backend.app.services.document_generator import generate_fdr_sample_image

router = APIRouter(prefix="/api/fdrs", tags=["FDR Instruments Repository"])

class FDRCreateRequest(BaseModel):
    institution_id: str
    fdr_number: str
    account_number: str
    instrument_type: Optional[str] = "FDR_JOINT"
    bank_name: str
    branch_name: str
    ifsc_code: str
    deposit_amount: float
    rate_of_interest: Optional[float] = 7.25
    issue_date: str # YYYY-MM-DD
    maturity_date: str # YYYY-MM-DD
    statutory_lock_in_years: Optional[int] = 8
    statutory_lock_in_end_date: str
    lien_marked: Optional[bool] = True
    lien_reference_number: Optional[str] = None
    predecessor_fdr_id: Optional[str] = None

@router.get("")
def list_fdrs(
    status: Optional[str] = Query(None),
    bank: Optional[str] = Query(None),
    institution_id: Optional[str] = Query(None),
    is_discrepant: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(FDRInstrument)
    if status:
        query = query.filter(FDRInstrument.status == status)
    if bank:
        query = query.filter(FDRInstrument.bank_name.ilike(f"%{bank}%"))
    if institution_id:
        query = query.filter(FDRInstrument.institution_id == institution_id)
    if is_discrepant is not None:
        query = query.filter(FDRInstrument.is_discrepant == is_discrepant)
    if search:
        s = f"%{search}%"
        query = query.join(Institution).filter(
            (FDRInstrument.fdr_number.ilike(s)) |
            (FDRInstrument.account_number.ilike(s)) |
            (Institution.name.ilike(s)) |
            (Institution.pid.ilike(s))
        )

    fdrs = query.order_by(FDRInstrument.created_at.desc()).all()
    results = []
    for f in fdrs:
        inst = f.institution
        results.append({
            "id": f.id,
            "fdr_number": f.fdr_number,
            "account_number": f.account_number,
            "bank_name": f.bank_name,
            "branch_name": f.branch_name,
            "ifsc_code": f.ifsc_code,
            "deposit_amount": f.deposit_amount,
            "rate_of_interest": f.rate_of_interest,
            "issue_date": f.issue_date,
            "maturity_date": f.maturity_date,
            "statutory_lock_in_years": f.statutory_lock_in_years,
            "statutory_lock_in_end_date": f.statutory_lock_in_end_date,
            "lien_marked": f.lien_marked,
            "status": f.status,
            "verification_level": f.verification_level,
            "is_discrepant": f.is_discrepant,
            "discrepancy_notes": f.discrepancy_notes,
            "institution_id": f.institution_id,
            "institution_name": inst.name if inst else "Unknown",
            "institution_pid": inst.pid if inst else "N/A",
            "institution_state": inst.state if inst else "N/A",
            "regional_office": inst.regional_office if inst else "N/A",
            "created_at": f.created_at
        })

    return {"fdrs": results, "total": len(results)}

@router.get("/{fdr_id}")
def get_fdr_detail(fdr_id: str, db: Session = Depends(get_db)):
    fdr = db.query(FDRInstrument).filter(FDRInstrument.id == fdr_id).first()
    if not fdr:
        raise HTTPException(status_code=404, detail="FDR instrument not found")

    inst = fdr.institution
    docs = db.query(FDRDocument).filter(FDRDocument.fdr_id == fdr.id).all()
    verifications = db.query(FDRVerification).filter(FDRVerification.fdr_id == fdr.id).order_by(FDRVerification.verified_at.desc()).all()

    # Predecessor lineage
    predecessor = None
    if fdr.predecessor_fdr_id:
        p = db.query(FDRInstrument).filter(FDRInstrument.id == fdr.predecessor_fdr_id).first()
        if p:
            predecessor = {
                "id": p.id,
                "fdr_number": p.fdr_number,
                "deposit_amount": p.deposit_amount,
                "maturity_date": p.maturity_date,
                "status": p.status
            }

    return {
        "fdr": {
            "id": fdr.id,
            "fdr_number": fdr.fdr_number,
            "account_number": fdr.account_number,
            "instrument_type": fdr.instrument_type,
            "bank_name": fdr.bank_name,
            "branch_name": fdr.branch_name,
            "ifsc_code": fdr.ifsc_code,
            "deposit_amount": fdr.deposit_amount,
            "rate_of_interest": fdr.rate_of_interest,
            "issue_date": fdr.issue_date,
            "maturity_date": fdr.maturity_date,
            "statutory_lock_in_years": fdr.statutory_lock_in_years,
            "statutory_lock_in_end_date": fdr.statutory_lock_in_end_date,
            "lien_marked": fdr.lien_marked,
            "lien_in_favor_of": fdr.lien_in_favor_of,
            "lien_reference_number": fdr.lien_reference_number,
            "status": fdr.status,
            "verification_level": fdr.verification_level,
            "is_discrepant": fdr.is_discrepant,
            "discrepancy_notes": fdr.discrepancy_notes,
            "predecessor": predecessor,
            "institution": {
                "id": inst.id,
                "pid": inst.pid,
                "name": inst.name,
                "type": inst.type,
                "state": inst.state,
                "regional_office": inst.regional_office,
                "head_name": inst.head_of_inst_name,
                "head_email": inst.head_of_inst_email,
                "head_phone": inst.head_of_inst_phone
            } if inst else None,
            "documents": [
                {
                    "id": d.id,
                    "document_type": d.document_type,
                    "file_name": d.file_name,
                    "file_size_bytes": d.file_size_bytes,
                    "sha256_hash": d.sha256_hash,
                    "ocr_processed": d.ocr_processed,
                    "ocr_confidence_score": d.ocr_confidence_score,
                    "uploaded_by": d.uploaded_by,
                    "created_at": d.created_at,
                    "file_url": f"/storage/documents/{d.file_name}"
                } for d in docs
            ],
            "verifications": [
                {
                    "id": v.id,
                    "verification_source": v.verification_source,
                    "verified_by_user": v.verified_by_user,
                    "bank_api_transaction_ref": v.bank_api_transaction_ref,
                    "is_valid": v.is_valid,
                    "bank_confirmed_amount": v.bank_confirmed_amount,
                    "bank_confirmed_maturity": v.bank_confirmed_maturity,
                    "remarks": v.remarks,
                    "verified_at": v.verified_at
                } for v in verifications
            ]
        }
    }

@router.post("")
def create_fdr(req: FDRCreateRequest, db: Session = Depends(get_db)):
    inst = db.query(Institution).filter(Institution.id == req.institution_id).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Check duplicate
    existing = db.query(FDRInstrument).filter(
        FDRInstrument.bank_name == req.bank_name,
        FDRInstrument.fdr_number == req.fdr_number
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="FDR Number already registered for this bank")

    fdr = FDRInstrument(
        institution_id=req.institution_id,
        fdr_number=req.fdr_number,
        account_number=req.account_number,
        instrument_type=req.instrument_type,
        bank_name=req.bank_name,
        branch_name=req.branch_name,
        ifsc_code=req.ifsc_code,
        deposit_amount=req.deposit_amount,
        rate_of_interest=req.rate_of_interest,
        issue_date=req.issue_date,
        maturity_date=req.maturity_date,
        statutory_lock_in_years=req.statutory_lock_in_years,
        statutory_lock_in_end_date=req.statutory_lock_in_end_date,
        lien_marked=req.lien_marked,
        lien_reference_number=req.lien_reference_number,
        predecessor_fdr_id=req.predecessor_fdr_id,
        status="UNDER_SCRUTINY",
        verification_level="SELF_DECLARED",
        is_discrepant=False
    )
    db.add(fdr)
    db.flush()

    # Automatically generate corresponding sample certificate document
    doc_filename = f"fdr_{fdr.fdr_number}.png"
    img_path = generate_fdr_sample_image(
        filename=doc_filename,
        fdr_number=fdr.fdr_number,
        bank_name=fdr.bank_name,
        branch_name=fdr.branch_name,
        ifsc_code=fdr.ifsc_code,
        institution_name=inst.name,
        deposit_amount=fdr.deposit_amount,
        issue_date=fdr.issue_date,
        maturity_date=fdr.maturity_date,
        is_lien_marked=fdr.lien_marked
    )

    doc = FDRDocument(
        fdr_id=fdr.id,
        document_type="FDR_CERTIFICATE",
        file_name=doc_filename,
        storage_path=img_path,
        mime_type="image/png",
        file_size_bytes=os.path.getsize(img_path),
        sha256_hash=compute_file_sha256(img_path),
        ocr_processed=False,
        uploaded_by=inst.head_of_inst_name
    )
    db.add(doc)
    db.commit()
    db.refresh(fdr)

    log_audit_event(
        db=db,
        entity_name="fdr_instruments",
        entity_id=fdr.id,
        action_type="REGISTER_FDR",
        actor_id=inst.head_of_inst_email,
        actor_role="INSTITUTION_ADMIN",
        new_state={
            "fdr_number": fdr.fdr_number,
            "deposit_amount": fdr.deposit_amount,
            "bank_name": fdr.bank_name,
            "status": fdr.status
        }
    )

    return {"success": True, "fdr_id": fdr.id, "status": fdr.status}

@router.post("/{fdr_id}/upload-document")
async def upload_fdr_document(
    fdr_id: str,
    file: UploadFile = File(...),
    document_type: str = Form("FDR_CERTIFICATE"),
    db: Session = Depends(get_db)
):
    fdr = db.query(FDRInstrument).filter(FDRInstrument.id == fdr_id).first()
    if not fdr:
        raise HTTPException(status_code=404, detail="FDR instrument not found")

    filename = f"{fdr.fdr_number}_{file.filename}"
    save_path = DOCS_DIR / filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    sha256_hash = compute_file_sha256(save_path)
    file_size = os.path.getsize(save_path)

    doc = FDRDocument(
        fdr_id=fdr.id,
        document_type=document_type,
        file_name=filename,
        storage_path=str(save_path),
        mime_type=file.content_type or "application/octet-stream",
        file_size_bytes=file_size,
        sha256_hash=sha256_hash,
        ocr_processed=False,
        uploaded_by="INSTITUTION_PORTAL_USER"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    log_audit_event(
        db=db,
        entity_name="fdr_documents",
        entity_id=doc.id,
        action_type="UPLOAD_DOCUMENT",
        actor_id="INSTITUTION_USER",
        actor_role="INSTITUTION_ADMIN",
        new_state={"file_name": filename, "sha256_hash": sha256_hash}
    )

    return {
        "success": True,
        "document_id": doc.id,
        "file_name": doc.file_name,
        "sha256_hash": sha256_hash
    }
