# 組織図テーブル

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


class Department(Base):
    __tablename__ = "t_departments"

    department_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("t_clients.client_id", ondelete="CASCADE"), nullable=False)
    parent_department_id: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0)
    department_name: Mapped[str] = mapped_column(String(255), nullable=False)
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

    client = relationship("Client", back_populates="departments", passive_deletes=True )
    contacts = relationship("Contact", back_populates="department")