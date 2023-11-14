from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "User"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    First_Name = Column(String(255), nullable=False)
    Last_Name = Column(String(255), nullable=False)
    Username = Column(String(255), nullable=False, unique=True)
    Password = Column(String(255), nullable=False)
    Email = Column(String(255), nullable=False)
    BrokerID = Column(Integer)
    isBroker = Column(Boolean, default=False)
    isClient = Column(Boolean, default=False)
    isSysAdmin = Column(Boolean, default=False)
