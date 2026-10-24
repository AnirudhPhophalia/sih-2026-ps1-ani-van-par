from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.app.database import get_db
from backend.app.models import FDRAlert, FDRInstrument, Institution
from backend.app.services.maturity_engine import run_national_maturity_sweep

router = APIRouter(prefix="/api/maturity", tags=["Validity, Maturity & Escalations"])

class RunSweepRequest(BaseModel):
    simulated_date: Optional[str] = None # YYYY-MM-DD

@router.get("/alerts")
def list_alerts(
    severity: Optional[str] = Query(None),
    escalation_tier: Optional[int] = Query(None),
    is_resolved: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(FDRAlert)
    if severity:
        query = query.filter(FDRAlert.severity == severity.upper())
    if escalation_tier is not None:
        query = query.filter(FDRAlert.escalation_tier == escalation_tier)
    if is_resolved is not None:
        query = query.filter(FDRAlert.is_resolved == is_resolved)

    alerts = query.order_by(FDRAlert.created_at.desc()).all()
    results = []
    for a in alerts:
        fdr = a.fdr
        inst = a.institution
        results.append({
            "id": a.id,
            "fdr_id": a.fdr_id,
            "fdr_number": fdr.fdr_number if fdr else "N/A",
            "institution_id": a.institution_id,
            "institution_name": inst.name if inst else "N/A",
            "institution_pid": inst.pid if inst else "N/A",
            "severity": a.severity,
            "alert_code": a.alert_code,
            "message": a.message,
            "channels_sent": a.channels_sent,
            "is_read": a.is_read,
            "is_resolved": a.is_resolved,
            "escalation_tier": a.escalation_tier,
            "created_at": a.created_at
        })

    return {"alerts": results, "total": len(results)}

@router.post("/run-sweep")
def trigger_national_sweep(body: Optional[RunSweepRequest] = None, db: Session = Depends(get_db)):
    """
    Executes an autonomous maturity sweep across all instruments in the repository.
    Can simulate time travel by passing simulated_date: 'YYYY-MM-DD'.
    """
    sim_date = body.simulated_date if body else None
    result = run_national_maturity_sweep(db, simulated_date_str=sim_date)
    return result

@router.post("/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: str, db: Session = Depends(get_db)):
    alert = db.query(FDRAlert).filter(FDRAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_resolved = True
    alert.is_read = True
    db.commit()

    return {"success": True, "alert_id": alert_id, "is_resolved": True}
