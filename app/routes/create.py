from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schema import Contact
from app.models import ContactCreate

router = APIRouter()


@router.post("/contact", status_code=201)
async def create_contact(
    data: ContactCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    contact = Contact(
        name=data.name,
        message=data.message,
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent", ""),
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return {
        "message": "Contact created successfully",
        "id": contact.id,
    }
