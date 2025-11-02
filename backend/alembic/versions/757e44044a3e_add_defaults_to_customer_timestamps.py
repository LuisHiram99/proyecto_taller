"""add_defaults_to_customer_timestamps

Revision ID: 757e44044a3e
Revises: 540a8e2581b0
Create Date: 2025-11-02 14:01:42.858148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '757e44044a3e'
down_revision: Union[str, Sequence[str], None] = '540a8e2581b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add server defaults to the timestamp columns
    op.execute("""
        ALTER TABLE customers 
        ALTER COLUMN created_at SET DEFAULT NOW()
    """)
    
    op.execute("""
        ALTER TABLE customers 
        ALTER COLUMN updated_at SET DEFAULT NOW()
    """)
    
    # Update existing NULL values to NOW()
    op.execute("""
        UPDATE customers 
        SET created_at = NOW() 
        WHERE created_at IS NULL
    """)
    
    op.execute("""
        UPDATE customers 
        SET updated_at = NOW() 
        WHERE updated_at IS NULL
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the defaults
    op.execute("""
        ALTER TABLE customers 
        ALTER COLUMN created_at DROP DEFAULT
    """)
    
    op.execute("""
        ALTER TABLE customers 
        ALTER COLUMN updated_at DROP DEFAULT
    """)
