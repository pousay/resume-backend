from fastapi import APIRouter, BackgroundTasks, Depends, Request
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schema import Contact
from app.models import ContactCreate
from app.dependencies.services import get_notifier
from app.services import NotificationService

router = APIRouter()


@router.post("/contact", status_code=201)
async def create_contact(
    data: ContactCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    notifier: NotificationService = Depends(get_notifier),
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

    background_tasks.add_task(
        notifier.notify_new_contact,
        contact,
    )

    return {
        "message": "Contact created successfully",
        "id": contact.id,
    }
