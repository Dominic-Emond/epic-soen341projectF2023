from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Broker(Base):
    __tablename__ = "Broker"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    First_Name = Column(String(255))
    Last_Name = Column(String(255))
    Email_Address = Column(String(255))
    Username = Column(String(255), unique=True)
    Pass = Column(String(255))

    # Define relationships if needed
    # For example, if a Broker can have multiple properties
    properties = relationship("Property", back_populates="broker")
