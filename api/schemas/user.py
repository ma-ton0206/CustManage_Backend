from datetime import date, datetime  # yyyy-mm-dd
from api.schemas.base import AuditTimestamps
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from api.constants.status import UserRole


class PostUserIn(BaseModel):
    user_email: str = Field(..., description="ユーザーEメール")
    user_password: str = Field(..., description="パスワード")
    user_name: str = Field(..., description="ユーザー名")
    company_id: UUID = Field(..., description="企業ID")


class PostUserOut(AuditTimestamps):
    user_id: UUID = Field(..., description="ユーザーID")
    company_id: UUID = Field(..., description="企業ID")


class PutUserIn(BaseModel):
    user_email: str = Field(..., description="ユーザーEメール")
    user_password: str = Field(..., description="パスワード")
    user_name: str = Field(..., description="ユーザー名")


class PutUserOut(AuditTimestamps):
    user_id: UUID = Field(..., description="ユーザーID")


class DeleteUserOut(AuditTimestamps):
    user_id: UUID = Field(..., description="ユーザーID")


class GetUserOut(AuditTimestamps):
    user_id: UUID = Field(..., description="ユーザーID")
    user_name: str = Field(..., description="ユーザー名")
    user_email: str = Field(..., description="ユーザーEメール")
    user_role: UserRole = Field(..., description="ユーザー権限")

    model_config = ConfigDict(from_attributes=True)


class LoginUserIn(BaseModel):
    user_email: str = Field(..., description="ユーザーEメール")
    user_password: str = Field(..., description="パスワード")


class LoginUserOut(BaseModel):
    token: str = Field(..., description="トークン")
    user_id: UUID = Field(..., description="ユーザーID")
    user_name: str = Field(..., description="ユーザー名")
    user_email: str = Field(..., description="ユーザーEメール")
    user_role: UserRole = Field(..., description="ユーザー権限")


class AdminCreateUserIn(BaseModel):
    user_email: str = Field(..., description="ユーザーEメール")
    user_role: UserRole = Field(..., description="ユーザー権限")


class AdminCreateUserOut(BaseModel):
    message: str = Field(..., description="メッセージ")
    user_email: str = Field(..., description="ユーザーEメール")
    token: str = Field(..., description="トークン")


class ActivateUserIn(BaseModel):
    user_name: str = Field(..., description="ユーザー名")
    user_email: str = Field(..., description="ユーザーEメール")
    user_password: str = Field(..., description="パスワード")
    token: str = Field(..., description="トークン")


class ActivateUserOut(BaseModel):
    message: str = Field(..., description="メッセージ")
