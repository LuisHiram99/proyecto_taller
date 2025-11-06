"""add_default_workshop

Revision ID: 1ce9fd71484e
Revises: 757e44044a3e
Create Date: 2025-11-06 12:51:54.561381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext


# revision identifiers, used by Alembic.
revision: str = '1ce9fd71484e'
down_revision: Union[str, Sequence[str], None] = '757e44044a3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Insert default workshop with ID 1
    op.execute("""
        INSERT INTO workshops (workshop_id, workshop_name, address, opening_hours, closing_hours)
        VALUES (1, 'Default Workshop', 'Default Address', '09:00', '18:00')
        ON CONFLICT (workshop_id) DO NOTHING;
    """)
    
    # Hash default admin password using passlib (argon2)
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
    hashed = pwd_context.hash("admin")

    # Use a connection to execute with parameters
    bind = op.get_bind()
    bind.execute(
        sa.text("""
            INSERT INTO users (user_id, first_name, last_name, email, role, hashed_password, workshop_id)
            VALUES (:user_id, :first_name, :last_name, :email, :role, :hashed_password, :workshop_id)
            ON CONFLICT (user_id) DO NOTHING;
        """),
        {
            "user_id": 1,
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@mail.com",
            "role": "admin",
            "hashed_password": hashed,
            "workshop_id": 1,
        },
    )



def downgrade() -> None:
    """Downgrade schema."""
    pass
