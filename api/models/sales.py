# 販売実績テーブル

from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String, Integer, DateTime, ForeignKey, Float,
    func,
)
from sqlalchemy import Enum as SQLAlchemyEnum
from api.database.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from api.constants.status import SalesStatus


class Sales(Base):
    __tablename__ = "t_sales"

    sales_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("t_clients.client_id", ondelete="CASCADE"), nullable=False)
    sales_number: Mapped[str] = mapped_column(String(255), nullable=False)
    sales_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sales_price: Mapped[int] = mapped_column(Integer, nullable=False)  # 販売金額
    total_supply_price: Mapped[int] = mapped_column(
        Integer, nullable=False)  # 仕入金額
    gross_profit: Mapped[int] = mapped_column(Integer, nullable=False)  # 粗利
    gross_profit_rate: Mapped[float] = mapped_column(
        Float, nullable=False)  # 粗利率
    order_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now())
    sales_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now())
    status: Mapped[SalesStatus] = mapped_column(
        SQLAlchemyEnum(SalesStatus, name="sales_status_enum"),
        nullable=False,
        default=SalesStatus.ORDER_CONFIRMED.name,
        server_default="ORDER_CONFIRMED"
    )
    sales_note: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True)
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

    client = relationship("Client", back_populates="sales")
    purchase_details = relationship(
        "PurchaseDetails", back_populates="sales", cascade="all, delete-orphan", passive_deletes=True)
