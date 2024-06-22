from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import ContactResponse, ContactCreate, ContactUpdate
from src.repository import contacts


router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.post("/", response_model=ContactResponse)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return await contacts.create_contact(contact, db=db)

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return await contacts.get_contacts(skip=skip, limit=limit, db=db)

@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(first_name: Optional[str] = Query(None), last_name: Optional[str] = Query(None), email: Optional[str] = Query(None), db: Session = Depends(get_db)):
    db_contacts = await contacts.search_contact(first_name=first_name, last_name=last_name, email=email, db=db)
    if db_contacts is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contacts

@router.get("/upcoming_birthdays", response_model=List[ContactResponse])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    db_contacts = await contacts.get_upcoming_birthdays(db=db)
    if db_contacts is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = await contacts.get_contact(contact_id=contact_id, db=db)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, body: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = await contacts.update_contact(contact_id=contact_id, body=body, db=db)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = await contacts.remove_contact(contact_id=contact_id, db=db)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

