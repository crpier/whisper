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
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("hashed_password", sa.String(255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "users", ["email"], unique=True)
    op.create_index(
        op.f("ix_user_full_name"), "users", ["full_name"], unique=False
    )
    op.create_index(op.f("ix_user_id"), "users", ["id"], unique=False)
    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(255), nullable=True),
        sa.Column("description", sa.String(255), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_item_description"), "items", ["description"], unique=False
    )
    op.create_index(op.f("ix_item_id"), "items", ["id"], unique=False)
    op.create_index(op.f("ix_item_title"), "items", ["title"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_item_title"), table_name="items")
    op.drop_index(op.f("ix_item_id"), table_name="items")
    op.drop_index(op.f("ix_item_description"), table_name="items")
    op.drop_table("items")
    op.drop_index(op.f("ix_user_id"), table_name="users")
    op.drop_index(op.f("ix_user_full_name"), table_name="users")
    op.drop_index(op.f("ix_user_email"), table_name="users")
    op.drop_table("users")
