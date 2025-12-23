from api.models.purchase_details import PurchaseDetails as PurchaseDetailsModel
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select
from api.models.users import Users


def get_purchase_details(db: Session, current_user: Users):
    try:
        query = (
            select(PurchaseDetailsModel).
            filter(
                PurchaseDetailsModel.company_id == current_user.company_id)
        )
        result = db.execute(query)
        purchase_details = result.scalars().all()
        return purchase_details
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# def update_purchase_details(db: Session, purchase_details_in: PutPurchaseDetailsIn, current_user: Users):
#     try:
#         query = (select(PurchaseDetailsModel).filter(
#             PurchaseDetailsModel.purchase_id == purchase_details_in.purchase_id).
#             filter(PurchaseDetailsModel.company_id == current_user.company_id))
#         result = db.execute(query)
#         purchase_details = result.scalar_one_or_none()
#         if not purchase_details:
#             db.rollback()
#             raise HTTPException(
#                 status_code=404, detail="purchase details not found")
#         purchase_details.supplier_name = purchase_details_in.supplier_name
#         purchase_details.product_name = purchase_details_in.product_name
#         purchase_details.qty = purchase_details_in.qty
#         purchase_details.supply_price = purchase_details_in.supply_price
#         purchase_details.due_date = purchase_details_in.due_date
#         db.commit()
#         db.refresh(purchase_details)
#         return purchase_details
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()


# def create_purchase_details(db: Session, purchase_details_in: PostPurchaseDetailsIn, current_user: Users):
#     try:
#         purchase_details = PurchaseDetailsModel(
#             company_id=current_user.company_id,
#             created_by_user_id=current_user.user_id,
#             **purchase_details_in.model_dump())
#         db.add(purchase_details)
#         db.commit()
#         db.refresh(purchase_details)
#         return purchase_details
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()


# def delete_purchase_details(db: Session, purchase_details_in: DeletePurchaseDetailsOut, current_user: Users):
#     try:
#         query = select(PurchaseDetailsModel).filter(
#             PurchaseDetailsModel.purchase_id == purchase_details_in.purchase_id)
#         result = db.execute(query)
#         purchase_details = result.scalar_one_or_none()
#         if not purchase_details:
#             db.rollback()
#             raise HTTPException(
#                 status_code=404, detail="purchase details not found")
#         db.delete(purchase_details)
#         db.commit()
#         return purchase_details
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()
