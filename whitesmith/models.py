from sqlalchemy import Table, Column, Integer, String
from .db import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key="true"),
    Column("name", String(20)),
    Column("email", String(50))


)