from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root@localhost/basepython1?charset=utf8mb4"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
ModeloBase = declarative_base()
