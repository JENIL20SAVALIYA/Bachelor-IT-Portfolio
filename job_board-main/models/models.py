from sqlalchemy import Integer,String,Column,ForeignKey
from sqlalchemy.ext.declarative import  declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)  
    title = Column(String)
    description = Column(String)
    salary = Column(Integer)

class User(Base):
    __tablename__ = "users"

    username = Column(String,primary_key=True,index=True)
    email = Column(String,primary_key=True)
    password = Column(String)





