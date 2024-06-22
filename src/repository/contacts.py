from typing import List, Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, extract

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate, ContactCreate, ContactResponse

async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()

async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()

async def create_contact(body: ContactCreate, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birth_date=body.birth_date,
        additional_info=body.additional_info,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db_contact.first_name = body.first_name
        db_contact.last_name = body.last_name
        db_contact.email = body.email
        db_contact.phone_number = body.phone_number
        db_contact.birth_date = body.birth_date
        db_contact.additional_info = body.additional_info
        db.commit()
        db.refresh(db_contact)
    return db_contact

async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def search_contact(first_name: Optional[str], last_name: Optional[str], email: Optional[str], db: Session) -> List[Contact]:
    query = db.query(Contact)
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()

async def get_upcoming_birthdays(db: Session) -> List[Contact]:
    today = datetime.now().date()
    seven_days_later = today + timedelta(days=7)

    upcoming_birthdays = db.query(Contact).filter(
        or_(
            and_(
                extract('month', Contact.birth_date) == today.month,
                extract('day', Contact.birth_date) >= today.day,
                extract('day', Contact.birth_date) < (today.day + 7)
            ),
            and_(
                extract('month', Contact.birth_date) == (today.replace(month=today.month % 12 + 1)).month,
                extract('day', Contact.birth_date) <= seven_days_later.day
            )
        )
    ).all()
    
    filtered_birthdays = [
        contact for contact in upcoming_birthdays
        if (datetime(today.year, contact.birth_date.month, contact.birth_date.day).date() - today).days in range(7)
        or (datetime(today.year + 1, contact.birth_date.month, contact.birth_date.day).date() - today).days in range(7)
    ]
    
    return filtered_birthdays