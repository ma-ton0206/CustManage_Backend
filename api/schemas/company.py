from api.schemas.base import AuditTimestamps
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

class GetCompanyOut(BaseModel):
    company_id: UUID = Field(..., description="企業ID")
    company_name: str = Field(..., description="企業名")
    company_address: str = Field(..., description="住所")

    model_config = ConfigDict(from_attributes=True)


# class PutCompanyIn(BaseModel):
#     company_id: int = Field(..., description="企業ID")
#     company_name: str = Field(..., description="企業名")
#     company_address: str = Field(..., description="住所")


# class PutCompanyOut(AuditTimestamps):
#     company_id: int = Field(..., description="企業ID")


# class DeleteCompanyOut(AuditTimestamps):
#     company_id: int = Field(..., description="企業ID")


# class PostCompanyIn(BaseModel):
#     company_name: str = Field(..., description="企業名")
#     company_address: str = Field(..., description="住所")


# class PostCompanyOut(AuditTimestamps):
#     company_id: int = Field(..., description="企業ID")


# class DeleteCompanyOut(AuditTimestamps):
#     company_id: int = Field(..., description="企業ID")

