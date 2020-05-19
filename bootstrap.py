from db import Base, engine


def bootstrap():
    Base.metadata.create_all(engine)
