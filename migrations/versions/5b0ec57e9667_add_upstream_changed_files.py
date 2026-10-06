"""add upstream changed files

Revision ID: 5b0ec57e9667
Revises: be1fc5cfc23d
Create Date: 2026-10-06 20:47:22.932208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b0ec57e9667'
down_revision = 'be1fc5cfc23d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "upstream_changes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("upstream_event_id", sa.Integer(), nullable=False),
        sa.Column("file_path", sa.String(length=1024), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("additions", sa.Integer(), nullable=False),
        sa.Column("deletions", sa.Integer(), nullable=False),
        sa.Column("changes", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["upstream_event_id"],
            ["upstream_events.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("upstream_changes")