from sqlalchemy  import Column, Integer, VARCHAR, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TDbear(Base):

    __tablename__ = 'tdbear'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(VARCHAR(length=1000))
    bio = Column(VARCHAR(length=1000))
    dates = Column(VARCHAR(length=255))

    format = Column(VARCHAR(length=50))
    amount = Column(Integer)
    action = Column(VARCHAR(length=255))
    key_search = Column(VARCHAR(1000))
