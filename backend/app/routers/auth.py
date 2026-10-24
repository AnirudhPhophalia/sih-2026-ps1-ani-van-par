from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/auth", tags=["Authentication & Personas"])

PERSONAS = {
    "INSTITUTION_ADMIN": {
        "id": "inst_admin_delhi",
        "name": "Dr. R. K. Saxena",
        "role": "INSTITUTION_ADMIN",
        "designation": "Director / Principal",
        "institution_pid": "1-3324567891",
        "institution_name": "Delhi Institute of Engineering & Technology",
        "email": "director@dietdelhi.ac.in"
    },
    "SCRUTINY_OFFICER": {
        "id": "aicte_scrutiny_01",
        "name": "Smt. Sunita Rao",
        "role": "SCRUTINY_OFFICER",
        "designation": "Regulation Bureau Dealing Officer",
        "email": "scrutiny.regulation@aicte-india.org"
    },
    "REGIONAL_OFFICER": {
        "id": "aicte_ro_nwro",
        "name": "Dr. R. K. Verma",
        "role": "REGIONAL_OFFICER",
        "designation": "Regional Officer (NWRO / Northern Region)",
        "email": "ro.northwest@aicte-india.org"
    },
    "BUREAU_CHIEF": {
        "id": "aicte_member_secretary",
        "name": "Prof. Rajive Kumar",
        "role": "BUREAU_CHIEF",
        "designation": "Member Secretary / Competent Authority",
        "email": "member.secretary@aicte-india.org"
    },
    "BANK_AUDITOR": {
        "id": "sbi_bm_delhi",
        "name": "Shri Amit Kapoor",
        "role": "BANK_AUDITOR",
        "designation": "Chief Manager & Branch Head",
        "bank_name": "State Bank of India",
        "branch": "Parliament Street Branch",
        "email": "bm.01001@sbi.co.in"
    },
    "CISO_AUDITOR": {
        "id": "aicte_ciso",
        "name": "Dr. Arvind Swaminathan",
        "role": "CISO_AUDITOR",
        "designation": "Chief Information Security Officer & Vigilance Lead",
        "email": "ciso.audit@aicte-india.org"
    }
}

class SwitchRoleRequest(BaseModel):
    role: str

@router.get("/personas")
def get_available_personas():
    return {"personas": list(PERSONAS.values())}

@router.get("/current-user/{role}")
def get_user_by_role(role: str):
    user = PERSONAS.get(role.upper())
    if not user:
        raise HTTPException(status_code=404, detail="Persona role not found")
    return {"user": user}
