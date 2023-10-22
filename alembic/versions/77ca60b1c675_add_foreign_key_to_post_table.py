"""add foreign-key to post table

Revision ID: 77ca60b1c675
Revises: 46e463087164
Create Date: 2023-10-07 02:19:06.152665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77ca60b1c675'
down_revision: Union[str, None] = '46e463087164'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="post", referent_table="users", local_cols=['owner_id'], 
                          remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="post")
    op.drop_column('post', 'owner_id')
    pass
