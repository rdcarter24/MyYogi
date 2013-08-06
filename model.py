from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound


# Use connection function below when initializing database.
# Comment 9 though 12 out when using connection function
ENGINE = None
Session = None
ENGINE = create_engine("sqlite:///yoga.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))

Base = declarative_base()

#comment 16 through 17 out when using connect function below
Base.query = session.query_property()
Base.metadata.create_all(ENGINE)


#Class declaration
class Asana(Base):
    __tablename__ = "asanas"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    image = Column(String(64), nullable=True)
    side = Column(String(1), nullable=True)
    routine = Column(String(64), nullable=True)
    breaths = Column(Integer, nullable=True)
    variance = Column(Integer, nullable=True)


class Flow(Base):
    __tablename__ = "flows"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable= False)
    sequence = Column(String(64), nullable=True) 
    cycles = Column(Integer, nullable=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable= False)
    email = Column(String(64), nullable=False) 
    password = Column(Integer, nullable=False) 

#use connect function when initializing database
# def connect():
#     global ENGINE
#     global Session

#     ENGINE = create_engine("sqlite:///yoga.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()