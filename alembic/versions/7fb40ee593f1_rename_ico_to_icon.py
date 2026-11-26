"""rename ico to icon

Revision ID: 7fb40ee593f1
Revises: 7d5eeaae5c53
Create Date: 2026-11-27 00:22:58.850722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fb40ee593f1'
down_revision: Union[str, Sequence[str], None] = '7d5eeaae5c53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("skill", "ico", new_column_name="icon")


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("skill", "icon", new_column_name="ico")