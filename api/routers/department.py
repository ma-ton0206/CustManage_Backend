from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from api.database.db import get_db
from api.schemas.department import GetDepartmentOut, PutDepartmentIn, PutDepartmentsOut, DeleteDepartmentOut
from api.cruds.department import get_departments, update_department, delete_departments, create_departments, update_department_name
from api.utils.auth import get_current_user
from api.models.users import Users
from api.schemas.department import DeleteDepartmentIn, PostDepartmentIn, PostDepartmentOut, UpdateDepartmentNameIn, UpdateDepartmentNameOut

router = APIRouter()


# GET
@router.get("/api/departments/{client_id}", tags=["departments"], response_model=List[GetDepartmentOut])
def get_departments_endpoint(
    client_id: int, 
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return get_departments(db, client_id, current_user)


# PUT
@router.put("/api/departments/{client_id}", tags=["departments"], response_model=PutDepartmentsOut)
def update_departments_endpoint(
    client_id: int,
    departments_in: PutDepartmentIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return update_department(db, client_id, departments_in, current_user)

#delete
@router.delete("/api/departments/{client_id}/{department_id}", tags=["departments"], response_model=DeleteDepartmentOut)
def delete_departments_endpoint(
    client_id: int,
    department_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return delete_departments(db, client_id, department_id, current_user)


#POST
@router.post("/api/departments/{client_id}", tags=["departments"], response_model=PostDepartmentOut)
def create_departments_endpoint(
    client_id: int,
    departments_in: PostDepartmentIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return create_departments(db, client_id, departments_in, current_user)

@router.patch("/api/departments/{client_id}/{department_id}", tags=["departments"], response_model=UpdateDepartmentNameOut)
def update_department_name_endpoint(
    client_id: int,
    department_id: int,
    department_name_in: UpdateDepartmentNameIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return update_department_name(db, client_id, department_id, department_name_in, current_user)