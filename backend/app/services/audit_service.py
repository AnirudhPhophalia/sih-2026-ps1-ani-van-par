import hashlib
import json
from sqlalchemy.orm import Session
from backend.app.models import AuditLedger

GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

def compute_record_hash(entity_name: str, entity_id: str, action_type: str, actor_id: str, new_state: dict, prev_hash: str) -> str:
    state_str = json.dumps(new_state or {}, sort_keys=True, default=str)
    raw = f"{entity_name}|{entity_id}|{action_type}|{actor_id}|{state_str}|{prev_hash}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def log_audit_event(
    db: Session,
    entity_name: str,
    entity_id: str,
    action_type: str,
    actor_id: str,
    actor_role: str,
    new_state: dict = None,
    previous_state: dict = None,
    actor_ip: str = "127.0.0.1"
) -> AuditLedger:
    last_record = db.query(AuditLedger).order_by(AuditLedger.id.desc()).first()
    prev_hash = last_record.record_hash if last_record else GENESIS_HASH

    current_hash = compute_record_hash(
        entity_name=entity_name,
        entity_id=entity_id,
        action_type=action_type,
        actor_id=actor_id,
        new_state=new_state or {},
        prev_hash=prev_hash
    )

    entry = AuditLedger(
        entity_name=entity_name,
        entity_id=str(entity_id),
        action_type=action_type,
        actor_id=actor_id,
        actor_role=actor_role,
        actor_ip=actor_ip,
        previous_state=previous_state,
        new_state=new_state,
        prev_record_hash=prev_hash,
        record_hash=current_hash
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def verify_audit_integrity(db: Session):
    records = db.query(AuditLedger).order_by(AuditLedger.id.asc()).all()
    if not records:
        return {
            "is_valid": True,
            "total_records": 0,
            "tampered_index": None,
            "message": "Audit ledger is empty (Genesis state)."
        }

    expected_prev = GENESIS_HASH
    for idx, rec in enumerate(records):
        # 1. Check parent hash linkage
        if rec.prev_record_hash != expected_prev:
            return {
                "is_valid": False,
                "total_records": len(records),
                "tampered_index": rec.id,
                "reason": f"Broken chain link at Block #{rec.id}. Expected previous hash {expected_prev[:12]}... but got {rec.prev_record_hash[:12]}...",
                "block_details": {
                    "id": rec.id,
                    "action": rec.action_type,
                    "entity": f"{rec.entity_name} ({rec.entity_id})",
                    "actor": rec.actor_id
                }
            }

        # 2. Check internal record hash
        recalculated_hash = compute_record_hash(
            entity_name=rec.entity_name,
            entity_id=rec.entity_id,
            action_type=rec.action_type,
            actor_id=rec.actor_id,
            new_state=rec.new_state or {},
            prev_hash=expected_prev
        )

        if recalculated_hash != rec.record_hash:
            return {
                "is_valid": False,
                "total_records": len(records),
                "tampered_index": rec.id,
                "reason": f"Cryptographic signature mismatch at Block #{rec.id}! Data content was modified out-of-band.",
                "block_details": {
                    "id": rec.id,
                    "action": rec.action_type,
                    "entity": f"{rec.entity_name} ({rec.entity_id})",
                    "actor": rec.actor_id,
                    "stored_hash": rec.record_hash,
                    "recalculated_hash": recalculated_hash
                }
            }

        expected_prev = rec.record_hash

    return {
        "is_valid": True,
        "total_records": len(records),
        "tampered_index": None,
        "message": f"Cryptographic integrity verified! All {len(records)} blocks in the Merkle-hash chain are valid and untampered.",
        "latest_block_hash": expected_prev
    }

def simulate_tamper(db: Session, record_id: int, forged_amount: float = 99999999.0):
    record = db.query(AuditLedger).filter(AuditLedger.id == record_id).first()
    if not record:
        return {"success": False, "error": "Record not found"}

    # Maliciously modify the state without updating hash
    state = dict(record.new_state or {})
    state["deposit_amount"] = forged_amount
    state["_tampered_flag"] = "MALICIOUS_UNAUTHORIZED_MODIFICATION"
    record.new_state = state
    db.commit()

    return {
        "success": True,
        "message": f"Simulated unauthorized database tampering at Block #{record_id}. The cryptographic checksum is now invalid.",
        "record_id": record_id
    }
