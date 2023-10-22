"""add final columns to posts table

Revision ID: a17cffe83f63
Revises: 77ca60b1c675
Create Date: 2023-10-07 02:33:11.986390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a17cffe83f63'
down_revision: Union[str, None] = '77ca60b1c675'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'
    ))
    op.add_column('post', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')
    ))
    pass


def downgrade() -> None:
    op.drop_column('post', 'published')
    op.drop_column('post', 'created_at')
    pass
