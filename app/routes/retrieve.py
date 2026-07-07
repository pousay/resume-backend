from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schema import Contact

router = APIRouter()


@router.get("/contacts")
async def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()


@router.get("/contacts/{contact_id}")
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    return db.get(Contact, contact_id)
