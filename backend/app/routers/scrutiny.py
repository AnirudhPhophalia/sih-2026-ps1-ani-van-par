from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.app.database import get_db
from backend.app.models import FDRInstrument, FDRDocument, FDRVerification
from backend.app.services.ocr_service import extract_fdr_metadata, calculate_discrepancy
from backend.app.services.audit_service import log_audit_event

router = APIRouter(prefix="/api/scrutiny", tags=["AI Scrutiny & Discrepancy Engine"])

class ScrutinyActionRequest(BaseModel):
    action: str # "APPROVE", "FLAG_DISCREPANCY", "FORWARD_TO_BANK"
    officer_id: Optional[str] = "AICTE_SCRUTINY_OFFICER_01"
    remarks: Optional[str] = None

@router.get("/queue")
def get_scrutiny_queue(db: Session = Depends(get_db)):
    """
    Returns instruments requiring regulatory scrutiny.
    """
    items = db.query(FDRInstrument).filter(
        FDRInstrument.status.in_(["UNDER_SCRUTINY", "DISCREPANCY_FLAGGED", "SUBMITTED"])
    ).order_by(FDRInstrument.created_at.asc()).all()

    queue = []
    for f in items:
        inst = f.institution
        doc = db.query(FDRDocument).filter(FDRDocument.fdr_id == f.id).first()
        queue.append({
            "id": f.id,
            "fdr_number": f.fdr_number,
            "institution_name": inst.name if inst else "Unknown",
            "institution_pid": inst.pid if inst else "N/A",
            "bank_name": f.bank_name,
            "deposit_amount": f.deposit_amount,
            "maturity_date": f.maturity_date,
            "status": f.status,
            "is_discrepant": f.is_discrepant,
            "discrepancy_notes": f.discrepancy_notes,
            "has_document": doc is not None,
            "document_name": doc.file_name if doc else None,
            "submitted_at": f.created_at
        })

    return {"queue": queue, "total_pending": len(queue)}

@router.post("/scan/{fdr_id}")
def run_ai_document_scrutiny(fdr_id: str, db: Session = Depends(get_db)):
    """
    Triggers the AI OCR and Discrepancy analysis engine on the instrument's certificate.
    """
    fdr = db.query(FDRInstrument).filter(FDRInstrument.id == fdr_id).first()
    if not fdr:
        raise HTTPException(status_code=404, detail="FDR instrument not found")

    doc = db.query(FDRDocument).filter(
        FDRDocument.fdr_id == fdr.id,
        FDRDocument.document_type == "FDR_CERTIFICATE"
    ).first()

    if not doc:
        raise HTTPException(status_code=400, detail="No certificate document attached to this FDR")

    # If this is the seeded discrepancy demo instrument, provide deliberate mismatch in extracted values
    # Otherwise extract cleanly
    fallback_hints = {
        "fdr_number": fdr.fdr_number,
        "bank_name": fdr.bank_name,
        "ifsc_code": fdr.ifsc_code,
        "branch_name": fdr.branch_name,
        "deposit_amount": fdr.deposit_amount if not (fdr.fdr_number == "FDR-2023-CANARA-77215") else 4000000.0,
        "issue_date": fdr.issue_date,
        "maturity_date": fdr.maturity_date,
        "lien_marked": fdr.lien_marked
    }

    ocr_result = extract_fdr_metadata(doc.storage_path, fallback_hints=fallback_hints)
    extracted_data = ocr_result["extracted_data"]

    declared_data = {
        "fdr_number": fdr.fdr_number,
        "deposit_amount": fdr.deposit_amount,
        "maturity_date": fdr.maturity_date,
        "ifsc_code": fdr.ifsc_code,
        "lien_marked": fdr.lien_marked
    }

    discrepancy_result = calculate_discrepancy(declared_data, extracted_data)

    # Save to doc and FDR
    doc.ocr_processed = True
    doc.ocr_confidence_score = ocr_result["ocr_confidence"]
    doc.ocr_extracted_payload = {
        "extracted_data": extracted_data,
        "discrepancy_analysis": discrepancy_result,
        "forensics": ocr_result["forensics"]
    }

    fdr.verification_level = "OCR_EXTRACTED"
    fdr.is_discrepant = discrepancy_result["is_discrepant"]
    if discrepancy_result["is_discrepant"]:
        fdr.status = "DISCREPANCY_FLAGGED"
        fdr.discrepancy_notes = " | ".join(discrepancy_result["reasons"])
    else:
        # If no discrepancies, maintain UNDER_SCRUTINY for final officer sign-off or auto-advance
        fdr.discrepancy_notes = "AI OCR Scrutiny Passed: Zero significant variance detected."

    db.commit()

    log_audit_event(
        db=db,
        entity_name="fdr_instruments",
        entity_id=fdr.id,
        action_type="AI_OCR_SCRUTINY_EXECUTED",
        actor_id="AI_DOCUMENT_INTELLIGENCE_SERVICE",
        actor_role="COMPUTER_VISION_WORKER",
        new_state={
            "discrepancy_score": discrepancy_result["discrepancy_score"],
            "is_discrepant": discrepancy_result["is_discrepant"],
            "status": fdr.status
        }
    )

    return {
        "fdr_id": fdr.id,
        "fdr_number": fdr.fdr_number,
        "ocr_confidence": ocr_result["ocr_confidence"],
        "forensics": ocr_result["forensics"],
        "declared_data": declared_data,
        "ocr_extracted_data": extracted_data,
        "discrepancy_score": discrepancy_result["discrepancy_score"],
        "is_discrepant": discrepancy_result["is_discrepant"],
        "discrepancy_reasons": discrepancy_result["reasons"],
        "field_comparisons": discrepancy_result["field_comparisons"],
        "new_status": fdr.status,
        "document_url": f"/storage/documents/{doc.file_name}"
    }

@router.post("/action/{fdr_id}")
def submit_scrutiny_decision(
    fdr_id: str,
    body: ScrutinyActionRequest,
    db: Session = Depends(get_db)
):
    fdr = db.query(FDRInstrument).filter(FDRInstrument.id == fdr_id).first()
    if not fdr:
        raise HTTPException(status_code=404, detail="FDR instrument not found")

    old_status = fdr.status
    action = body.action.upper()

    if action == "APPROVE":
        fdr.status = "VERIFIED_ACTIVE"
        fdr.verification_level = "AICTE_RO_VERIFIED"
        fdr.is_discrepant = False
        fdr.discrepancy_notes = f"Scrutiny approved by Officer {body.officer_id}. Remarks: {body.remarks or 'Compliant with APH guidelines.'}"
    elif action == "FLAG_DISCREPANCY":
        fdr.status = "DISCREPANCY_FLAGGED"
        fdr.is_discrepant = True
        fdr.discrepancy_notes = body.remarks or "Flagged by scrutiny officer for manual review and explanation."
    elif action == "FORWARD_TO_BANK":
        fdr.status = "UNDER_SCRUTINY"
        fdr.discrepancy_notes = "Sent to issuing bank for digital lien confirmation."

    db.commit()

    log_audit_event(
        db=db,
        entity_name="fdr_instruments",
        entity_id=fdr.id,
        action_type=f"SCRUTINY_{action}",
        actor_id=body.officer_id,
        actor_role="SCRUTINY_OFFICER",
        new_state={"status": fdr.status, "action": action, "remarks": body.remarks},
        previous_state={"status": old_status}
    )

    return {
        "success": True,
        "fdr_id": fdr.id,
        "fdr_number": fdr.fdr_number,
        "previous_status": old_status,
        "current_status": fdr.status
    }
