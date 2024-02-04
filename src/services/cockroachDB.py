import os

from faker import Faker
from dotenv import load_dotenv
from icecream import ic

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy_cockroachdb import run_transaction

from src.model.TDbear import TDbear
from src.model.TDbearAi import TDbearAI
from src.utils import now

class CokroachDB:
    def __init__(self) -> None:
        load_dotenv()
        self.__database = os.getenv('DATABASE_URL').replace("postgresql://", "cockroachdb://")
        self.__engine = create_engine(url=self.__database)
        
        self.__faker = Faker()
        ...

    def post(self, session: Session, component: dict) -> None:

        try:

            session.add(TDbear(
                id=component["id"],
                user_id=component["user_id"],
                username = component["username"],
                bio = component["bio"],
                dates = now(),

                amount = component["amount"],
                action = component["action"],
                key_search = component["key_search"]
            ))

        except Exception as err:
            ic(err)
        ...

    def ai(self, session: Session, component: dict) -> None:

        try:

            session.add(TDbearAI(
                id=component["id"],
                user_id=component["user_id"],
                username = component["username"],
                bio = component["bio"],
                dates = now(),

                action = component["action"],
                question = component["question"],
                answer = component["answer"],
            ))

        except Exception as err:
            ic(err)

    def send(self, component: dict) -> None:

        match component["action"]:

            case 'instagram' | 'pinterest' | 'license' | 'info' | 'start':
                run_transaction(sessionmaker(bind=self.__engine),
                                lambda s: self.post(
                                    session=s,
                                    component=component
                                ))
                
            case 'ai':
                run_transaction(sessionmaker(bind=self.__engine),
                                lambda s: self.ai(
                                    session=s,
                                    component=component
                                ))

        
        ...
