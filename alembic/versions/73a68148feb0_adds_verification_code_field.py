"""adds verification code field

Revision ID: 73a68148feb0
Revises: bc776f5f25ee
Create Date: 2023-09-27 17:21:50.659823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73a68148feb0'
down_revision: Union[str, None] = 'bc776f5f25ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('verification_code', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'verification_code')
    # ### end Alembic commands ###
