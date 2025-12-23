from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from api.database.db import get_db
from api.schemas.company import GetCompanyOut
from api.cruds.company import get_companies
from api.utils.auth import get_current_user
from api.models.users import Users


router = APIRouter()


# GET
@router.get("/api/companies", tags=["companies"], response_model=List[GetCompanyOut])
def get_companies_endpoint(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return get_companies(db, current_user)


# # POST
# @router.post("/api/companies", tags=["companies"], response_model=PostCompanyOut)
# def create_companies_endpoint(
#     companies_in: PostCompanyIn,
#     db: Session = Depends(get_db),
#     current_user: Users = Depends(get_current_user)
# ):
#     return create_company(db, companies_in, current_user)

# # PUT
# @router.put("/api/companies/{company_id}", tags=["companies"], response_model=PutCompanyOut)
# def update_companies_endpoint(
#     company_id: int,
#     companies_in: PutCompanyIn,
#     db: Session = Depends(get_db),
#     current_user: Users = Depends(get_current_user)
# ):
#     return update_company(db, company_id, companies_in, current_user)


# # DELETE
# @router.delete("/api/companies/{company_id}", tags=["companies"], response_model=DeleteCompanyOut)
# def delete_companies_endpoint(
#     company_id: int,
#     db: Session = Depends(get_db),
#     current_user: Users = Depends(get_current_user)
# ):
#     return delete_company(db, company_id, current_user)
