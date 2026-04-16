"""add orders vehicle enum is_active

Revision ID: ba41c4275202
Revises: 6f6c4490504a
Create Date: 2026-04-16 16:54:32.332950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba41c4275202'
down_revision: Union[str, Sequence[str], None] = '6f6c4490504a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # сначала создаём тип в PostgreSQL
    orderstatus = sa.Enum('SEARCH', 'IN_PROGRESS', 'DONE', 'CANCELLED', name='orderstatus')
    orderstatus.create(op.get_bind())

    # добавляем is_active
    op.add_column('orders', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.execute("UPDATE orders SET is_active = TRUE WHERE is_active IS NULL")
    op.alter_column('orders', 'is_active', nullable=False)

    # теперь меняем тип колонки — тип уже существует
    op.execute("UPDATE orders SET status = 'SEARCH' WHERE status = 'search'")
    op.execute("UPDATE orders SET status = 'IN_PROGRESS' WHERE status = 'in_progress'")
    op.execute("UPDATE orders SET status = 'DONE' WHERE status = 'done'")
    op.execute("UPDATE orders SET status = 'CANCELLED' WHERE status = 'cancelled'")
    op.alter_column('orders', 'status',
               existing_type=sa.VARCHAR(),
               type_=sa.Enum('SEARCH', 'IN_PROGRESS', 'DONE', 'CANCELLED', name='orderstatus'),
               existing_nullable=False,
               postgresql_using='status::orderstatus')

def downgrade() -> None:
    op.alter_column('orders', 'status',
               existing_type=sa.Enum('SEARCH', 'IN_PROGRESS', 'DONE', 'CANCELLED', name='orderstatus'),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               postgresql_using='status::varchar')
    op.drop_column('orders', 'is_active')

    orderstatus = sa.Enum('SEARCH', 'IN_PROGRESS', 'DONE', 'CANCELLED', name='orderstatus')
    orderstatus.drop(op.get_bind())
