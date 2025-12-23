# タスクテーブル

from __future__ import annotations
from typing import Optional
from datetime import datetime, date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String, Integer, Boolean, DateTime, ForeignKey, CheckConstraint,
    func, Index, Date
)
from sqlalchemy import Enum as SQLAlchemyEnum
from api.database.db import Base
from api.constants.status import TaskStatus
from sqlalchemy.dialects.postgresql import UUID
import uuid


# タスクテーブルの定義
class Task(Base):
    # baseを継承することで、SQLAlchemy に「DBテーブル」として登録される。
    # テーブル名
    __tablename__ = "t_task"  # 命名規約は小文字スネークケース推奨（任意）

    # 主キー: autoincrementはInteger PKなら自動なので省略可
    task_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # 外部キー（usersテーブルに合わせて調整）
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("m_users.user_id"), nullable=False, index=True
    )

    is_completed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )

    content: Mapped[str] = mapped_column(
        String(1024), nullable=False
    )

    # 期限：タイムゾーンありを推奨（DBにより対応差あり）
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    status: Mapped[TaskStatus] = mapped_column(
        SQLAlchemyEnum(TaskStatus, name="task_status_enum"),
        nullable=False,
        default=TaskStatus.NOT_STARTED.name,
        server_default="NOT_STARTED"
    )

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

    # 追加の制約やインデックス
    __table_args__ = (
        CheckConstraint(
            "status IN ('NOT_STARTED', 'IN_PROGRESS', 'DONE')", name="ck_task_status_valid"),
        Index("ix_task_user_due", "user_id", "due_date"),
    )
