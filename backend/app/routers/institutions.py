from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.database import get_db
from backend.app.models import Institution, FDRInstrument

router = APIRouter(prefix="/api/institutions", tags=["Institutions"])

@router.get("")
def list_institutions(
    state: str = Query(None),
    zone: str = Query(None),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Institution)
    if state:
        query = query.filter(Institution.state == state)
    if zone:
        query = query.filter(Institution.regional_office.contains(zone))
    if search:
        s = f"%{search}%"
        query = query.filter((Institution.name.ilike(s)) | (Institution.pid.ilike(s)))

    institutions = query.all()
    results = []
    for inst in institutions:
        fdr_count = db.query(FDRInstrument).filter(FDRInstrument.institution_id == inst.id).count()
        total_collateral = db.query(func.sum(FDRInstrument.deposit_amount)).filter(FDRInstrument.institution_id == inst.id).scalar() or 0.0

        results.append({
            "id": inst.id,
            "pid": inst.pid,
            "name": inst.name,
            "type": inst.type,
            "state": inst.state,
            "regional_office": inst.regional_office,
            "head_name": inst.head_of_inst_name,
            "head_email": inst.head_of_inst_email,
            "head_phone": inst.head_of_inst_phone,
            "fdr_count": fdr_count,
            "total_collateral": total_collateral,
            "created_at": inst.created_at
        })
    return {"institutions": results, "total": len(results)}

@router.get("/{inst_id}")
def get_institution_details(inst_id: str, db: Session = Depends(get_db)):
    inst = db.query(Institution).filter((Institution.id == inst_id) | (Institution.pid == inst_id)).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Institution not found")

    fdrs = db.query(FDRInstrument).filter(FDRInstrument.institution_id == inst.id).all()
    total_collateral = sum(f.deposit_amount for f in fdrs)

    return {
        "institution": {
            "id": inst.id,
            "pid": inst.pid,
            "name": inst.name,
            "type": inst.type,
            "state": inst.state,
            "regional_office": inst.regional_office,
            "head_name": inst.head_of_inst_name,
            "head_email": inst.head_of_inst_email,
            "head_phone": inst.head_of_inst_phone,
            "total_collateral": total_collateral,
            "fdr_instruments": [
                {
                    "id": f.id,
                    "fdr_number": f.fdr_number,
                    "bank_name": f.bank_name,
                    "deposit_amount": f.deposit_amount,
                    "maturity_date": f.maturity_date,
                    "status": f.status,
                    "verification_level": f.verification_level,
                    "is_discrepant": f.is_discrepant
                } for f in fdrs
            ]
        }
    }
