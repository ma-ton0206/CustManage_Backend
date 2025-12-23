from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from api.database.db import get_db
from api.schemas.client import GetClientOut, PostClientIn, PostClientOut, PutClientIn, PutClientOut, DeleteClientOut, GetClientDetailOut
from api.cruds.client import create_client, get_clients, update_client, delete_client, get_client_detail
from api.utils.auth import get_current_user
from api.models.users import Users


router = APIRouter()


# GET
@router.get("/api/clients", tags=["clients"], response_model=List[GetClientOut])
def get_clients_endpoint(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return get_clients(db, current_user)


@router.get("/api/clients/{client_id}", tags=["clients"], response_model=GetClientDetailOut)
def get_client_detail_endpoint(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return get_client_detail(db, client_id, current_user)

# POST


@router.post("/api/clients", tags=["clients"], response_model=PostClientOut)
def create_client_endpoint(
    client_in: PostClientIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return create_client(db, client_in, current_user)


# PUT
@router.put("/api/clients/{client_id}", tags=["clients"], response_model=PutClientOut)
def update_client_endpoint(
    client_id: int,
    client_in: PutClientIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return update_client(db, client_id, client_in, current_user)


# DELETE
@router.delete("/api/clients/{client_id}", tags=["clients"], response_model=DeleteClientOut)
def delete_client_endpoint(
    client_id: int, 
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return delete_client(db, client_id, current_user)
