"""unique email and phone

Revision ID: 6e50e3749b57
Revises: 5223f85321f9
Create Date: 2023-09-19 16:02:50.325718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e50e3749b57'
down_revision: Union[str, None] = '5223f85321f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.drop_index('ix_users_phone', table_name='users')
    op.create_index(op.f('ix_users_phone'), 'users', ['phone'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_phone'), table_name='users')
    op.create_index('ix_users_phone', 'users', ['phone'], unique=False)
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    # ### end Alembic commands ###
