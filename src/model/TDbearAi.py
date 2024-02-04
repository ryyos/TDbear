from sqlalchemy  import Column, Integer, VARCHAR, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TDbearAI(Base):

    __tablename__ = 'tdbearai'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(VARCHAR(length=1000))
    bio = Column(VARCHAR(length=1000))
    dates = Column(VARCHAR(length=255))

    action = Column(VARCHAR(length=255))
    question = Column(TEXT)
    answer = Column(TEXT)
