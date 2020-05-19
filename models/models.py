from sqlalchemy import Column, String, Integer
import sys
sys.path.append('..')
from db import Base


class Website(Base):
    __tablename__ = 'websites'
    website_id = Column(Integer, primary_key=True)
    name = Column(String)
    server = Column(String)
