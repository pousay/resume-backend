from pydantic import BaseModel, Field


class ContactForm(BaseModel):
    name: str = Field(..., title="Name", description="The name of the contact")
    message: str = Field(
        ..., title="Message", description="The message from the contact"
    )


class ContactCreate(ContactForm):
    pass
