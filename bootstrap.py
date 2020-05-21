from db import Base, engine, session
from models.models import Website, Visits
import requests
import sqlalchemy


def bootstrap():
    Base.metadata.create_all(engine)
    reader = requests.get("https://register.start.bg")
    server = reader.headers["Server"]
    try:
        session.add(Visits(visited_id=1, current_id=0))
        session.add(Website(name="https://register.start.bg", server=server, parent_id=0))
        session.commit()
        session.close()
    except sqlalchemy.exc.IntegrityError:
        print('Initial values already added.')
        session.rollback()
