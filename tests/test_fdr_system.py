import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal, Base, engine
from backend.app.services.seed_data import seed_database_if_empty
from backend.app.services.audit_service import verify_audit_integrity, simulate_tamper

client = TestClient(app)

def setup_module():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database_if_empty(db)
    finally:
        db.close()

def test_health_check():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "OPERATIONAL"
    assert data["zero_trust_status"] == "ENFORCED"

def test_analytics_dashboard():
    res = client.get("/api/analytics/dashboard")
    assert res.status_code == 200
    data = res.json()
    assert "kpis" in data
    assert data["kpis"]["total_institutions"] >= 8
    assert data["kpis"]["total_fdrs"] >= 7
    assert data["kpis"]["total_capital_crores"] > 0

def test_fdr_repository_list_and_detail():
    res = client.get("/api/fdrs")
    assert res.status_code == 200
    data = res.json()
    assert len(data["fdrs"]) >= 7

    first_fdr = data["fdrs"][0]
    detail_res = client.get(f"/api/fdrs/{first_fdr['id']}")
    assert detail_res.status_code == 200
    detail = detail_res.json()["fdr"]
    assert detail["fdr_number"] == first_fdr["fdr_number"]
    assert len(detail["documents"]) >= 1
    assert len(detail["documents"][0]["sha256_hash"]) == 64

def test_ai_ocr_scrutiny_and_discrepancy():
    # Test seeded discrepancy instrument: FDR-2023-CANARA-77215
    res = client.get("/api/fdrs?search=FDR-2023-CANARA-77215")
    assert res.status_code == 200
    fdrs = res.json()["fdrs"]
    assert len(fdrs) > 0
    target_fdr = fdrs[0]

    scan_res = client.post(f"/api/scrutiny/scan/{target_fdr['id']}")
    assert scan_res.status_code == 200
    scan_data = scan_res.json()
    assert scan_data["is_discrepant"] is True
    assert scan_data["discrepancy_score"] > 0.05
    assert len(scan_data["discrepancy_reasons"]) > 0

def test_tri_modal_bank_gateway():
    res = client.get("/api/fdrs")
    fdr = res.json()["fdrs"][0]

    # Mode 1: CBS API
    cbs_res = client.post(f"/api/bank-gateway/cbs-verify/{fdr['id']}")
    assert cbs_res.status_code == 200
    cbs_data = cbs_res.json()
    assert cbs_data["success"] is True
    assert "transaction_ref" in cbs_data

    # Mode 2: Branch Token & Manager Verification Desk
    token_res = client.post("/api/bank-gateway/generate-token", json={
        "fdr_id": fdr["id"],
        "branch_email": "manager.branch@sbi.co.in"
    })
    assert token_res.status_code == 200
    token_data = token_res.json()
    token_str = token_data["token"]

    submit_res = client.post(f"/api/bank-gateway/desk/{token_str}/submit", json={
        "manager_name": "Shri Amit Kapoor",
        "manager_emp_id": "SBI-BM-102",
        "is_approved": True,
        "notes": "Lien endorsed in favor of Member Secretary AICTE"
    })
    assert submit_res.status_code == 200

    # Mode 3: NeSL & DigiLocker
    nesl_res = client.post(f"/api/bank-gateway/nesl-verify/{fdr['id']}")
    assert nesl_res.status_code == 200
    assert nesl_res.json()["is_valid"] is True

def test_maturity_engine_sweep():
    sweep_res = client.post("/api/maturity/run-sweep", json={
        "simulated_date": "2026-10-24"
    })
    assert sweep_res.status_code == 200
    data = sweep_res.json()
    assert data["total_scanned"] >= 7

def test_maker_checker_authorizer_release_workflow():
    # Find Kolkata FDR which has lock-in fulfilled
    res = client.get("/api/fdrs?search=FDR-2014-SBI-10928")
    fdr = res.json()["fdrs"][0]

    reqs_res = client.get("/api/release/requests")
    reqs = [r for r in reqs_res.json()["requests"] if r["fdr_id"] == fdr["id"]]
    assert len(reqs) > 0
    req = reqs[0]

    # Tier 1: Scrutiny Officer (Maker)
    maker_res = client.post(f"/api/release/{req['id']}/scrutiny", json={
        "officer_name": "Smt. Sunita Rao",
        "is_approved": True,
        "comments": "10 Academic years lock-in satisfied."
    })
    assert maker_res.status_code == 200

    # Tier 2: Regional Officer (Checker)
    ro_res = client.post(f"/api/release/{req['id']}/ro-review", json={
        "ro_name": "Dr. R. K. Verma",
        "is_recommended": True,
        "comments": "Recommended for discharge."
    })
    assert ro_res.status_code == 200

    # Tier 3: Bureau Chief (Authorizer DSC)
    auth_res = client.post(f"/api/release/{req['id']}/authorize", json={
        "authorizer_name": "Prof. Rajive Kumar",
        "aadhaar_esign_simulated": True,
        "pin": "123456"
    })
    assert auth_res.status_code == 200
    auth_data = auth_res.json()
    assert auth_data["final_status"] == "RELEASED_DISCHARGED"
    assert "digital_signature_hash" in auth_data

    # Download NOC PDF
    pdf_res = client.get(f"/api/release/{req['id']}/noc-download")
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert len(pdf_res.content) > 1000

def test_cryptographic_audit_ledger_and_tamper_attack_detection():
    # 1. Clean verification
    db = SessionLocal()
    try:
        clean_check = verify_audit_integrity(db)
        assert clean_check["is_valid"] is True
        assert clean_check["total_records"] > 0

        # 2. Simulate malicious out-of-band database tampering
        first_record_id = 1
        tamper_res = simulate_tamper(db, record_id=first_record_id, forged_amount=99999999.0)
        assert tamper_res["success"] is True

        # 3. Merkle verification must catch the tamper attempt
        tampered_check = verify_audit_integrity(db)
        assert tampered_check["is_valid"] is False
        assert tampered_check["tampered_index"] == first_record_id
    finally:
        db.close()
