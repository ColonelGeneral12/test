"""add coloumn to posts table

Revision ID: a16ae62efde1
Revises: ae32fa77298a
Create Date: 2023-10-06 02:59:32.066926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a16ae62efde1'
down_revision: Union[str, None] = 'ae32fa77298a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('post', 'content')
    pass
