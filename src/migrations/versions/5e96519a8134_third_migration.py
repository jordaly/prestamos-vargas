"""third migration

Revision ID: 5e96519a8134
Revises: bfb7476d8d27
Create Date: 2024-02-16 10:25:08.395153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e96519a8134'
down_revision: Union[str, None] = 'bfb7476d8d27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
