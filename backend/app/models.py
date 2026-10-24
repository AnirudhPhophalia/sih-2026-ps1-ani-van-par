import uuid
import datetime
import json
from sqlalchemy import (
    Column, String, Boolean, Integer, Float, Date, DateTime, Text, JSON, ForeignKey
)
from sqlalchemy.orm import relationship
from backend.app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

def get_current_time():
    return datetime.datetime.now(datetime.timezone.utc)

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    pid = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False, default="PRIVATE_UNAIDED")
    state = Column(String(100), nullable=False)
    regional_office = Column(String(100), nullable=False)
    head_of_inst_name = Column(String(150), nullable=False)
    head_of_inst_email = Column(String(150), nullable=False)
    head_of_inst_phone = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=get_current_time)
    updated_at = Column(DateTime(timezone=True), default=get_current_time, onupdate=get_current_time)

    fdrs = relationship("FDRInstrument", back_populates="institution", cascade="all, delete-orphan")
    release_requests = relationship("FDRReleaseRequest", back_populates="institution")
    alerts = relationship("FDRAlert", back_populates="institution")


class FDRInstrument(Base):
    __tablename__ = "fdr_instruments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    institution_id = Column(String(36), ForeignKey("institutions.id", ondelete="RESTRICT"), nullable=False, index=True)
    fdr_number = Column(String(100), nullable=False, index=True)
    account_number = Column(String(100), nullable=False)
    instrument_type = Column(String(50), default="FDR_JOINT")

    # Financial Details
    bank_name = Column(String(150), nullable=False)
    branch_name = Column(String(150), nullable=False)
    ifsc_code = Column(String(20), nullable=False)
    deposit_amount = Column(Float, nullable=False)
    rate_of_interest = Column(Float, default=7.25)

    # Date Matrix
    issue_date = Column(String(20), nullable=False) # YYYY-MM-DD
    maturity_date = Column(String(20), nullable=False, index=True) # YYYY-MM-DD
    statutory_lock_in_years = Column(Integer, default=8)
    statutory_lock_in_end_date = Column(String(20), nullable=False)

    # Lien Endorsement
    lien_marked = Column(Boolean, default=True)
    lien_in_favor_of = Column(String(255), default="Member Secretary, AICTE, New Delhi")
    lien_reference_number = Column(String(100))

    # Lifecycle Status
    status = Column(String(50), default="SUBMITTED", index=True)
    verification_level = Column(String(50), default="SELF_DECLARED")
    is_discrepant = Column(Boolean, default=False)
    discrepancy_notes = Column(Text, nullable=True)

    # Succession lineage for renewals
    predecessor_fdr_id = Column(String(36), ForeignKey("fdr_instruments.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), default=get_current_time)
    updated_at = Column(DateTime(timezone=True), default=get_current_time, onupdate=get_current_time)

    # Relationships
    institution = relationship("Institution", back_populates="fdrs")
    documents = relationship("FDRDocument", back_populates="fdr", cascade="all, delete-orphan")
    verifications = relationship("FDRVerification", back_populates="fdr", cascade="all, delete-orphan")
    release_requests = relationship("FDRReleaseRequest", back_populates="fdr")
    alerts = relationship("FDRAlert", back_populates="fdr", cascade="all, delete-orphan")


class FDRDocument(Base):
    __tablename__ = "fdr_documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    fdr_id = Column(String(36), ForeignKey("fdr_instruments.id", ondelete="CASCADE"), nullable=False, index=True)
    document_type = Column(String(50), nullable=False) # 'FDR_CERTIFICATE', 'BANK_LIEN_LETTER', 'BOARD_RESOLUTION', 'DISCHARGE_NOC'
    file_name = Column(String(255), nullable=False)
    storage_path = Column(String(500), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    sha256_hash = Column(String(64), nullable=False)

    # OCR Extraction Metadata
    ocr_processed = Column(Boolean, default=False)
    ocr_confidence_score = Column(Float, default=0.0)
    ocr_extracted_payload = Column(JSON, nullable=True)

    uploaded_by = Column(String(100), default="Institution Administrator")
    created_at = Column(DateTime(timezone=True), default=get_current_time)

    fdr = relationship("FDRInstrument", back_populates="documents")


class FDRVerification(Base):
    __tablename__ = "fdr_verifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    fdr_id = Column(String(36), ForeignKey("fdr_instruments.id", ondelete="CASCADE"), nullable=False, index=True)
    verification_source = Column(String(50), nullable=False) # 'SELF_DECLARED', 'OCR_EXTRACTED', 'BANK_API_VERIFIED', 'BANK_OFFICER_MANUAL', 'AICTE_RO_VERIFIED'
    verified_by_user = Column(String(150), nullable=True)
    bank_api_transaction_ref = Column(String(150), nullable=True)
    is_valid = Column(Boolean, default=True)
    bank_confirmed_amount = Column(Float, nullable=True)
    bank_confirmed_maturity = Column(String(20), nullable=True)
    bank_confirmed_lien = Column(Boolean, default=True)
    remarks = Column(Text, nullable=True)
    raw_response_payload = Column(JSON, nullable=True)
    verified_at = Column(DateTime(timezone=True), default=get_current_time)

    fdr = relationship("FDRInstrument", back_populates="verifications")


class FDRReleaseRequest(Base):
    __tablename__ = "fdr_release_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    fdr_id = Column(String(36), ForeignKey("fdr_instruments.id", ondelete="RESTRICT"), nullable=False, index=True)
    institution_id = Column(String(36), ForeignKey("institutions.id"), nullable=False)
    requested_amount = Column(Float, nullable=False)
    reason_for_release = Column(Text, nullable=False)

    # Workflow Stages: Maker (Scrutiny) -> Checker (RO) -> Authorizer (Bureau Chief)
    scrutiny_status = Column(String(50), default="PENDING")
    scrutiny_by = Column(String(150), nullable=True)
    scrutiny_comments = Column(Text, nullable=True)
    scrutiny_at = Column(DateTime(timezone=True), nullable=True)

    ro_recommendation = Column(String(50), default="PENDING")
    ro_by = Column(String(150), nullable=True)
    ro_comments = Column(Text, nullable=True)
    ro_at = Column(DateTime(timezone=True), nullable=True)

    final_authorization = Column(String(50), default="PENDING")
    authorized_by = Column(String(150), nullable=True)
    digital_signature_hash = Column(String(500), nullable=True)
    authorized_at = Column(DateTime(timezone=True), nullable=True)

    noc_document_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_current_time)

    fdr = relationship("FDRInstrument", back_populates="release_requests")
    institution = relationship("Institution", back_populates="release_requests")


class FDRAlert(Base):
    __tablename__ = "fdr_alerts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    fdr_id = Column(String(36), ForeignKey("fdr_instruments.id", ondelete="CASCADE"), nullable=True, index=True)
    institution_id = Column(String(36), ForeignKey("institutions.id"), nullable=True)
    severity = Column(String(20), nullable=False) # 'INFO', 'WARNING', 'CRITICAL', 'ESCALATION'
    alert_code = Column(String(50), nullable=False) # 'EXPIRY_90_DAYS', 'OVERDUE_RENEWAL', 'DISCREPANCY_FOUND'
    message = Column(Text, nullable=False)
    channels_sent = Column(JSON, default=lambda: ["SMS", "EMAIL", "PORTAL"])
    is_read = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    escalation_tier = Column(Integer, default=1) # 1: College, 2: Regional Officer, 3: Bureau Head
    created_at = Column(DateTime(timezone=True), default=get_current_time)

    fdr = relationship("FDRInstrument", back_populates="alerts")
    institution = relationship("Institution", back_populates="alerts")


class AuditLedger(Base):
    __tablename__ = "audit_ledger"

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_name = Column(String(50), nullable=False, index=True)
    entity_id = Column(String(36), nullable=False, index=True)
    action_type = Column(String(50), nullable=False) # 'INSERT', 'UPDATE', 'VERIFY', 'APPROVE_RELEASE', 'OVERRIDE'
    actor_id = Column(String(100), nullable=False)
    actor_role = Column(String(50), nullable=False)
    actor_ip = Column(String(50), default="127.0.0.1")
    previous_state = Column(JSON, nullable=True)
    new_state = Column(JSON, nullable=True)
    prev_record_hash = Column(String(64), nullable=True)
    record_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_current_time)


class BankVerificationToken(Base):
    __tablename__ = "bank_verification_tokens"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    token = Column(String(100), unique=True, nullable=False, index=True)
    fdr_id = Column(String(36), ForeignKey("fdr_instruments.id", ondelete="CASCADE"), nullable=False)
    bank_name = Column(String(150), nullable=False)
    branch_email = Column(String(150), nullable=False)
    status = Column(String(30), default="PENDING") # PENDING, CONFIRMED, REJECTED
    notes = Column(Text, nullable=True)
    verified_by_manager = Column(String(150), nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_current_time)
