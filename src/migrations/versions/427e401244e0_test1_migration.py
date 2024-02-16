"""test1 migration

Revision ID: 427e401244e0
Revises: 2b42d15670e9
Create Date: 2024-02-16 10:30:23.271541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '427e401244e0'
down_revision: Union[str, None] = '2b42d15670e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
