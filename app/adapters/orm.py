from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import registry

from app.models.domain_model import User

mapper_registry = registry()

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(255)),
    Column("email", String(255), unique=True, index=True, nullable=False),
    Column("hashed_password", String(255), nullable=False),
    # TODO: stations, own_playlists, saved_playlists
)

mapper_registry.map_imperatively(User, user_table)
