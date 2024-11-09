from .db import engine, metadata

metadata.create_all(engine)