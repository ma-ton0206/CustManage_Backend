"""fix company_id type to uuid in m_users

Revision ID: d74265ddb20e
Revises: 390314b7e59b
Create Date: 2025-10-14 06:54:34.408992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd74265ddb20e'
down_revision: Union[str, Sequence[str], None] = '390314b7e59b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from sqlalchemy.dialects import postgresql as psql

def upgrade() -> None:
    """Fix m_users.company_id to UUID type"""

    # ① 外部キー制約が残っている場合を安全に削除
    try:
        op.drop_constraint('m_users_company_id_fkey', 'm_users', type_='foreignkey')
    except Exception:
        pass  # 既に削除済みでもOK

    # ② 旧カラム削除（integer版）
    try:
        op.drop_column('m_users', 'company_id')
    except Exception:
        pass  # 既に無ければスキップ

    # ③ UUIDカラムを再作成
    op.add_column(
        'm_users',
        sa.Column('company_id', psql.UUID(as_uuid=True), nullable=True)
    )

    # ④ 外部キーをUUID型に合わせて再作成
    op.create_foreign_key(
        'm_users_company_id_fkey',
        source_table='m_users',
        referent_table='m_companies',
        local_cols=['company_id'],
        remote_cols=['company_id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
