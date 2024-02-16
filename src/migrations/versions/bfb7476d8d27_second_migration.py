"""second migration

Revision ID: bfb7476d8d27
Revises: b1bcb677643c
Create Date: 2024-02-16 10:23:31.485001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bfb7476d8d27'
down_revision: Union[str, None] = 'b1bcb677643c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
