from sqlalchemy import Column, Integer, LargeBinary, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Image(Base):
    __tablename__ = "Image"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Property_Id = Column(Integer, ForeignKey("Property.Id"))
    Image = Column(LargeBinary)

    # Define a relationship with the Property model if needed
    # property = relationship("Property", back_populates="images")
