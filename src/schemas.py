from typing import Optional
from pydantic import BaseModel
from datetime import date

class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_info: Optional[str] = None

class ContactCreate(ContactModel):
    pass

class ContactUpdate(ContactModel):
    pass

class ContactResponse(ContactModel):
    id: int

    class Config:
        from_attributes = True