# 顧客の担当者テーブル

from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String, Integer, DateTime, ForeignKey,
    func,
)
from api.database.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Contact(Base):
    __tablename__ = "t_contacts"

    contact_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    department_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("t_departments.department_id"), nullable=False)
    contact_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(255), nullable=False)
    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("m_companies.company_id"), nullable=True)
    
    created_by_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("m_users.user_id"), nullable=False
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

    department = relationship("Department", back_populates="contacts")
