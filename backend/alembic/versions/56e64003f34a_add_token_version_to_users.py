"""add_token_version_to_users

Revision ID: 56e64003f34a
Revises: 09e05065824b
Create Date: 2025-11-08 22:25:50.664858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56e64003f34a'
down_revision: Union[str, Sequence[str], None] = '09e05065824b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add token_version column with default value 0
    op.add_column('users', sa.Column('token_version', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove token_version column
    op.drop_column('users', 'token_version')
