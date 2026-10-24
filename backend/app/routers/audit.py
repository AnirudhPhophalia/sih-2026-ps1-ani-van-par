from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.app.database import get_db
from backend.app.models import AuditLedger
from backend.app.services.audit_service import verify_audit_integrity, simulate_tamper

router = APIRouter(prefix="/api/audit", tags=["Cryptographic Audit Ledger"])

class TamperSimulationRequest(BaseModel):
    block_id: int
    forged_amount: Optional[float] = 99999999.0

@router.get("/ledger")
def get_audit_ledger(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    action: Optional[str] = Query(None),
    actor: Optional[str] = Query(None),
    entity: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLedger)
    if action:
        query = query.filter(AuditLedger.action_type.ilike(f"%{action}%"))
    if actor:
        query = query.filter(AuditLedger.actor_id.ilike(f"%{actor}%"))
    if entity:
        query = query.filter(AuditLedger.entity_name.ilike(f"%{entity}%"))

    total = query.count()
    records = query.order_by(AuditLedger.id.desc()).offset(offset).limit(limit).all()

    return {
        "records": [
            {
                "id": r.id,
                "entity_name": r.entity_name,
                "entity_id": r.entity_id,
                "action_type": r.action_type,
                "actor_id": r.actor_id,
                "actor_role": r.actor_role,
                "actor_ip": r.actor_ip,
                "previous_state": r.previous_state,
                "new_state": r.new_state,
                "prev_record_hash": r.prev_record_hash,
                "record_hash": r.record_hash,
                "created_at": r.created_at
            } for r in records
        ],
        "total": total,
        "offset": offset,
        "limit": limit
    }

@router.get("/verify-chain")
def run_integrity_verification(db: Session = Depends(get_db)):
    """
    Validates cryptographic Merkle hash chaining across all blocks.
    Returns whether the ledger is pristine or tampered.
    """
    result = verify_audit_integrity(db)
    return result

@router.post("/simulate-tamper")
def trigger_tamper_simulation(body: TamperSimulationRequest, db: Session = Depends(get_db)):
    """
    Simulates malicious out-of-band database modification.
    """
    result = simulate_tamper(db, record_id=body.block_id, forged_amount=body.forged_amount)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result
