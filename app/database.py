from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://mixlab:mixlab@127.0.0.1:3306/standard?charset=utf8"
# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

