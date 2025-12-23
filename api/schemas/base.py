# 基底モデル
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional


class AuditBase(BaseModel):
    created_by_user_id: Optional[UUID] = Field(None, description="作成者のユーザーID")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_by_user_id: Optional[UUID] = Field(None, description="更新者のユーザーID")
    updated_at: datetime = Field(default_factory=datetime.now)


class AuditTimestamps(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
