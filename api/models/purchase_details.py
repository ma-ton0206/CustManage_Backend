# 仕入明細テーブル

from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String, Integer, DateTime, ForeignKey, Float,
    func,
)
from api.database.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import Optional


class PurchaseDetails(Base):
    __tablename__ = "t_purchase_details"

    purchase_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sales_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("t_sales.sales_id", ondelete="CASCADE"), nullable=True)
    supplier_name: Mapped[str] = mapped_column(String(255), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    supply_price: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now())
    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("m_companies.company_id"), nullable=True)
    
    created_by_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("m_users.user_id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("m_users.user_id"), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    sales = relationship("Sales", back_populates="purchase_details")