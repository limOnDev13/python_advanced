"""Add user.surname

Revision ID: ad88152a2f54
Revises: 8ce4cbc3f3ce
Create Date: 2024-08-30 10:37:08.421647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad88152a2f54'
down_revision: Union[str, None] = '8ce4cbc3f3ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('surname', sa.VARCHAR(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'surname')
    # ### end Alembic commands ###
