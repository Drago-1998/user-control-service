from database.base import Base
from database.engine import engine


def create_all_tables():
    Base.metadata.create_all(engine)


def create_admin():
    pass


if __name__ == "__main__":
    create_all_tables()
    create_admin()
