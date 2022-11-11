from models import Base
from alembic import *
from sqlalchemy import create_engine

target_metadata = Base.metadata

def run_migrations_online():
    engine = create_engine("sqlite:///db.sqlite", echo=True, future=True)

    with engine.connect() as connection:
        context.configure(
                    connection=connection,
                    target_metadata=target_metadata
                    )

        with context.begin_transaction():
            context.run_migrations()


if __name__ == "__main__":
    run_migrations_online()
