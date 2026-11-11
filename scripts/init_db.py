
from sqlalchemy import text

from app.database.connection import engine
from app.database.models import Base


def initialize_database():
    with engine.connect() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        connection.commit()

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully.")


if __name__ == "__main__":
    initialize_database()
