# sessionはSQLを実行したり、データベースとの通信を行うための一時的な接続
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select
from api.models.company import Company as CompanyModel
from api.models.users import Users


def get_companies(db: Session, current_user: Users):
    try:
        query = select(CompanyModel)
        result = db.execute(query)
        companies = result.scalars().all()
        print("🟢 companies", companies)
        return companies
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# def create_company(db: Session, company_in: PostCompanyIn, current_user: Users):
#     print("!!!!!!create_company", company_in)
#     print("!!!!!!current_user", current_user.user_id)
#     company = CompanyModel(
#         **company_in.model_dump(),
#     )
#     try:
#         db.add(company)
#         db.commit()
#         db.refresh(company)
#         return company
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()


# def update_company(db: Session, company_id: int, company_in: PutCompanyIn, current_user: Users):
#     try:
#         query = select(CompanyModel).filter(
#             CompanyModel.company_id == company_id)
#         result = db.execute(query)
#         company = result.scalar_one_or_none()
#         if not company:
#             db.rollback()
#             raise HTTPException(status_code=404, detail="company not found")
#         company.company_name = company_in.company_name
#         company.updated_by_user_id = current_user.user_id
#         db.commit()
#         db.refresh(company)
#         return company
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()


# def delete_company(db: Session, company_id: int, current_user: Users):
#     try:
#         query = select(CompanyModel).filter(
#             CompanyModel.company_id == company_id)
#         result = db.execute(query)
#         company = result.scalar_one_or_none()
#         if not company:
#             db.rollback()
#             raise HTTPException(status_code=404, detail="company not found")
#         db.delete(company)
#         db.commit()
#         return company
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()
