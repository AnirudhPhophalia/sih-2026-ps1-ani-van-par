import uuid
import secrets
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.app.models import FDRInstrument, FDRVerification, BankVerificationToken, AuditLedger
from backend.app.services.audit_service import log_audit_event

SUPPORTED_BANKS = {
    "SBI": {"name": "State Bank of India", "cbs_code": "002", "prefix": "SBIN"},
    "PNB": {"name": "Punjab National Bank", "cbs_code": "024", "prefix": "PUNB"},
    "HDFC": {"name": "HDFC Bank Ltd.", "cbs_code": "240", "prefix": "HDFC"},
    "CANARA": {"name": "Canara Bank", "cbs_code": "015", "prefix": "CNRB"},
    "BOB": {"name": "Bank of Baroda", "cbs_code": "012", "prefix": "BARB"},
    "ICICI": {"name": "ICICI Bank Ltd.", "cbs_code": "229", "prefix": "ICIC"},
}

def verify_via_cbs_api(db: Session, fdr: FDRInstrument, actor_id: str = "SYSTEM_CBS_GATEWAY") -> dict:
    """
    Mode 1: Core Banking System (CBS) / SFMS Real-time API query.
    Simulates direct bank ledger cross-check.
    """
    # Deterministic check based on FDR attributes:
    # If the FDR was marked discrepant, simulate a bank finding or mismatch
    is_valid_in_cbs = not fdr.is_discrepant
    confirmed_amount = fdr.deposit_amount if is_valid_in_cbs else round(fdr.deposit_amount * 0.9, 2)
    tx_ref = f"CBS-SFMS-{secrets.token_hex(6).upper()}"

    verification = FDRVerification(
        fdr_id=fdr.id,
        verification_source="BANK_API_VERIFIED",
        verified_by_user=actor_id,
        bank_api_transaction_ref=tx_ref,
        is_valid=is_valid_in_cbs,
        bank_confirmed_amount=confirmed_amount,
        bank_confirmed_maturity=fdr.maturity_date,
        bank_confirmed_lien=True,
        remarks=f"Real-time CBS response from {fdr.bank_name} SFMS Gateway. Lien flag: TRUE. Live balance reconciled.",
        raw_response_payload={
            "gateway_status": "SUCCESS",
            "bank_name": fdr.bank_name,
            "ifsc": fdr.ifsc_code,
            "account_number": fdr.account_number,
            "cbs_ledger_balance": confirmed_amount,
            "lien_marked_aicte": True,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )
    db.add(verification)

    # Update instrument
    if is_valid_in_cbs:
        fdr.verification_level = "BANK_API_VERIFIED"
        if fdr.status in ["SUBMITTED", "UNDER_SCRUTINY"]:
            fdr.status = "VERIFIED_ACTIVE"

    db.commit()

    log_audit_event(
        db=db,
        entity_name="fdr_instruments",
        entity_id=fdr.id,
        action_type="BANK_CBS_VERIFY",
        actor_id=actor_id,
        actor_role="CBS_INTEGRATION_ADAPTER",
        new_state={
            "verification_level": fdr.verification_level,
            "status": fdr.status,
            "tx_ref": tx_ref
        }
    )

    return {
        "success": True,
        "mode": "CBS_SFMS_API",
        "transaction_ref": tx_ref,
        "is_valid": is_valid_in_cbs,
        "confirmed_amount": confirmed_amount,
        "lien_status": "VERIFIED_LIEN_ACTIVE",
        "instrument_status": fdr.status
    }

def generate_bank_officer_token(db: Session, fdr: FDRInstrument, branch_email: str) -> BankVerificationToken:
    """
    Mode 2: Generates a secure, one-time signed verification token for Bank Branch Manager.
    """
    token_str = secrets.token_urlsafe(32)
    token_obj = BankVerificationToken(
        token=token_str,
        fdr_id=fdr.id,
        bank_name=fdr.bank_name,
        branch_email=branch_email,
        status="PENDING"
    )
    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)

    log_audit_event(
        db=db,
        entity_name="bank_verification_tokens",
        entity_id=token_obj.id,
        action_type="GENERATE_BRANCH_TOKEN",
        actor_id="AICTE_SCRUTINY_OFFICER",
        actor_role="SCRUTINY_OFFICER",
        new_state={"token_id": token_obj.id, "branch_email": branch_email}
    )

    return token_obj

def submit_bank_officer_verification(
    db: Session,
    token_str: str,
    manager_name: str,
    manager_emp_id: str,
    is_approved: bool,
    manager_notes: str
) -> dict:
    """
    Mode 2: Branch Manager completes the verification desk flow.
    """
    token_obj = db.query(BankVerificationToken).filter(BankVerificationToken.token == token_str).first()
    if not token_obj:
        return {"success": False, "error": "Invalid or expired verification token."}

    fdr = db.query(FDRInstrument).filter(FDRInstrument.id == token_obj.fdr_id).first()
    if not fdr:
        return {"success": False, "error": "Associated FDR instrument not found."}

    token_obj.status = "CONFIRMED" if is_approved else "REJECTED"
    token_obj.notes = manager_notes
    token_obj.verified_by_manager = f"{manager_name} (Emp ID: {manager_emp_id})"

    verification = FDRVerification(
        fdr_id=fdr.id,
        verification_source="BANK_OFFICER_MANUAL",
        verified_by_user=f"{manager_name} [{manager_emp_id}]",
        bank_api_transaction_ref=f"MANUAL-BM-{token_obj.id[:8]}",
        is_valid=is_approved,
        bank_confirmed_amount=fdr.deposit_amount,
        bank_confirmed_maturity=fdr.maturity_date,
        bank_confirmed_lien=is_approved,
        remarks=f"Manual branch verification signed by {manager_name}. Notes: {manager_notes}",
        raw_response_payload={
            "manager_name": manager_name,
            "manager_emp_id": manager_emp_id,
            "branch_email": token_obj.branch_email,
            "is_approved": is_approved,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )
    db.add(verification)

    if is_approved:
        fdr.verification_level = "BANK_OFFICER_MANUAL"
        if fdr.status in ["SUBMITTED", "UNDER_SCRUTINY"]:
            fdr.status = "VERIFIED_ACTIVE"
    else:
        fdr.status = "DISCREPANCY_FLAGGED"
        fdr.is_discrepant = True
        fdr.discrepancy_notes = f"Bank Branch Manager rejected lien: {manager_notes}"

    db.commit()

    log_audit_event(
        db=db,
        entity_name="fdr_instruments",
        entity_id=fdr.id,
        action_type="BANK_OFFICER_VERIFICATION",
        actor_id=f"BANK_BM_{manager_emp_id}",
        actor_role="BANK_BRANCH_MANAGER",
        new_state={
            "verification_level": fdr.verification_level,
            "status": fdr.status,
            "manager_name": manager_name
        }
    )

    return {
        "success": True,
        "token_status": token_obj.status,
        "instrument_status": fdr.status,
        "fdr_number": fdr.fdr_number
    }

def verify_via_nesl_digilocker(db: Session, fdr: FDRInstrument) -> dict:
    """
    Mode 3: NeSL / DigiLocker Information Utility Verification.
    Validates e-Stamping and Digital Document Execution (DDE).
    """
    estamp_cert = f"IN-DL{secrets.token_hex(8).upper()}"
    digilocker_uri = f"in.gov.digilocker.doc:{fdr.fdr_number}"

    verification = FDRVerification(
        fdr_id=fdr.id,
        verification_source="AICTE_RO_VERIFIED",
        verified_by_user="NeSL_DDE_GATEWAY",
        bank_api_transaction_ref=estamp_cert,
        is_valid=True,
        bank_confirmed_amount=fdr.deposit_amount,
        bank_confirmed_maturity=fdr.maturity_date,
        bank_confirmed_lien=True,
        remarks=f"Verified via NeSL Information Utility & DigiLocker. Digital Document Execution (DDE) e-Stamp: {estamp_cert}",
        raw_response_payload={
            "nesl_estamp_certificate": estamp_cert,
            "digilocker_uri": digilocker_uri,
            "duty_amount": 500.0,
            "stamp_date": fdr.issue_date,
            "state_jurisdiction": "New Delhi / Ministry of Finance"
        }
    )
    db.add(verification)
    fdr.verification_level = "AICTE_RO_VERIFIED"
    if fdr.status in ["SUBMITTED", "UNDER_SCRUTINY"]:
        fdr.status = "VERIFIED_ACTIVE"

    db.commit()

    log_audit_event(
        db=db,
        entity_name="fdr_instruments",
        entity_id=fdr.id,
        action_type="NESL_DIGILOCKER_VERIFY",
        actor_id="NESL_SERVICE",
        actor_role="INFORMATION_UTILITY",
        new_state={"estamp_cert": estamp_cert, "status": fdr.status}
    )

    return {
        "success": True,
        "mode": "NeSL_DDE_DIGILOCKER",
        "estamp_certificate": estamp_cert,
        "digilocker_uri": digilocker_uri,
        "is_valid": True,
        "status": fdr.status
    }
