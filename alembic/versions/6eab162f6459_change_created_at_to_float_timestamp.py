"""change created_at to float timestamp

Revision ID: 6eab162f6459
Revises: 5ab33476c828
Create Date: 2026-02-02 23:45:03.666749

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "6eab162f6459"
down_revision: Union[str, Sequence[str], None] = "5ab33476c828"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("ALTER TABLE chats ALTER COLUMN created_at DROP DEFAULT")
    op.execute("ALTER TABLE messages ALTER COLUMN created_at DROP DEFAULT")

    op.alter_column(
        "chats",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.Float(),
        existing_nullable=False,
        postgresql_using="EXTRACT(EPOCH FROM created_at)::float",
    )
    op.alter_column(
        "messages",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.Float(),
        existing_nullable=False,
        postgresql_using="EXTRACT(EPOCH FROM created_at)::float",
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "messages",
        "created_at",
        existing_type=sa.Float(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
        postgresql_using="TO_TIMESTAMP(created_at)::timestamptz",
    )
    op.alter_column(
        "chats",
        "created_at",
        existing_type=sa.Float(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
        postgresql_using="TO_TIMESTAMP(created_at)::timestamptz",
    )

    op.execute("ALTER TABLE chats ALTER COLUMN created_at SET DEFAULT now()")
    op.execute("ALTER TABLE messages ALTER COLUMN created_at SET DEFAULT now()")
