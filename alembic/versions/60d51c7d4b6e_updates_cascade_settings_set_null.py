"""updates cascade settings set null

Revision ID: 60d51c7d4b6e
Revises: bd9725f6e04e
Create Date: 2023-09-26 14:40:02.049740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60d51c7d4b6e'
down_revision: Union[str, None] = 'bd9725f6e04e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('products_owner_id_fkey', 'products', type_='foreignkey')
    op.create_foreign_key(None, 'products', 'users', ['owner_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.create_foreign_key('products_owner_id_fkey', 'products', 'users', ['owner_id'], ['id'])
    # ### end Alembic commands ###