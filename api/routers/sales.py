from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from api.database.db import get_db
from api.schemas.sales import GetSalesOut, PostSalesIn, PostSalesOut, PutSalesIn, PutSalesOut, DeleteSalesOut, GetSalesDetailOut, GetSalesTrendOut, GetYearSalesOut, GetTopSalesOut
from api.cruds.sales import create_sales, get_sales, update_sales, delete_sales, get_sales_detail, get_sales_trend, get_year_sales, get_top_sales
from datetime import date
from api.utils.auth import get_current_user
from api.models.users import Users


router = APIRouter()


# GET
@router.get("/api/sales", tags=["sales"], response_model=List[GetSalesOut])
def get_sales_endpoint(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return get_sales(db, current_user)


@router.get("/api/sales/{sales_id}", tags=["sales"], response_model=GetSalesDetailOut)
def get_sales_detail_endpoint(
    sales_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return get_sales_detail(db, sales_id, current_user)


# 売上推移画面、開始月と終了月を指定して、その間の売上金額を取得
@router.get("/api/sales/trend/{client_id}", tags=["sales"], response_model=List[GetSalesTrendOut])
def get_sales_trend_endpoint(
    client_id: int,
    start_date: date = Query(..., description="開始日"),
    end_date: date = Query(..., description="終了日"),
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):

    return get_sales_trend(db, start_date, end_date, current_user, client_id)

# 年間売上金額を取得
@router.get("/api/sales/trend/year/{year}", tags=["sales"], response_model=List[GetYearSalesOut])
def get_year_sales_endpoint(
    year: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return get_year_sales(db, year, current_user)

# トップ3顧客を取得
@router.get("/api/sales/top/{year}", tags=["sales"], response_model=List[GetTopSalesOut])
def get_top_sales_endpoint(
    year: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return get_top_sales(db, current_user, year)

# POST
@router.post("/api/sales", tags=["sales"], response_model=PostSalesOut)
def create_sales_endpoint(
    sales_in: PostSalesIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return create_sales(db, sales_in, current_user)


# PUT
@router.put("/api/sales/{sales_id}", tags=["sales"], response_model=PutSalesOut)
def update_sales_endpoint(
    sales_id: int,
    sales_in: PutSalesIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return update_sales(db, sales_id, sales_in, current_user)


# DELETE
@router.delete("/api/sales/{sales_id}", tags=["sales"], response_model=DeleteSalesOut)
def delete_sales_endpoint(
    sales_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return delete_sales(db, sales_id, current_user)
