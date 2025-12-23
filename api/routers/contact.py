from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from api.database.db import get_db
from api.schemas.contact import GetContactOut, PutContactIn, PutContactsOut
from api.cruds.contact import get_contacts, update_contact, delete_contact, create_contact
from api.utils.auth import get_current_user
from api.models.users import Users
from api.schemas.contact import DeleteContactIn, DeleteContactOut, PostContactIn, PostContactOut

router = APIRouter()


# GET
@router.get("/api/contacts/{client_id}/{department_id}", tags=["contacts"], response_model=List[GetContactOut])
def get_contacts_endpoint(
    client_id: int,
    department_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return get_contacts(db, client_id, department_id, current_user)


# PUT
@router.put("/api/contacts/{client_id}/{department_id}", tags=["contacts"], response_model=PutContactsOut)
def update_contacts_endpoint(
    client_id: int,
    department_id: int,
    contacts_in: PutContactIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return update_contact(db, client_id, department_id, contacts_in, current_user)


# DELETE
@router.delete("/api/contacts/{client_id}/{department_id}/{contact_id}", tags=["contacts"], response_model=DeleteContactOut)
def delete_contact_endpoint(
    client_id: int,
    department_id: int,
    delete_contact_in: DeleteContactIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return delete_contact(db, client_id, department_id, delete_contact_in.contact_id, current_user)

#POST
@router.post("/api/contacts/{client_id}/{department_id}", tags=["contacts"], response_model=PostContactOut)
def create_contact_endpoint(
    client_id: int,
    department_id: int,
    contacts_in: PostContactIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return create_contact(db, client_id, department_id, contacts_in, current_user)