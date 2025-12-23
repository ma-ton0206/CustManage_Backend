from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from api.database.db import get_db
from api.schemas.purchase_details import GetPurchaseDetailsOut
from api.cruds.purchase_details import get_purchase_details
from api.utils.auth import get_current_user
from api.models.users import Users


router = APIRouter()


@router.get("/api/purchase_details", tags=["purchase_details"], response_model=List[GetPurchaseDetailsOut])
def get_purchase_details_endpoint(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return get_purchase_details(db, current_user)


# @router.put("/api/purchase_details", tags=["purchase_details"], response_model=PutPurchaseDetailsOut)
# def update_purchase_details_endpoint(
#     purchase_details_in: PutPurchaseDetailsIn,
#     db: Session = Depends(get_db),
#     current_user: Users = Depends(get_current_user)
# ):
#     return update_purchase_details(db, purchase_details_in, current_user)


# @router.post("/api/purchase_details", tags=["purchase_details"], response_model=PostPurchaseDetailsOut)
# def create_purchase_details_endpoint(
#     purchase_details_in: PostPurchaseDetailsIn, 
#     db: Session = Depends(get_db),
#     current_user: Users = Depends(get_current_user)
# ):
#     return create_purchase_details(db, purchase_details_in, current_user)


# # @router.delete("/api/purchase_details", tags=["purchase_details"], response_model=DeletePurchaseDetailsOut)
# # def delete_purchase_details_endpoint(
# #     purchase_details_in: DeletePurchaseDetailsOut,
# #     db: Session = Depends(get_db),
# #     current_user: Users = Depends(get_current_user)
# # ):
# #     return delete_purchase_details(db, purchase_details_in, current_user)
