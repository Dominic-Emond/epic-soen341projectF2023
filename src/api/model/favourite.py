from sqlalchemy import Table, Column, Integer, DECIMAL, ForeignKey, MetaData
from pydantic import BaseModel


meta = MetaData()

# Favourite Table
favourites = Table(
    'Favourite', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True),
    Column('PropertyId', Integer, ForeignKey('Property.Id')),
    Column('ClientId', Integer, ForeignKey('Client.Id')),
)

class Favourite(BaseModel):
    PropertyId: int
    ClientId: int