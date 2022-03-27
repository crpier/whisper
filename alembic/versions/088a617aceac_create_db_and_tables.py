"""create db and tables

Revision ID: 088a617aceac
Revises:
Create Date: 2022-02-13 20:58:10.587728

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "088a617aceac"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("hashed_password", sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_user_id"), "users", ["id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_user_id"), table_name="users")
    op.drop_index(op.f("ix_user_email"), table_name="users")
    op.drop_table("users")
