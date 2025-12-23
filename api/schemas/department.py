from api.schemas.base import AuditTimestamps
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


# GET
class GetDepartmentOut(BaseModel):
    department_id: int = Field(..., description="部署ID")
    parent_department_id: int = Field(..., description="親部署ID")
    department_name: str = Field(..., description="部署名")
    children: List["GetDepartmentOut"] = Field(default_factory=list, description="子部署")

    model_config = ConfigDict(from_attributes=True)


# PUT
# departmentsの中身を配列で持っている
class PutDepartmentIn(BaseModel):
    department_id: Optional[int] = Field(None, description="部署ID")
    department_name: str = Field(..., description="部署名")
    parent_department_id: int = Field(..., description="親部署ID")


class PutDepartmentsOut(AuditTimestamps):
    department_id: int = Field(..., description="部署ID")

# delete


class DeleteDepartmentIn(BaseModel):
    department_id: int = Field(..., description="部署ID")


class DeleteDepartmentOut(AuditTimestamps):
    department_id: int = Field(..., description="部署ID")


# POST
class PostDepartmentIn(BaseModel):
    parent_department_id: int = Field(..., description="親部署ID")
    department_name: str = Field(..., description="部署名")


class PostDepartmentOut(AuditTimestamps):
    department_id: int = Field(..., description="部署ID")

class UpdateDepartmentNameIn(BaseModel):
    department_name: str = Field(..., description="部署名")
    
class UpdateDepartmentNameOut(AuditTimestamps):
    department_id: int = Field(..., description="部署ID")