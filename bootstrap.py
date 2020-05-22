from db import Base, engine, session
from models.models import Visits
import sqlalchemy


def bootstrap():
    Base.metadata.create_all(engine)
    try:
        session.add(Visits(visited_id=1, current_id=0))
        session.commit()
        session.close()
    except sqlalchemy.exc.IntegrityError:
        print('Initial values already added.')
        session.rollback()
