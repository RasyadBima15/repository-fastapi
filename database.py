from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "mysql+pymysql://root:your_password@localhost/db_repositori"

engine = create_engine(URL_DATABASE)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()