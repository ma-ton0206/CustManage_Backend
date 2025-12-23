from api.schemas.base import AuditTimestamps

from pydantic import BaseModel, Field, ConfigDict

# GET
class GetClientOut(BaseModel):
    client_id: int = Field(..., description="クライアントID")
    client_name: str = Field(..., description="クライアント名")
    client_address: str = Field(..., description="住所")
    client_phone: str = Field(..., description="電話番号")

    model_config = ConfigDict(from_attributes=True)


class GetClientDetailOut(BaseModel):
    client_id: int = Field(..., description="クライアントID")
    industry: str = Field(..., description="業種")
    client_phone: str = Field(..., description="電話番号")
    client_address: str = Field(..., description="住所")
    client_name: str = Field(..., description="クライアント名")

    model_config = ConfigDict(from_attributes=True)


class GetTopClientOut(BaseModel):
    client_id: int = Field(..., description="クライアントID")
    client_name: str = Field(..., description="クライアント名")
    year_sales_price: int = Field(..., description="売上金額")

    model_config = ConfigDict(from_attributes=True)


# POST
class PostClientIn(BaseModel):
    client_name: str = Field(..., description="クライアント名")
    industry: str = Field(..., description="業種")
    client_phone: str = Field(..., description="電話番号")
    client_address: str = Field(..., description="住所")


class PostClientOut(AuditTimestamps):
    client_id: int = Field(..., description="クライアントID")


# PUT
class PutClientIn(BaseModel):
    client_name: str = Field(..., description="クライアント名")
    industry: str = Field(..., description="業種")
    client_phone: str = Field(..., description="電話番号")
    client_address: str = Field(..., description="住所")


class PutClientOut(AuditTimestamps):
    client_id: int = Field(..., description="クライアントID")


# DELETE
class DeleteClientOut(AuditTimestamps):
    client_id: int = Field(..., description="クライアントID")


class GetClientNameOut(BaseModel):
    client_name: str = Field(..., description="クライアント名")