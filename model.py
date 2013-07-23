from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session


# Use connection function below when initializing database.
# Comment 9 though 12 out when using connection function
ENGINE = None
Session = None
ENGINE = create_engine("sqlite:///yoga.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()

# comment 16 through 17 out when using connect function below
Base.query = session.query_property()
Base.metadata.create_all(ENGINE)


#Class declaration
class Asana(Base):
    __tablename__ = "asanas"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    position = Column(Integer, nullable=False)
    movement = Column(String(64), nullable=True)
    time = Column(Integer, nullable=False)

#use connect function when initializing database
# def connect():
#     global ENGINE
#     global Session

#     ENGINE = create_engine("sqlite:///yoga.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()