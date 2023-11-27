from sqlalchemy import Table, Column, Integer, DECIMAL, ForeignKey, MetaData
from pydantic import BaseModel

meta = MetaData()

# Offer Table
offers = Table(
    'Offer', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True),
    Column('Price', DECIMAL),
    Column('PropertyId', Integer, ForeignKey('Property.Id')),
    Column('ClientId', Integer, ForeignKey('Client.Id')),
    Column('BrokerId', Integer, ForeignKey('Broker.Id'))
)

# Offer Class (Pydantic model)
class Offer(BaseModel):
    Price: float
    PropertyId: int
    ClientId: int
    BrokerId: int
