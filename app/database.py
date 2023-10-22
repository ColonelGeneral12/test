from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor

#SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:kali@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#   try:
#      conn = psycopg2.connect(host='localhost', database='fastapi',user='postgres', password='kali', cursor_factory=RealDictCursor)

# the cursor factory returns the coloumn names and values
# host - the ip address of the database
# password - password of the database

#     cursor = conn.cursor()
# this(cursor) is used to execute sql statements

#    print("success")
#    break

# except Exception as error:
#   print("failed.")
#  print(error)
# time.sleep(5)
