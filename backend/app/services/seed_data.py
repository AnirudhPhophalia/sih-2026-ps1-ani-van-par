import os
from datetime import datetime, date, timedelta, timezone
from sqlalchemy.orm import Session
from backend.app.models import (
    Institution, FDRInstrument, FDRDocument, FDRVerification, FDRAlert, FDRReleaseRequest
)
from backend.app.services.document_generator import generate_fdr_sample_image
from backend.app.services.ocr_service import compute_file_sha256
from backend.app.services.audit_service import log_audit_event

SEED_INSTITUTIONS = [
    {
        "pid": "1-3324567891",
        "name": "Delhi Institute of Engineering & Technology",
        "type": "PRIVATE_UNAIDED",
        "state": "Delhi",
        "regional_office": "North-West Regional Office (NWRO)",
        "head_name": "Dr. R. K. Saxena",
        "head_email": "director@dietdelhi.ac.in",
        "head_phone": "+91-9811223344"
    },
    {
        "pid": "1-2244668800",
        "name": "Maharashtra Institute of Technology & Research",
        "type": "GOVT_AIDED",
        "state": "Maharashtra",
        "regional_office": "Western Regional Office (WRO)",
        "head_name": "Prof. S. N. Deshmukh",
        "head_email": "principal@mitr-pune.edu.in",
        "head_phone": "+91-9822334455"
    },
    {
        "pid": "1-4455667788",
        "name": "Bangalore Academy of Applied Sciences",
        "type": "PRIVATE_UNAIDED",
        "state": "Karnataka",
        "regional_office": "South-Western Regional Office (SWRO)",
        "head_name": "Dr. Meenakshi Sundaram",
        "head_email": "head@baas.edu.in",
        "head_phone": "+91-9844556677"
    },
    {
        "pid": "1-5566778899",
        "name": "Chennai College of Technology & Innovation",
        "type": "PRIVATE_UNAIDED",
        "state": "Tamil Nadu",
        "regional_office": "Southern Regional Office (SRO)",
        "head_name": "Dr. V. Ramanathan",
        "head_email": "director@cctechennai.org",
        "head_phone": "+91-9444112233"
    },
    {
        "pid": "1-7788990011",
        "name": "Hyderabad Technological Institute",
        "type": "PRIVATE_UNAIDED",
        "state": "Telangana",
        "regional_office": "South-Central Regional Office (SCRO)",
        "head_name": "Dr. K. Srinivas Rao",
        "head_email": "principal@hti-hyd.ac.in",
        "head_phone": "+91-9849012345"
    },
    {
        "pid": "1-9988776655",
        "name": "Kolkata Engineering & Management College",
        "type": "PRIVATE_UNAIDED",
        "state": "West Bengal",
        "regional_office": "Eastern Regional Office (ERO)",
        "head_name": "Prof. Anirban Mukherjee",
        "head_email": "director@kemc-kolkata.edu.in",
        "head_phone": "+91-9830112233"
    },
    {
        "pid": "1-1122334455",
        "name": "Lucknow Institute of Pharmaceutical Sciences",
        "type": "PRIVATE_UNAIDED",
        "state": "Uttar Pradesh",
        "regional_office": "Northern Regional Office (NRO)",
        "head_name": "Dr. Akhilesh Verma",
        "head_email": "director@lips-lucknow.edu.in",
        "head_phone": "+91-9415012345"
    },
    {
        "pid": "1-6677889900",
        "name": "Bhopal Institute of Technology & Science",
        "type": "PRIVATE_UNAIDED",
        "state": "Madhya Pradesh",
        "regional_office": "Central Regional Office (CRO)",
        "head_name": "Dr. Sangeeta Chouhan",
        "head_email": "principal@bits-bhopal.ac.in",
        "head_phone": "+91-9826012345"
    }
]

def seed_database_if_empty(db: Session):
    inst_count = db.query(Institution).count()
    if inst_count > 0:
        return {"message": "Database already seeded."}

    print("Seeding initial AICTE institutions, FDR instruments, and cryptographic records...")
    today = date.today()

    inst_map = {}
    for data in SEED_INSTITUTIONS:
        inst = Institution(
            pid=data["pid"],
            name=data["name"],
            type=data["type"],
            state=data["state"],
            regional_office=data["regional_office"],
            head_of_inst_name=data["head_name"],
            head_of_inst_email=data["head_email"],
            head_of_inst_phone=data["head_phone"],
            is_active=True
        )
        db.add(inst)
        db.flush()
        inst_map[data["name"]] = inst

        log_audit_event(
            db=db,
            entity_name="institutions",
            entity_id=inst.id,
            action_type="REGISTER_INSTITUTION",
            actor_id="AICTE_REGULATION_SYSTEM",
            actor_role="SYSTEM_ADMIN",
            new_state={"pid": inst.pid, "name": inst.name}
        )

    # Instrument 1: Verified Active (Delhi)
    inst1 = inst_map["Delhi Institute of Engineering & Technology"]
    fdr1_num = "FDR-2022-SBI-49102"
    fdr1_img = f"fdr_{fdr1_num}.png"
    img_path1 = generate_fdr_sample_image(
        filename=fdr1_img,
        fdr_number=fdr1_num,
        bank_name="State Bank of India",
        branch_name="Parliament Street Branch, New Delhi",
        ifsc_code="SBIN0001001",
        institution_name=inst1.name,
        deposit_amount=5000000.00,
        issue_date="2022-06-15",
        maturity_date="2030-06-15",
        is_lien_marked=True
    )
    fdr1 = FDRInstrument(
        institution_id=inst1.id,
        fdr_number=fdr1_num,
        account_number="30987654321",
        bank_name="State Bank of India",
        branch_name="Parliament Street Branch, New Delhi",
        ifsc_code="SBIN0001001",
        deposit_amount=5000000.00,
        rate_of_interest=7.10,
        issue_date="2022-06-15",
        maturity_date="2030-06-15",
        statutory_lock_in_years=8,
        statutory_lock_in_end_date="2030-06-15",
        lien_marked=True,
        lien_in_favor_of="Member Secretary, AICTE, New Delhi",
        lien_reference_number="AICTE/DEL/FDR/2022/49102",
        status="VERIFIED_ACTIVE",
        verification_level="BANK_API_VERIFIED",
        is_discrepant=False
    )
    db.add(fdr1)
    db.flush()

    doc1 = FDRDocument(
        fdr_id=fdr1.id,
        document_type="FDR_CERTIFICATE",
        file_name=fdr1_img,
        storage_path=img_path1,
        mime_type="image/png",
        file_size_bytes=os.path.getsize(img_path1),
        sha256_hash=compute_file_sha256(img_path1),
        ocr_processed=True,
        ocr_confidence_score=0.98,
        ocr_extracted_payload={"status": "MATCHED"}
    )
    db.add(doc1)

    log_audit_event(
        db=db,
        entity_name="fdr_instruments",
        entity_id=fdr1.id,
        action_type="SUBMIT_AND_VERIFY_FDR",
        actor_id=inst1.head_of_inst_email,
        actor_role="INSTITUTION_ADMIN",
        new_state={"fdr_number": fdr1.fdr_number, "amount": fdr1.deposit_amount}
    )

    # Instrument 2: Under Scrutiny (Maharashtra)
    inst2 = inst_map["Maharashtra Institute of Technology & Research"]
    fdr2_num = "FDR-2024-PNB-61094"
    fdr2_img = f"fdr_{fdr2_num}.png"
    img_path2 = generate_fdr_sample_image(
        filename=fdr2_img,
        fdr_number=fdr2_num,
        bank_name="Punjab National Bank",
        branch_name="Shivaji Nagar, Pune",
        ifsc_code="PUNB0123400",
        institution_name=inst2.name,
        deposit_amount=3500000.00,
        issue_date="2024-03-10",
        maturity_date="2032-03-10",
        is_lien_marked=True
    )
    fdr2 = FDRInstrument(
        institution_id=inst2.id,
        fdr_number=fdr2_num,
        account_number="41230009871",
        bank_name="Punjab National Bank",
        branch_name="Shivaji Nagar, Pune",
        ifsc_code="PUNB0123400",
        deposit_amount=3500000.00,
        rate_of_interest=7.25,
        issue_date="2024-03-10",
        maturity_date="2032-03-10",
        statutory_lock_in_years=8,
        statutory_lock_in_end_date="2032-03-10",
        lien_marked=True,
        lien_in_favor_of="Member Secretary, AICTE, New Delhi",
        lien_reference_number="AICTE/WRO/FDR/2024/61094",
        status="UNDER_SCRUTINY",
        verification_level="SELF_DECLARED",
        is_discrepant=False
    )
    db.add(fdr2)
    db.flush()

    doc2 = FDRDocument(
        fdr_id=fdr2.id,
        document_type="FDR_CERTIFICATE",
        file_name=fdr2_img,
        storage_path=img_path2,
        mime_type="image/png",
        file_size_bytes=os.path.getsize(img_path2),
        sha256_hash=compute_file_sha256(img_path2),
        ocr_processed=False
    )
    db.add(doc2)

    # Instrument 3: Discrepancy Flagged (Amount mismatch demo)
    inst3 = inst_map["Bangalore Academy of Applied Sciences"]
    fdr3_num = "FDR-2023-CANARA-77215"
    fdr3_img = f"fdr_{fdr3_num}.png"
    # Scanned image has 4,000,000 but college entered 5,000,000!
    img_path3 = generate_fdr_sample_image(
        filename=fdr3_img,
        fdr_number=fdr3_num,
        bank_name="Canara Bank",
        branch_name="MG Road, Bangalore",
        ifsc_code="CNRB0000123",
        institution_name=inst3.name,
        deposit_amount=4000000.00, # Actual on certificate
        issue_date="2023-01-20",
        maturity_date="2031-01-20",
        is_lien_marked=True
    )
    fdr3 = FDRInstrument(
        institution_id=inst3.id,
        fdr_number=fdr3_num,
        account_number="08812345678",
        bank_name="Canara Bank",
        branch_name="MG Road, Bangalore",
        ifsc_code="CNRB0000123",
        deposit_amount=5000000.00, # Declared higher!
        rate_of_interest=7.00,
        issue_date="2023-01-20",
        maturity_date="2031-01-20",
        statutory_lock_in_years=8,
        statutory_lock_in_end_date="2031-01-20",
        lien_marked=True,
        status="DISCREPANCY_FLAGGED",
        verification_level="OCR_EXTRACTED",
        is_discrepant=True,
        discrepancy_notes="Deposit Amount mismatch: College declared ₹50,00,000.00, but OCR extracted certificate specifies ₹40,00,000.00. (Discrepancy Score: 0.090 > 0.05)"
    )
    db.add(fdr3)
    db.flush()

    doc3 = FDRDocument(
        fdr_id=fdr3.id,
        document_type="FDR_CERTIFICATE",
        file_name=fdr3_img,
        storage_path=img_path3,
        mime_type="image/png",
        file_size_bytes=os.path.getsize(img_path3),
        sha256_hash=compute_file_sha256(img_path3),
        ocr_processed=True,
        ocr_confidence_score=0.94,
        ocr_extracted_payload={
            "fdr_number": fdr3_num,
            "deposit_amount": 4000000.00,
            "maturity_date": "2031-01-20"
        }
    )
    db.add(doc3)

    # Instrument 4: Approaching Maturity (T-45 days)
    inst4 = inst_map["Chennai College of Technology & Innovation"]
    mat_date_4 = (today + timedelta(days=45)).strftime("%Y-%m-%d")
    fdr4_num = "FDR-2018-HDFC-99312"
    fdr4_img = f"fdr_{fdr4_num}.png"
    img_path4 = generate_fdr_sample_image(
        filename=fdr4_img,
        fdr_number=fdr4_num,
        bank_name="HDFC Bank Ltd.",
        branch_name="Anna Salai, Chennai",
        ifsc_code="HDFC0000240",
        institution_name=inst4.name,
        deposit_amount=4500000.00,
        issue_date="2018-12-10",
        maturity_date=mat_date_4,
        is_lien_marked=True
    )
    fdr4 = FDRInstrument(
        institution_id=inst4.id,
        fdr_number=fdr4_num,
        account_number="50100234567890",
        bank_name="HDFC Bank Ltd.",
        branch_name="Anna Salai, Chennai",
        ifsc_code="HDFC0000240",
        deposit_amount=4500000.00,
        rate_of_interest=7.40,
        issue_date="2018-12-10",
        maturity_date=mat_date_4,
        statutory_lock_in_years=8,
        statutory_lock_in_end_date=(today + timedelta(days=45)).strftime("%Y-%m-%d"),
        lien_marked=True,
        status="MATURITY_APPROACHING",
        verification_level="BANK_API_VERIFIED",
        is_discrepant=False
    )
    db.add(fdr4)
    db.flush()

    doc4 = FDRDocument(
        fdr_id=fdr4.id,
        document_type="FDR_CERTIFICATE",
        file_name=fdr4_img,
        storage_path=img_path4,
        mime_type="image/png",
        file_size_bytes=os.path.getsize(img_path4),
        sha256_hash=compute_file_sha256(img_path4),
        ocr_processed=True,
        ocr_confidence_score=0.97
    )
    db.add(doc4)

    alert4 = FDRAlert(
        fdr_id=fdr4.id,
        institution_id=inst4.id,
        severity="WARNING",
        alert_code="EXPIRY_90_DAYS",
        message=f"Statutory Notice: FDR #{fdr4_num} expires in 45 days ({mat_date_4}). Prepare renewal or submit release request.",
        channels_sent=["PORTAL", "EMAIL"],
        is_read=False,
        is_resolved=False,
        escalation_tier=1
    )
    db.add(alert4)

    # Instrument 5: Matured Overdue (Hyderabad)
    inst5 = inst_map["Hyderabad Technological Institute"]
    mat_date_5 = (today - timedelta(days=22)).strftime("%Y-%m-%d")
    fdr5_num = "FDR-2016-BOB-33418"
    fdr5_img = f"fdr_{fdr5_num}.png"
    img_path5 = generate_fdr_sample_image(
        filename=fdr5_img,
        fdr_number=fdr5_num,
        bank_name="Bank of Baroda",
        branch_name="Banjara Hills, Hyderabad",
        ifsc_code="BARB0BANJAR",
        institution_name=inst5.name,
        deposit_amount=6000000.00,
        issue_date="2016-10-01",
        maturity_date=mat_date_5,
        is_lien_marked=True
    )
    fdr5 = FDRInstrument(
        institution_id=inst5.id,
        fdr_number=fdr5_num,
        account_number="2120010004567",
        bank_name="Bank of Baroda",
        branch_name="Banjara Hills, Hyderabad",
        ifsc_code="BARB0BANJAR",
        deposit_amount=6000000.00,
        rate_of_interest=7.50,
        issue_date="2016-10-01",
        maturity_date=mat_date_5,
        statutory_lock_in_years=8,
        statutory_lock_in_end_date="2024-10-01",
        lien_marked=True,
        status="MATURED_PENDING_RENEWAL",
        verification_level="BANK_API_VERIFIED",
        is_discrepant=False
    )
    db.add(fdr5)
    db.flush()

    doc5 = FDRDocument(
        fdr_id=fdr5.id,
        document_type="FDR_CERTIFICATE",
        file_name=fdr5_img,
        storage_path=img_path5,
        mime_type="image/png",
        file_size_bytes=os.path.getsize(img_path5),
        sha256_hash=compute_file_sha256(img_path5),
        ocr_processed=True,
        ocr_confidence_score=0.96
    )
    db.add(doc5)

    alert5 = FDRAlert(
        fdr_id=fdr5.id,
        institution_id=inst5.id,
        severity="CRITICAL",
        alert_code="OVERDUE_RENEWAL",
        message=f"CRITICAL ESCALATION: FDR #{fdr5_num} is 22 days past maturity! Escalated to Regional Officer (SCRO).",
        channels_sent=["PORTAL", "EMAIL", "SMS"],
        is_read=False,
        is_resolved=False,
        escalation_tier=2
    )
    db.add(alert5)

    # Instrument 6: Release Requested (Lock-in fulfilled, 10 years completed)
    inst6 = inst_map["Kolkata Engineering & Management College"]
    fdr6_num = "FDR-2014-SBI-10928"
    fdr6_img = f"fdr_{fdr6_num}.png"
    img_path6 = generate_fdr_sample_image(
        filename=fdr6_img,
        fdr_number=fdr6_num,
        bank_name="State Bank of India",
        branch_name="Park Street Branch, Kolkata",
        ifsc_code="SBIN0000012",
        institution_name=inst6.name,
        deposit_amount=5000000.00,
        issue_date="2014-08-15",
        maturity_date="2024-08-15",
        is_lien_marked=True
    )
    fdr6 = FDRInstrument(
        institution_id=inst6.id,
        fdr_number=fdr6_num,
        account_number="30112233445",
        bank_name="State Bank of India",
        branch_name="Park Street Branch, Kolkata",
        ifsc_code="SBIN0000012",
        deposit_amount=5000000.00,
        rate_of_interest=7.50,
        issue_date="2014-08-15",
        maturity_date="2024-08-15",
        statutory_lock_in_years=10,
        statutory_lock_in_end_date="2024-08-15",
        lien_marked=True,
        status="RELEASE_REQUESTED",
        verification_level="BANK_API_VERIFIED",
        is_discrepant=False
    )
    db.add(fdr6)
    db.flush()

    doc6 = FDRDocument(
        fdr_id=fdr6.id,
        document_type="FDR_CERTIFICATE",
        file_name=fdr6_img,
        storage_path=img_path6,
        mime_type="image/png",
        file_size_bytes=os.path.getsize(img_path6),
        sha256_hash=compute_file_sha256(img_path6),
        ocr_processed=True,
        ocr_confidence_score=0.99
    )
    db.add(doc6)

    # Add a pending release request
    rel_req = FDRReleaseRequest(
        fdr_id=fdr6.id,
        institution_id=inst6.id,
        requested_amount=5000000.00,
        reason_for_release="Completed 10 academic cycles with full regulatory compliance and zero pending fee litigation or student complaints. Requesting lien discharge.",
        scrutiny_status="PENDING",
        ro_recommendation="PENDING",
        final_authorization="PENDING"
    )
    db.add(rel_req)

    # Instrument 7: Renewed with predecessor lineage (Lucknow)
    inst7 = inst_map["Lucknow Institute of Pharmaceutical Sciences"]
    fdr7_num = "FDR-2024-PNB-88210"
    fdr7_img = f"fdr_{fdr7_num}.png"
    img_path7 = generate_fdr_sample_image(
        filename=fdr7_img,
        fdr_number=fdr7_num,
        bank_name="Punjab National Bank",
        branch_name="Hazratganj, Lucknow",
        ifsc_code="PUNB0021300",
        institution_name=inst7.name,
        deposit_amount=3000000.00,
        issue_date="2024-05-01",
        maturity_date="2032-05-01",
        is_lien_marked=True
    )
    fdr7 = FDRInstrument(
        institution_id=inst7.id,
        fdr_number=fdr7_num,
        account_number="190020110022",
        bank_name="Punjab National Bank",
        branch_name="Hazratganj, Lucknow",
        ifsc_code="PUNB0021300",
        deposit_amount=3000000.00,
        rate_of_interest=7.20,
        issue_date="2024-05-01",
        maturity_date="2032-05-01",
        statutory_lock_in_years=8,
        statutory_lock_in_end_date="2032-05-01",
        lien_marked=True,
        status="VERIFIED_ACTIVE",
        verification_level="BANK_API_VERIFIED",
        is_discrepant=False
    )
    db.add(fdr7)
    db.flush()

    doc7 = FDRDocument(
        fdr_id=fdr7.id,
        document_type="FDR_CERTIFICATE",
        file_name=fdr7_img,
        storage_path=img_path7,
        mime_type="image/png",
        file_size_bytes=os.path.getsize(img_path7),
        sha256_hash=compute_file_sha256(img_path7),
        ocr_processed=True,
        ocr_confidence_score=0.98
    )
    db.add(doc7)

    db.commit()
    print("Database seeding completed successfully!")
    return {"message": "Database successfully seeded with 8 institutions and 7 comprehensive FDR lifecycle records."}
