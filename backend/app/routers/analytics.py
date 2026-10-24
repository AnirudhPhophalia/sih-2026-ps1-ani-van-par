from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.database import get_db
from backend.app.models import FDRInstrument, Institution, FDRAlert, AuditLedger

router = APIRouter(prefix="/api/analytics", tags=["National Executive Analytics"])

@router.get("/dashboard")
def get_executive_dashboard(db: Session = Depends(get_db)):
    total_institutions = db.query(Institution).count()
    total_fdrs = db.query(FDRInstrument).count()

    total_capital_raw = db.query(func.sum(FDRInstrument.deposit_amount)).scalar() or 0.0
    total_capital_crores = round(total_capital_raw / 10000000.0, 2)

    # Status Breakdown
    statuses = db.query(FDRInstrument.status, func.count(FDRInstrument.id)).group_by(FDRInstrument.status).all()
    status_dict = {s[0]: s[1] for s in statuses}

    # Verification Levels
    verif_levels = db.query(FDRInstrument.verification_level, func.count(FDRInstrument.id)).group_by(FDRInstrument.verification_level).all()
    verif_dict = {v[0]: v[1] for v in verif_levels}

    # Bank-wise Distribution
    banks = db.query(
        FDRInstrument.bank_name,
        func.count(FDRInstrument.id),
        func.sum(FDRInstrument.deposit_amount)
    ).group_by(FDRInstrument.bank_name).all()

    bank_distribution = [
        {
            "bank_name": b[0],
            "fdr_count": b[1],
            "total_amount": float(b[2] or 0),
            "amount_crores": round(float(b[2] or 0) / 10000000.0, 2)
        } for b in banks
    ]

    # State & Zone Distribution
    state_data = db.query(
        Institution.state,
        Institution.regional_office,
        func.count(FDRInstrument.id),
        func.sum(FDRInstrument.deposit_amount)
    ).join(FDRInstrument, Institution.id == FDRInstrument.institution_id, isouter=True).group_by(
        Institution.state, Institution.regional_office
    ).all()

    regional_distribution = [
        {
            "state": s[0],
            "regional_office": s[1],
            "fdr_count": s[2],
            "total_amount": float(s[3] or 0),
            "amount_crores": round(float(s[3] or 0) / 10000000.0, 2)
        } for s in state_data if s[2] > 0
    ]

    # Alerts summary
    unresolved_alerts = db.query(FDRAlert).filter(FDRAlert.is_resolved == False).count()
    critical_alerts = db.query(FDRAlert).filter(
        FDRAlert.is_resolved == False,
        FDRAlert.severity.in_(["CRITICAL", "ESCALATION"])
    ).count()

    total_audit_blocks = db.query(AuditLedger).count()

    return {
        "kpis": {
            "total_capital_crores": total_capital_crores,
            "total_capital_inr": total_capital_raw,
            "total_institutions": total_institutions,
            "total_fdrs": total_fdrs,
            "active_fdrs": status_dict.get("VERIFIED_ACTIVE", 0),
            "expiring_soon": status_dict.get("MATURITY_APPROACHING", 0),
            "matured_overdue": status_dict.get("MATURED_PENDING_RENEWAL", 0),
            "under_scrutiny": status_dict.get("UNDER_SCRUTINY", 0),
            "discrepancies_flagged": status_dict.get("DISCREPANCY_FLAGGED", 0),
            "release_requested": status_dict.get("RELEASE_REQUESTED", 0),
            "released_discharged": status_dict.get("RELEASED_DISCHARGED", 0),
            "unresolved_alerts": unresolved_alerts,
            "critical_alerts": critical_alerts,
            "total_audit_blocks": total_audit_blocks
        },
        "status_distribution": status_dict,
        "verification_distribution": verif_dict,
        "bank_distribution": bank_distribution,
        "regional_distribution": regional_distribution
    }
