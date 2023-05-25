import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

file_config = pathlib.Path(__file__).parent.parent.joinpath("conf/config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get("DEV", "USER")
password = config.get("DEV", "PASSWORD")
domain = config.get("DEV", "DOMAIN")
port = config.get("DEV", "PORT")
db_name = config.get("DEV", "DB_NAME")


DATABASE_URL = f"postgresql://{username}:{password}@{domain}:{port}/{db_name}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(DATABASE_URL, max_overflow=5)  #  echo=True,

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
