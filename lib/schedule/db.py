import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as SqlalchemySession

engine = create_engine(os.getenv('SCHEDULE_DB_CONNECTION_STRING'), connect_args={'check_same_thread': False})
sm = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def Session() -> SqlalchemySession:
    return sm()