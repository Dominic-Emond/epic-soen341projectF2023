from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "Client"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    First_Name = Column(String(255))
    Last_Name = Column(String(255))
    Type = Column(String(255))
    Username = Column(String(255), unique=True)
    Pass = Column(String(255))
