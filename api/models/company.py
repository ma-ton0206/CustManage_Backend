# ユーザー所属企業テーブルの定義

from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String, Integer, DateTime, ForeignKey,
    func,
)
from api.database.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


# Companyテーブルの定義
#ここは直打ちを想定。

class Company(Base):
    __tablename__ = "m_companies"

    company_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    company_address: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
