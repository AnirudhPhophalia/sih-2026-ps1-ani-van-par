from datetime import datetime, date, timedelta, timezone
from sqlalchemy.orm import Session
from backend.app.models import FDRInstrument, FDRAlert, Institution
from backend.app.services.audit_service import log_audit_event

def parse_date(d_str: str) -> date:
    try:
        return datetime.strptime(d_str, "%Y-%m-%d").date()
    except Exception:
        return date.today()

def evaluate_instrument_maturity(db: Session, fdr: FDRInstrument, ref_date: date = None) -> list[dict]:
    """
    Evaluates an individual FDR instrument against statutory lock-in and maturity dates.
    Generates milestone alerts and transitions state if appropriate.
    """
    if ref_date is None:
        ref_date = date.today()

    maturity_d = parse_date(fdr.maturity_date)
    lock_in_end_d = parse_date(fdr.statutory_lock_in_end_date)
    days_to_maturity = (maturity_d - ref_date).days
    days_to_lock_in_end = (lock_in_end_d - ref_date).days

    generated_alerts = []

    # State transitions
    old_status = fdr.status
    if fdr.status in ["VERIFIED_ACTIVE", "MATURITY_APPROACHING"]:
        if days_to_maturity <= 0:
            fdr.status = "MATURED_PENDING_RENEWAL"
        elif days_to_maturity <= 90:
            fdr.status = "MATURITY_APPROACHING"

    # Milestone checking
    # 1. Overdue (>0 days past maturity)
    if days_to_maturity < 0 and fdr.status == "MATURED_PENDING_RENEWAL":
        overdue_days = abs(days_to_maturity)
        tier = 3 if overdue_days > 30 else (2 if overdue_days > 15 else 1)
        severity = "ESCALATION" if tier == 3 else "CRITICAL"

        msg = (f"URGENT STATUTORY ALERT: FDR #{fdr.fdr_number} (₹{fdr.deposit_amount:,.2f}) for "
               f"{fdr.institution.name if fdr.institution else 'Institution'} matured on {fdr.maturity_date} "
               f"({overdue_days} days overdue). Renewal receipt not filed!")

        existing_alert = db.query(FDRAlert).filter(
            FDRAlert.fdr_id == fdr.id,
            FDRAlert.alert_code == "OVERDUE_RENEWAL",
            FDRAlert.escalation_tier == tier,
            FDRAlert.is_resolved == False
        ).first()

        if not existing_alert:
            alert = FDRAlert(
                fdr_id=fdr.id,
                institution_id=fdr.institution_id,
                severity=severity,
                alert_code="OVERDUE_RENEWAL",
                message=msg,
                channels_sent=["PORTAL", "EMAIL", "SMS", "WHATSAPP_NIC"],
                is_read=False,
                is_resolved=False,
                escalation_tier=tier
            )
            db.add(alert)
            generated_alerts.append({"type": "OVERDUE", "tier": tier, "message": msg})

    # 2. Approaching Maturity milestones: 180, 90, 30, 7 days
    elif days_to_maturity in range(0, 181):
        milestone = None
        tier = 1
        sev = "INFO"

        if days_to_maturity <= 7:
            milestone = "EXPIRY_7_DAYS"
            tier = 2
            sev = "CRITICAL"
        elif days_to_maturity <= 30:
            milestone = "EXPIRY_30_DAYS"
            tier = 1
            sev = "WARNING"
        elif days_to_maturity <= 90:
            milestone = "EXPIRY_90_DAYS"
            tier = 1
            sev = "INFO"
        elif days_to_maturity <= 180:
            milestone = "EXPIRY_180_DAYS"
            tier = 1
            sev = "INFO"

        if milestone:
            existing = db.query(FDRAlert).filter(
                FDRAlert.fdr_id == fdr.id,
                FDRAlert.alert_code == milestone,
                FDRAlert.is_resolved == False
            ).first()

            if not existing:
                msg = (f"AICTE Regulatory Notice: FDR #{fdr.fdr_number} of {fdr.bank_name} "
                       f"will mature in {days_to_maturity} days on {fdr.maturity_date}. "
                       f"Statutory lock-in ends {fdr.statutory_lock_in_end_date}. Prepare renewal documentation.")
                alert = FDRAlert(
                    fdr_id=fdr.id,
                    institution_id=fdr.institution_id,
                    severity=sev,
                    alert_code=milestone,
                    message=msg,
                    channels_sent=["PORTAL", "EMAIL"],
                    is_read=False,
                    is_resolved=False,
                    escalation_tier=tier
                )
                db.add(alert)
                generated_alerts.append({"type": milestone, "tier": tier, "message": msg})

    if old_status != fdr.status:
        log_audit_event(
            db=db,
            entity_name="fdr_instruments",
            entity_id=fdr.id,
            action_type="STATUS_TRANSITION_MATURITY",
            actor_id="AUTONOMOUS_MATURITY_ENGINE",
            actor_role="CRON_WORKER",
            new_state={"status": fdr.status, "days_to_maturity": days_to_maturity},
            previous_state={"status": old_status}
        )

    return generated_alerts

def run_national_maturity_sweep(db: Session, simulated_date_str: str = None) -> dict:
    """
    Executes a comprehensive audit sweep across all FDR instruments across India.
    Supports simulated time-travel to test alert triggers and transitions.
    """
    ref_d = parse_date(simulated_date_str) if simulated_date_str else date.today()
    all_fdrs = db.query(FDRInstrument).all()

    total_scanned = len(all_fdrs)
    status_counts = {}
    all_generated_alerts = []

    for fdr in all_fdrs:
        alerts = evaluate_instrument_maturity(db, fdr, ref_date=ref_d)
        all_generated_alerts.extend(alerts)
        status_counts[fdr.status] = status_counts.get(fdr.status, 0) + 1

    db.commit()

    return {
        "sweep_timestamp": datetime.now(timezone.utc).isoformat(),
        "reference_date": ref_d.isoformat(),
        "total_scanned": total_scanned,
        "new_alerts_triggered": len(all_generated_alerts),
        "status_distribution": status_counts,
        "alerts_sample": all_generated_alerts[:5]
    }
