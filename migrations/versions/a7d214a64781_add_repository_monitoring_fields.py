"""add repository monitoring fields

Revision ID: a7d214a64781
Revises:
Create Date: 2026-09-05 20:13:16.775330

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a7d214a64781"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Rename the existing column instead of dropping its data.
    op.alter_column(
        "repositories",
        "github_rep_id",
        new_column_name="github_repo_id",
    )

    # Replace the old unique constraint with a properly named one.
    op.drop_constraint(
        "repositories_github_rep_id_key",
        "repositories",
        type_="unique",
    )

    op.create_unique_constraint(
        "uq_repositories_github_repo_id",
        "repositories",
        ["github_repo_id"],
    )

    # Add monitoring fields with temporary server defaults so this
    # migration is also safe if repositories already contain rows.
    op.add_column(
        "repositories",
        sa.Column(
            "is_fork",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.add_column(
        "repositories",
        sa.Column(
            "baseline_sha",
            sa.String(length=40),
            nullable=True,
        ),
    )

    op.add_column(
        "repositories",
        sa.Column(
            "monitoring_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    # Defaults above are only for the migration.
    # The application model controls defaults going forward.
    op.alter_column(
        "repositories",
        "is_fork",
        server_default=None,
    )

    op.alter_column(
        "repositories",
        "monitoring_enabled",
        server_default=None,
    )


def downgrade():
    # Remove fields introduced by this migration.
    op.drop_column(
        "repositories",
        "monitoring_enabled",
    )

    op.drop_column(
        "repositories",
        "baseline_sha",
    )

    op.drop_column(
        "repositories",
        "is_fork",
    )

    # Restore the original unique constraint.
    op.drop_constraint(
        "uq_repositories_github_repo_id",
        "repositories",
        type_="unique",
    )

    op.create_unique_constraint(
        "repositories_github_rep_id_key",
        "repositories",
        ["github_repo_id"],
    )

    # Rename the column back to its original name.
    op.alter_column(
        "repositories",
        "github_repo_id",
        new_column_name="github_rep_id",
    )