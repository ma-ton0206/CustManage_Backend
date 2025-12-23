from api.schemas.base import AuditTimestamps
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from api.constants.status import SalesStatus
from api.schemas.purchase_details import GetPurchaseDetailsOut
from api.schemas.purchase_details import PutPurchaseDetailsIn, PostPurchaseDetailsIn


# GET
class GetSalesOut(BaseModel):
    sales_id: int = Field(..., description="販売ID")
    sales_number: str = Field(..., description="販売番号")
    sales_name: str = Field(..., description="物件名")
    client_name: str = Field(..., description="顧客名")
    order_date: date = Field(..., description="注文日")
    sales_price: int = Field(..., description="販売金額")
    status: SalesStatus = Field(..., description="ステータス")

    model_config = ConfigDict(from_attributes=True)


# class PurchaseDetails(BaseModel):
#     sales_id: int = Field(..., description="販売ID")
#     supplier_name: str = Field(..., description="仕入先名")
#     product_name: str = Field(..., description="商品名")
#     qty: int = Field(..., description="数量")
#     unit_price: int = Field(..., description="単価")
#     total_price: int = Field(..., description="合計金額")
#     due_date: date = Field(..., description="納品日")

#     model_config = ConfigDict(from_attributes=True)

class GetSalesTrendIn(BaseModel):
    client_id: int = Field(..., description="顧客ID")


class GetSalesDetailOut(BaseModel):
    sales_id: int = Field(..., description="販売ID")
    sales_price: int = Field(..., description="販売金額")
    client_name: str = Field(..., description="顧客名")
    order_date: date = Field(..., description="注文日")
    sales_date: date = Field(..., description="売上日")
    sales_name: str = Field(..., description="物件名")
    status: SalesStatus = Field(..., description="ステータス")
    sales_note: Optional[str] = Field(None, description="備考")
    purchase_details: List[GetPurchaseDetailsOut] = Field(
        ..., description="仕入明細")

    model_config = ConfigDict(from_attributes=True)


# PUT
class PutSalesIn(BaseModel):
    sales_name: str = Field(..., description="物件名")
    sales_price: int = Field(..., description="販売金額")
    order_date: date = Field(..., description="注文日")
    sales_date: date = Field(..., description="売上日")
    status: SalesStatus = Field(..., description="ステータス")
    sales_note: Optional[str] = Field(None, description="備考")
    purchase_details: List[PutPurchaseDetailsIn] = Field(
        ..., description="仕入明細")


class PutSalesOut(AuditTimestamps):
    sales_id: int = Field(..., description="販売ID")


# POST
class PostSalesIn(BaseModel):
    sales_name: str = Field(..., description="物件名")
    sales_price: int = Field(..., description="販売金額")
    client_id: int = Field(..., description="顧客ID")
    order_date: date = Field(..., description="注文日")
    sales_date: date = Field(..., description="売上日")
    status: SalesStatus = Field(..., description="ステータス")
    sales_note: Optional[str] = Field(None, description="備考")
    purchase_details: List[PostPurchaseDetailsIn] = Field(
        ..., description="仕入明細")


class PostSalesOut(AuditTimestamps):
    sales_id: int = Field(..., description="販売ID")


# DELETE
class DeleteSalesOut(AuditTimestamps):
    sales_id: int = Field(..., description="販売ID")


# trend関係


# 月ごとの売上情報
class GetSalesTrendMonth(BaseModel):
    month: int = Field(..., description="月")
    total_sales_price: int = Field(..., description="売上金額")


# 年ごとの売上推移データ
class GetSalesTrendOut(BaseModel):
    year: int = Field(..., description="年")
    data: List[GetSalesTrendMonth] = Field(
        default_factory=list, description="月別売上データ"
    )

    model_config = ConfigDict(from_attributes=True)


# 年間売上金額を取得
class GetYearSalesOut(BaseModel):
    month: int = Field(..., description="月")
    total_sales_price: int = Field(..., description="年間売上金額")

    model_config = ConfigDict(from_attributes=True)


# トップ3顧客
class GetTopSalesOut(BaseModel):
    client_name: str = Field(..., description="顧客名")
    total_sales_price: int = Field(..., description="売上金額")

    model_config = ConfigDict(from_attributes=True)