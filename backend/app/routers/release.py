import hashlib
import secrets
from datetime import datetime, timezone
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.app.database import get_db
from backend.app.models import FDRInstrument, Institution, FDRReleaseRequest
from backend.app.services.document_generator import generate_release_noc_pdf
from backend.app.services.audit_service import log_audit_event

router = APIRouter(prefix="/api/release", tags=["Multi-Tier Release & Refund Workflow"])

class SubmitReleaseRequest(BaseModel):
    fdr_id: str
    reason: str

class ScrutinyStageRequest(BaseModel):
    officer_name: str
    is_approved: bool
    comments: Optional[str] = "Statutory lock-in tenure verified. No pending fee complaints or litigation on record."

class ROStageRequest(BaseModel):
    ro_name: str
    is_recommended: bool
    comments: Optional[str] = "Regional Directorate concurs with scrutiny report. Recommend discharge of lien."

class AuthorizeStageRequest(BaseModel):
    authorizer_name: str
    aadhaar_esign_simulated: Optional[bool] = True
    pin: Optional[str] = "123456"

@router.get("/requests")
def list_release_requests(db: Session = Depends(get_db)):
    reqs = db.query(FDRReleaseRequest).order_by(FDRReleaseRequest.created_at.desc()).all()
    results = []
    for r in reqs:
        fdr = r.fdr
        inst = r.institution
        results.append({
            "id": r.id,
            "fdr_id": r.fdr_id,
            "fdr_number": fdr.fdr_number if fdr else "N/A",
            "bank_name": fdr.bank_name if fdr else "N/A",
            "institution_id": r.institution_id,
            "institution_name": inst.name if inst else "N/A",
            "institution_pid": inst.pid if inst else "N/A",
            "requested_amount": r.requested_amount,
            "reason": r.reason_for_release,
            "scrutiny_status": r.scrutiny_status,
            "scrutiny_by": r.scrutiny_by,
            "ro_recommendation": r.ro_recommendation,
            "ro_by": r.ro_by,
            "final_authorization": r.final_authorization,
            "authorized_by": r.authorized_by,
            "authorized_at": r.authorized_at,
            "has_noc": r.noc_document_path is not None,
            "created_at": r.created_at
        })

    return {"requests": results, "total": len(results)}

@router.post("/submit")
def submit_release_request(body: SubmitReleaseRequest, db: Session = Depends(get_db)):
    fdr = db.query(FDRInstrument).filter(FDRInstrument.id == body.fdr_id).first()
    if not fdr:
        raise HTTPException(status_code=404, detail="FDR instrument not found")

    existing = db.query(FDRReleaseRequest).filter(
        FDRReleaseRequest.fdr_id == fdr.id,
        FDRReleaseRequest.final_authorization != "REJECTED"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="A release request is already active for this FDR")

    req = FDRReleaseRequest(
        fdr_id=fdr.id,
        institution_id=fdr.institution_id,
        requested_amount=fdr.deposit_amount,
        reason_for_release=body.reason,
        scrutiny_status="PENDING",
        ro_recommendation="PENDING",
        final_authorization="PENDING"
    )
    db.add(req)
    fdr.status = "RELEASE_REQUESTED"
    db.commit()
    db.refresh(req)

    log_audit_event(
        db=db,
        entity_name="fdr_release_requests",
        entity_id=req.id,
        action_type="SUBMIT_RELEASE_REQUEST",
        actor_id=fdr.institution.head_of_inst_email if fdr.institution else "INSTITUTION",
        actor_role="INSTITUTION_ADMIN",
        new_state={"requested_amount": req.requested_amount, "fdr_number": fdr.fdr_number}
    )

    return {"success": True, "request_id": req.id, "status": "RELEASE_REQUESTED"}

@router.post("/{req_id}/scrutiny")
def maker_scrutiny_step(req_id: str, body: ScrutinyStageRequest, db: Session = Depends(get_db)):
    """
    Tier 1 (Maker): Scrutiny Officer verification step.
    """
    req = db.query(FDRReleaseRequest).filter(FDRReleaseRequest.id == req_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Release request not found")

    req.scrutiny_status = "APPROVED" if body.is_approved else "REJECTED"
    req.scrutiny_by = body.officer_name
    req.scrutiny_comments = body.comments
    req.scrutiny_at = datetime.now(timezone.utc)
    db.commit()

    log_audit_event(
        db=db,
        entity_name="fdr_release_requests",
        entity_id=req.id,
        action_type="MAKER_SCRUTINY_DECISION",
        actor_id=body.officer_name,
        actor_role="SCRUTINY_OFFICER",
        new_state={"scrutiny_status": req.scrutiny_status, "comments": req.scrutiny_comments}
    )

    return {"success": True, "request_id": req.id, "scrutiny_status": req.scrutiny_status}

@router.post("/{req_id}/ro-review")
def checker_ro_step(req_id: str, body: ROStageRequest, db: Session = Depends(get_db)):
    """
    Tier 2 (Checker): Regional Officer review step.
    """
    req = db.query(FDRReleaseRequest).filter(FDRReleaseRequest.id == req_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Release request not found")

    if req.scrutiny_status != "APPROVED":
        raise HTTPException(status_code=400, detail="Cannot review before Scrutiny Officer approval (Maker-Checker violation).")

    req.ro_recommendation = "RECOMMENDED" if body.is_recommended else "REJECTED"
    req.ro_by = body.ro_name
    req.ro_comments = body.comments
    req.ro_at = datetime.now(timezone.utc)
    db.commit()

    log_audit_event(
        db=db,
        entity_name="fdr_release_requests",
        entity_id=req.id,
        action_type="CHECKER_RO_RECOMMENDATION",
        actor_id=body.ro_name,
        actor_role="REGIONAL_OFFICER",
        new_state={"ro_recommendation": req.ro_recommendation, "comments": req.ro_comments}
    )

    return {"success": True, "request_id": req.id, "ro_recommendation": req.ro_recommendation}

@router.post("/{req_id}/authorize")
def authorizer_bureau_chief_step(req_id: str, body: AuthorizeStageRequest, db: Session = Depends(get_db)):
    """
    Tier 3 (Authorizer): Regulation Bureau Chief approval with simulated Aadhaar e-Sign / DSC Token.
    Generates official cryptographic Release NOC PDF.
    """
    req = db.query(FDRReleaseRequest).filter(FDRReleaseRequest.id == req_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Release request not found")

    if req.ro_recommendation != "RECOMMENDED":
        raise HTTPException(status_code=400, detail="Cannot authorize without Regional Officer recommendation.")

    fdr = req.fdr
    inst = req.institution

    # Cryptographic Aadhaar e-Sign / DSC Hash
    now_str = datetime.now(timezone.utc).isoformat()
    raw_sig_payload = f"AICTE_RELEASE|{fdr.fdr_number}|{body.authorizer_name}|{fdr.deposit_amount}|{now_str}"
    dsc_hash = "SHA256:DSC:" + hashlib.sha256(raw_sig_payload.encode()).hexdigest().upper()

    # Generate official NOC PDF
    noc_path = generate_release_noc_pdf(
        release_req_id=req.id,
        fdr_number=fdr.fdr_number,
        institution_name=inst.name,
        institution_pid=inst.pid,
        bank_name=fdr.bank_name,
        amount=fdr.deposit_amount,
        authorized_by=body.authorizer_name,
        digital_signature_hash=dsc_hash
    )

    req.final_authorization = "APPROVED"
    req.authorized_by = body.authorizer_name
    req.digital_signature_hash = dsc_hash
    req.authorized_at = datetime.now(timezone.utc)
    req.noc_document_path = noc_path

    fdr.status = "RELEASED_DISCHARGED"
    fdr.lien_marked = False
    db.commit()

    log_audit_event(
        db=db,
        entity_name="fdr_release_requests",
        entity_id=req.id,
        action_type="AUTHORIZER_BUREAU_CHIEF_APPROVAL",
        actor_id=body.authorizer_name,
        actor_role="BUREAU_CHIEF",
        new_state={
            "final_authorization": "APPROVED",
            "fdr_status": fdr.status,
            "dsc_hash": dsc_hash,
            "noc_path": noc_path
        }
    )

    return {
        "success": True,
        "request_id": req.id,
        "fdr_number": fdr.fdr_number,
        "final_status": fdr.status,
        "digital_signature_hash": dsc_hash,
        "noc_download_url": f"/api/release/{req.id}/noc-download"
    }

@router.get("/{req_id}/noc-download")
def download_release_noc(req_id: str, db: Session = Depends(get_db)):
    req = db.query(FDRReleaseRequest).filter(FDRReleaseRequest.id == req_id).first()
    if not req or not req.noc_document_path or not Path(req.noc_document_path).exists():
        raise HTTPException(status_code=404, detail="No generated NOC document found for this request")

    return FileResponse(
        req.noc_document_path,
        media_type="application/pdf",
        filename=Path(req.noc_document_path).name
    )
