from sqlalchemy import Table, Column, Integer, DECIMAL, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from pydantic import BaseModel


meta = MetaData()

# Favourite Table
favourites = Table(
    'Favourite', meta,
    Column('PropertyId', Integer, ForeignKey('Property.Id')),
    Column('ClientId', Integer, ForeignKey('Client.Id')),
)

class Favourite(BaseModel):
    PropertyId: int
    ClientId: int