# ユーザーテーブル

from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String, Integer, DateTime, ForeignKey, Boolean,
    func,
)
from api.database.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from api.constants.status import UserRole
from sqlalchemy import Enum as SQLAlchemyEnum

class Users(Base):
    __tablename__ = "m_users"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("m_companies.company_id"), nullable=True)
    user_name: Mapped[str] = mapped_column(String(255), nullable=True)
    user_email: Mapped[str] = mapped_column(String(255), nullable=False)
    user_password: Mapped[str] = mapped_column(String(255), nullable=True)
    user_role: Mapped[UserRole] = mapped_column(SQLAlchemyEnum(UserRole, name="user_role_enum"), nullable=False, default=UserRole.USER.name, server_default="USER")

    # ユーザーの有効/無効を管理するフラグ 退職者など
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True)

    created_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),ForeignKey("m_users.user_id"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("m_users.user_id"), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
