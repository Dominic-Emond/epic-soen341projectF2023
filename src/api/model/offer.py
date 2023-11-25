from sqlalchemy import Table, Column, Integer, DECIMAL, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from pydantic import BaseModel

meta = MetaData()

# Offer Table
offers = Table(
    'Offer', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True),
    Column('Price', DECIMAL),
    Column('PropertyId', Integer, ForeignKey('Property.Id')),
    Column('ClientId', Integer, ForeignKey('Client.Id')),
)

# Offer Class (Pydantic model)
class Offer(BaseModel):
    Price: float
    PropertyId: int
    ClientId: int