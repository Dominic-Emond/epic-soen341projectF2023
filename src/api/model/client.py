from sqlalchemy import Table, Column, Integer, String, MetaData
from pydantic import BaseModel

meta = MetaData()

# Client Table
clients = Table(
    'Client', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True),
    Column('First_Name', String, nullable=False),
    Column('Last_Name', String, nullable=False),
    Column('Type', Integer),
    Column('Username', String, nullable=False),
    Column('Pass', String, nullable=False),
)

# Client Class (Pydantic model)
class Client(BaseModel):
    First_Name: str
    Last_Name: str
    Type: int
    Username: str
    Pass: str
