from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://claftmkmejsnbz:e2ffbb0cd4b19b54aa4c207df4408b54123a130aa9c28470539b091dcb8eb819@ec2-3-218-71-191.compute-1.amazonaws.com:5432/d8fapcrmgd221p"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()