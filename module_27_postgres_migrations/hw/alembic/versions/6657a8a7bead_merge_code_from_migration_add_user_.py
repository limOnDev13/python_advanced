"""merge code from migration Add user patronomic and init migration

Revision ID: 6657a8a7bead
Revises: 7aa9b723e39a, ad88152a2f54
Create Date: 2024-08-30 11:01:30.953935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6657a8a7bead'
down_revision: Union[str, None] = ('7aa9b723e39a', 'ad88152a2f54')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
