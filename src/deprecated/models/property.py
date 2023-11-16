from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Property(Base):
    __tablename__ = "Property"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Broker_Id = Column(Integer, ForeignKey("Broker.Id"))
    Address = Column(String(255))
    Price = Column(Float)

    # Define a relationship with the Broker model
    broker = relationship("Broker", back_populates="properties")
