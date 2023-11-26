from sqlalchemy import Table, Column, Integer, String, Float, Boolean, MetaData
from pydantic import BaseModel

meta = MetaData()

# Property Table
properties = Table(
    'Property', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True),
    Column('Address', String, nullable=False),
    Column('City', String, nullable=False),
    Column('Price', Float, nullable=False),
    Column('Bedrooms', Integer, nullable=False),
    Column('Bathrooms', Integer, nullable=False),
    Column('Size_SqFt', Float, nullable=False),
    Column('IsAvailable', Boolean, default=True),
    Column('Broker_Id', Integer)

)

# Property Class (Pydantic model)
class Property(BaseModel):
    Address: str
    City: str
    Price: float
    Bedrooms: int
    Bathrooms: int
    Size_SqFt: float
    IsAvailable: bool = True
    Broker_Id: int = None