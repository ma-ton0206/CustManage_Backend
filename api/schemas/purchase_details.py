from api.schemas.base import AuditTimestamps
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional


class GetPurchaseDetailsOut(BaseModel):
    purchase_id: int = Field(..., description="仕入ID")
    # sales_id: int = Field(..., description="販売ID")
    supplier_name: str = Field(..., description="仕入先名")
    product_name: str = Field(..., description="商品名")
    qty: int = Field(..., description="数量")
    supply_price: int = Field(..., description="単価")
    due_date: date = Field(..., description="納品日")

    model_config = ConfigDict(from_attributes=True)


class PutPurchaseDetailsIn(BaseModel):
    # purchase_id: int = Field(..., description="仕入ID")
    # sales_id: int = Field(..., description="販売ID")
    supplier_name: str = Field(..., description="仕入先名")
    product_name: str = Field(..., description="商品名")
    qty: int = Field(..., description="数量")
    supply_price: int = Field(..., description="単価")
    purchase_id: Optional[int] = Field(None, description="仕入ID")
    due_date: date = Field(..., description="納品日")


class PutPurchaseDetailsOut(AuditTimestamps):
    purchase_id: int = Field(..., description="仕入ID")


class PostPurchaseDetailsIn(BaseModel):
    # sales_id: int = Field(..., description="販売ID")
    supplier_name: str = Field(..., description="仕入先名")
    product_name: str = Field(..., description="商品名")
    qty: int = Field(..., description="数量")
    supply_price: int = Field(..., description="単価")
    due_date: date = Field(..., description="納品日")


# class PostPurchaseDetailsOut(AuditTimestamps):
#     purchase_id: int = Field(..., description="仕入ID")


# class DeletePurchaseDetailsOut(AuditTimestamps):
#     purchase_id: int = Field(..., description="仕入ID")
