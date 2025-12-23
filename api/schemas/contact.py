from api.schemas.base import AuditTimestamps
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class GetContactOut(BaseModel):
    contact_id: int = Field(..., description="担当者ID")
    contact_name: str = Field(..., description="担当者名")
    role: str = Field(..., description="役割")
    contact_email: str = Field(..., description="メールアドレス")
    contact_phone: str = Field(..., description="電話番号")

    model_config = ConfigDict(from_attributes=True)


class PutContactIn(BaseModel):
    contact_id: Optional[int] = Field(None, description="担当者ID")
    contact_name: str = Field(..., description="担当者名")
    role: str = Field(..., description="役割")
    contact_email: str = Field(..., description="メールアドレス")
    contact_phone: str = Field(..., description="電話番号")


class PutContactsOut(AuditTimestamps):
    contact_id: int = Field(..., description="担当者ID")


class DeleteContactIn(BaseModel):
    contact_id: int = Field(..., description="担当者ID")


class DeleteContactOut(AuditTimestamps):
    contact_id: int = Field(..., description="担当者ID")


class PostContactIn(BaseModel):
    department_id: int = Field(..., description="部署ID")
    contact_name: str = Field(..., description="担当者名")
    role: str = Field(..., description="役割")
    contact_email: str = Field(..., description="メールアドレス")
    contact_phone: str = Field(..., description="電話番号")


class PostContactOut(AuditTimestamps):
    contact_id: int = Field(..., description="担当者ID")
