"""fourth migration

Revision ID: 2b42d15670e9
Revises: 5e96519a8134
Create Date: 2024-02-16 10:28:24.932918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b42d15670e9'
down_revision: Union[str, None] = '5e96519a8134'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
